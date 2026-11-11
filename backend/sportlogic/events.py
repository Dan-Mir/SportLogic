from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable
from typing import Any


class EventBus:
    def __init__(self) -> None:
        self._handlers: dict[str, list[Callable[..., Any]]] = defaultdict(list)

    def on(self, name: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        def decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
            self._handlers[name].append(fn)
            return fn

        return decorator

    def emit(self, name: str, **payload: Any) -> None:
        for fn in self._handlers.get(name, []):
            fn(**payload)

    def handlers(self, name: str) -> list[Callable[..., Any]]:
        return list(self._handlers.get(name, []))


bus = EventBus()
