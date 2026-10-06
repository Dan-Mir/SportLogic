from __future__ import annotations

import os

os.environ["SPORTLOGIC_DATABASE_URL"] = "sqlite+pysqlite:///:memory:"
os.environ["SPORTLOGIC_MODULES_ENABLED"] = "core,anagrafica,abbonamenti"

import pytest
from fastapi.testclient import TestClient

import arena.db as db
from arena.db import Base
from arena.main import create_app
from arena.modules.anagrafica.models import Member
from arena.modules.core.models import User
from arena.modules.core.security import hash_password


@pytest.fixture()
def admin_client():
    db._engine = None
    db._session_factory = None
    Base.metadata.create_all(db.get_engine())
    session = db.get_session()
    session.add_all(
        [
            User(
                email="admin@test.it",
                hashed_password=hash_password("password"),
                full_name="Admin Test",
                role="admin",
            ),
            Member(first_name="Mario", last_name="Rossi"),
        ]
    )
    session.commit()
    session.close()
    with TestClient(create_app()) as client:
        response = client.post(
            "/api/core/auth/login", json={"email": "admin@test.it", "password": "password"}
        )
        client.headers.update({"Authorization": f"Bearer {response.json()['access_token']}"})
        yield client


def test_subscription_plan_and_manual_payment(admin_client) -> None:
    plan = admin_client.post(
        "/api/abbonamenti/plans",
        json={"name": "Mensile", "price": "49.90", "duration_days": 30},
    )
    assert plan.status_code == 201, plan.text

    subscription = admin_client.post(
        "/api/abbonamenti/subscriptions",
        json={
            "member_id": 1,
            "plan_id": plan.json()["id"],
            "starts_on": "2026-10-06",
            "ends_on": "2026-11-05",
        },
    )
    assert subscription.status_code == 201, subscription.text

    payment = admin_client.post(
        f"/api/abbonamenti/subscriptions/{subscription.json()['id']}/payments",
        json={"amount": "49.90", "method": "pos", "reference": "POS-001"},
    )
    assert payment.status_code == 201, payment.text
    assert payment.json()["method"] == "pos"


def test_subscription_rejects_invalid_date_range(admin_client) -> None:
    plan = admin_client.post(
        "/api/abbonamenti/plans", json={"name": "Ingressi", "price": "10.00"}
    ).json()
    response = admin_client.post(
        "/api/abbonamenti/subscriptions",
        json={
            "member_id": 1,
            "plan_id": plan["id"],
            "starts_on": "2026-11-01",
            "ends_on": "2026-10-01",
        },
    )
    assert response.status_code == 422
