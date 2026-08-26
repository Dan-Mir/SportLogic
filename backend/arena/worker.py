from __future__ import annotations

import logging
import os
import signal
import threading

import dramatiq
from dramatiq.brokers.redis import RedisBroker
from dramatiq.worker import Worker

logging.basicConfig(level=logging.INFO)

broker = RedisBroker(url=os.environ.get("ARENA_REDIS_URL", "redis://localhost:6379/0"))
dramatiq.set_broker(broker)


@dramatiq.actor
def send_email(to: str, subject: str, body: str) -> None:
    print(f"[worker] invio email a {to}: {subject}")


def main() -> None:
    from arena.modules import discover_builtin  # noqa: F401

    worker = Worker(broker, worker_timeout=1000, worker_threads=4)
    worker.start()

    stop = threading.Event()
    signal.signal(signal.SIGINT, lambda *_: stop.set())
    signal.signal(signal.SIGTERM, lambda *_: stop.set())
    stop.wait()

    worker.stop()


if __name__ == "__main__":
    main()
