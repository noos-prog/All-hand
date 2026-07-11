"""Budget Management - Track and manage resource costs."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid


class BudgetPeriod(Enum):
    """Budget periods."""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"


@dataclass
class Budget:
    """A budget allocation."""
    budget_id: str
    owner_id: str
    amount: float
    period: BudgetPeriod
    spent: float = 0.0
    currency: str = "USD"
    start_date: datetime = field(default_factory=datetime.utcnow)
    end_date: Optional[datetime] = None


@dataclass
class BudgetAllocation:
    """An allocation from a budget."""
    allocation_id: str
    budget_id: str
    category: str
    amount: float
    spent: float = 0.0
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class CostTracker:
    """Track costs against budgets."""
    tracker_id: str
    owner_id: str
    category: str
    cost_per_unit: float
    units_used: float = 0.0
    total_cost: float = 0.0


class BudgetManager:
    """Manage budgets and track spending."""
    
    def __init__(self):
        self._budgets: Dict[str, Budget] = {}
        self._allocations: Dict[str, BudgetAllocation] = {}
        self._trackers: Dict[str, CostTracker] = {}
    
    def create_budget(
        self,
        owner_id: str,
        amount: float,
        period: BudgetPeriod,
        currency: str = "USD",
    ) -> Budget:
        budget = Budget(
            budget_id=str(uuid.uuid4()),
            owner_id=owner_id,
            amount=amount,
            period=period,
            currency=currency,
        )
        self._budgets[budget.budget_id] = budget
        return budget
    
    def create_allocation(
        self,
        budget_id: str,
        category: str,
        amount: float,
    ) -> Optional[BudgetAllocation]:
        budget = self._budgets.get(budget_id)
        if not budget:
            return None
        
        if (budget.spent + amount) > budget.amount:
            return None
        
        allocation = BudgetAllocation(
            allocation_id=str(uuid.uuid4()),
            budget_id=budget_id,
            category=category,
            amount=amount,
        )
        self._allocations[allocation.allocation_id] = allocation
        budget.spent += amount
        return allocation
    
    def track_cost(
        self,
        owner_id: str,
        category: str,
        cost_per_unit: float,
        units: float,
    ) -> CostTracker:
        tracker_id = f"{owner_id}:{category}"
        
        if tracker_id in self._trackers:
            tracker = self._trackers[tracker_id]
            tracker.units_used += units
            tracker.total_cost = tracker.units_used * tracker.cost_per_unit
        else:
            tracker = CostTracker(
                tracker_id=tracker_id,
                owner_id=owner_id,
                category=category,
                cost_per_unit=cost_per_unit,
                units_used=units,
                total_cost=units * cost_per_unit,
            )
            self._trackers[tracker_id] = tracker
        
        return tracker
    
    def get_budget(self, budget_id: str) -> Optional[Budget]:
        return self._budgets.get(budget_id)
    
    def get_owner_budgets(self, owner_id: str) -> List[Budget]:
        return [b for b in self._budgets.values() if b.owner_id == owner_id]
    
    def get_remaining(self, budget_id: str) -> float:
        budget = self._budgets.get(budget_id)
        if not budget:
            return 0.0
        return max(0, budget.amount - budget.spent)
    
    def get_statistics(self) -> Dict[str, Any]:
        return {
            "total_budgets": len(self._budgets),
            "total_allocations": len(self._allocations),
            "total_spent": sum(b.spent for b in self._budgets.values()),
            "total_budget": sum(b.amount for b in self._budgets.values()),
        }
