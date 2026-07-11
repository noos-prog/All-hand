#!/usr/bin/env python3
"""
Autoscaler — decides pool sizes from observed utilization, not guesses.

Mirrors the standard target-utilization algorithm used by real autoscalers
(e.g. Kubernetes HPA): grow when a pool is consistently near saturation,
shrink when it is mostly idle, always within a configured [min_size,
max_size] band so a spike cannot exhaust host resources.
"""

from __future__ import annotations

import logging
import math
from dataclasses import dataclass
from typing import Dict

from .pool import AgentPool

logger = logging.getLogger("agos_factory.autoscaler")


@dataclass(frozen=True)
class AutoscalerPolicy:
    """Tuning knobs for one specialization's autoscaling behavior.

    Attributes:
        min_size: Floor for `max_concurrency`; never scales below this.
        max_size: Ceiling for `max_concurrency`; the hard resource budget.
        target_utilization: Desired active/capacity ratio (0-1). The
            algorithm scales the pool so utilization trends toward this
            value, exactly like Kubernetes HPA's targetAverageUtilization.
        step_up_ratio: Max fractional growth allowed in a single decision
            (e.g. 0.5 = pool may grow by at most 50% per tick).
        step_down_ratio: Max fractional shrink allowed in a single decision.
    """

    min_size: int = 1
    max_size: int = 500
    target_utilization: float = 0.7
    step_up_ratio: float = 0.5
    step_down_ratio: float = 0.25

    def __post_init__(self) -> None:
        if self.min_size <= 0 or self.max_size < self.min_size:
            raise ValueError("require 0 < min_size <= max_size")
        if not (0.0 < self.target_utilization <= 1.0):
            raise ValueError("target_utilization must be in (0, 1]")


class Autoscaler:
    """Computes and applies new pool sizes for one or more `AgentPool`s."""

    def __init__(self, default_policy: AutoscalerPolicy | None = None) -> None:
        self._default_policy = default_policy or AutoscalerPolicy()
        self._policies: Dict[str, AutoscalerPolicy] = {}

    def set_policy(self, specialization: str, policy: AutoscalerPolicy) -> None:
        self._policies[specialization] = policy

    def policy_for(self, specialization: str) -> AutoscalerPolicy:
        return self._policies.get(specialization, self._default_policy)

    def recommend(self, pool: AgentPool) -> int:
        """Return the recommended `max_concurrency` for `pool` right now.

        Utilization = active / current capacity. When utilization exceeds
        the target, the desired capacity grows proportionally
        (active / target_utilization); when it is well below target, the
        pool shrinks toward that same proportional target. Growth/shrink
        per call is capped by the policy's step ratios to avoid thrashing.
        """
        policy = self.policy_for(pool.specialization)
        capacity = pool.capacity
        active = pool.active
        utilization = active / capacity if capacity else 1.0

        if utilization <= 0:
            desired = max(policy.min_size, math.floor(capacity * (1 - policy.step_down_ratio)))
        else:
            desired_raw = active / policy.target_utilization
            if utilization > policy.target_utilization:
                max_growth = capacity * (1 + policy.step_up_ratio)
                desired = min(math.ceil(desired_raw), math.ceil(max_growth))
            else:
                max_shrink = capacity * (1 - policy.step_down_ratio)
                desired = max(math.ceil(desired_raw), math.floor(max_shrink))

        desired = max(policy.min_size, min(policy.max_size, desired))
        return desired

    async def tick(self, pool: AgentPool) -> int:
        """Apply one autoscaling decision to `pool`. Returns the new size."""
        desired = self.recommend(pool)
        if desired != pool.capacity:
            logger.info(
                "autoscale '%s': %d -> %d (active=%d, target_util=%.2f)",
                pool.specialization, pool.capacity, desired,
                pool.active, self.policy_for(pool.specialization).target_utilization,
            )
            await pool.resize(desired)
        return desired
