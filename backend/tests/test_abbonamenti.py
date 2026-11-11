from __future__ import annotations

import os

os.environ["SPORTLOGIC_DATABASE_URL"] = "sqlite+pysqlite:///:memory:"
os.environ["SPORTLOGIC_MODULES_ENABLED"] = "core,anagrafica,abbonamenti"

import pytest
from fastapi.testclient import TestClient

import sportlogic.db as db
from sportlogic.db import Base
from sportlogic.main import create_app
from sportlogic.modules.anagrafica.models import Member
from sportlogic.modules.core.models import User
from sportlogic.modules.core.security import hash_password


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


def test_installments_track_partial_payment_and_receipt(admin_client) -> None:
    plan = admin_client.post(
        "/api/abbonamenti/plans", json={"name": "Trimestrale", "price": "120.00"}
    ).json()
    subscription = admin_client.post(
        "/api/abbonamenti/subscriptions",
        json={
            "member_id": 1,
            "plan_id": plan["id"],
            "starts_on": "2026-10-06",
            "ends_on": "2027-01-03",
            "installments_count": 2,
        },
    )
    assert subscription.status_code == 201, subscription.text
    subscription_id = subscription.json()["id"]
    assert [item["amount"] for item in subscription.json()["installments"]] == ["60.00", "60.00"]

    payment = admin_client.post(
        f"/api/abbonamenti/subscriptions/{subscription_id}/payments",
        json={"amount": "25.00"},
    )
    assert payment.status_code == 201, payment.text
    assert payment.json()["receipt"]["receipt_number"].startswith("R-2026-")

    installments = admin_client.get(
        "/api/abbonamenti/installments", params={"subscription_id": subscription_id}
    )
    assert installments.status_code == 200
    assert installments.json()[0]["status"] == "partial"
    assert installments.json()[0]["paid_amount"] == "25.00"

    too_large = admin_client.post(
        f"/api/abbonamenti/subscriptions/{subscription_id}/payments",
        json={"amount": "40.00"},
    )
    assert too_large.status_code == 422


def test_subscription_renewal_starts_after_previous_end(admin_client) -> None:
    plan = admin_client.post(
        "/api/abbonamenti/plans",
        json={"name": "Mensile rinnovo", "price": "30.00", "duration_days": 30},
    ).json()
    subscription = admin_client.post(
        "/api/abbonamenti/subscriptions",
        json={
            "member_id": 1,
            "plan_id": plan["id"],
            "starts_on": "2026-10-06",
            "ends_on": "2026-11-04",
        },
    ).json()

    renewal = admin_client.post(
        f"/api/abbonamenti/subscriptions/{subscription['id']}/renew", json={}
    )
    assert renewal.status_code == 201, renewal.text
    assert renewal.json()["starts_on"] == "2026-11-05"
    assert renewal.json()["ends_on"] == "2026-12-04"
