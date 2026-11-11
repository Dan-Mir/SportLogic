from __future__ import annotations

import logging
import os
import signal
import smtplib
import threading
from email.message import EmailMessage

import dramatiq
from dramatiq.brokers.redis import RedisBroker
from dramatiq.worker import Worker

logging.basicConfig(level=logging.INFO)

broker = RedisBroker(url=os.environ.get("SPORTLOGIC_REDIS_URL", "redis://localhost:6379/0"))
dramatiq.set_broker(broker)


@dramatiq.actor
def send_email(to: str, subject: str, body: str) -> None:
    from sportlogic.config import get_settings

    settings = get_settings()
    if not settings.smtp_host:
        logging.getLogger(__name__).warning("SMTP non configurato: email non inviata a %s", to)
        return

    message = EmailMessage()
    message["From"] = settings.smtp_from_email or settings.smtp_username
    message["To"] = to
    message["Subject"] = subject
    message.set_content(body)

    with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=30) as server:
        server.ehlo()
        if settings.smtp_use_tls:
            server.starttls()
            server.ehlo()
        if settings.smtp_username:
            server.login(settings.smtp_username, settings.smtp_password)
        server.send_message(message)
    logging.getLogger(__name__).info("Email inviata a %s: %s", to, subject)


def main() -> None:
    from sportlogic.modules import discover_builtin  # noqa: F401

    worker = Worker(broker, worker_timeout=1000, worker_threads=4)
    worker.start()

    stop = threading.Event()
    signal.signal(signal.SIGINT, lambda *_: stop.set())
    signal.signal(signal.SIGTERM, lambda *_: stop.set())
    stop.wait()

    worker.stop()


if __name__ == "__main__":
    main()
