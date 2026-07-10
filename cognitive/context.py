"""Context frames: layered, immutable views over cognitive state."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterator, Mapping, Optional


@dataclass(frozen=True)
class ContextFrame:
    """An immutable snapshot of a scope's variables."""

    name: str
    values: Mapping[str, Any] = field(default_factory=dict)
    parent: Optional["ContextFrame"] = None

    def resolve(self, key: str, default: Any = None) -> Any:
        if key in self.values:
            return self.values[key]
        if self.parent is not None:
            return self.parent.resolve(key, default)
        return default

    def extended(self, **overrides: Any) -> "ContextFrame":
        return ContextFrame(name=self.name, values={**self.values, **overrides}, parent=self.parent)

    def flatten(self) -> Dict[str, Any]:
        merged: Dict[str, Any] = {}
        stack = []
        node: Optional[ContextFrame] = self
        while node is not None:
            stack.append(node)
            node = node.parent
        for frame in reversed(stack):
            merged.update(frame.values)
        return merged


class ContextEngine:
    """Push/pop stack of context frames."""

    def __init__(self, root: Optional[ContextFrame] = None) -> None:
        self._current: Optional[ContextFrame] = root

    def push(self, name: str, **values: Any) -> ContextFrame:
        frame = ContextFrame(name=name, values=values, parent=self._current)
        self._current = frame
        return frame

    def pop(self) -> Optional[ContextFrame]:
        if self._current is None:
            return None
        popped = self._current
        self._current = popped.parent
        return popped

    def current(self) -> Optional[ContextFrame]:
        return self._current

    def get(self, key: str, default: Any = None) -> Any:
        return self._current.resolve(key, default) if self._current else default

    def __iter__(self) -> Iterator[ContextFrame]:
        node = self._current
        while node is not None:
            yield node
            node = node.parent
