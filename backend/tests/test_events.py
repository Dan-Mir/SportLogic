from __future__ import annotations

from arena.events import EventBus


def test_subscribe_and_emit() -> None:
    bus = EventBus()
    received: list[int] = []

    @bus.on("member.created")
    def handler(member_id: int) -> None:
        received.append(member_id)

    bus.emit("member.created", member_id=42)
    assert received == [42]


def test_multiple_handlers_in_order() -> None:
    bus = EventBus()
    calls: list[str] = []

    @bus.on("x")
    def a() -> None:
        calls.append("a")

    @bus.on("x")
    def b() -> None:
        calls.append("b")

    bus.emit("x")
    assert calls == ["a", "b"]


def test_emit_without_handlers_is_safe() -> None:
    bus = EventBus()
    bus.emit("nope")
