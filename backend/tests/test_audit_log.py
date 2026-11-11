from __future__ import annotations

import os

os.environ["SPORTLOGIC_DATABASE_URL"] = "sqlite+pysqlite:///:memory:"
os.environ["SPORTLOGIC_MODULES_ENABLED"] = "core,anagrafica"

import pytest
from fastapi.testclient import TestClient

import sportlogic.db as db
from sportlogic.db import Base
from sportlogic.main import create_app
from sportlogic.modules.core.models import AuditLog, User
from sportlogic.modules.core.security import hash_password


@pytest.fixture()
def client():
    db._engine = None
    db._session_factory = None
    Base.metadata.create_all(db.get_engine())
    app = create_app()
    with TestClient(app) as c:
        yield c


def _session():
    from sqlalchemy.orm import sessionmaker

    return sessionmaker(bind=db.get_engine())()


def _login(client, email="admin@test.it", password="password") -> str:
    r = client.post("/api/core/auth/login", json={"email": email, "password": password})
    assert r.status_code == 200, r.text
    return r.json()["access_token"]


def _setup_admin(client):
    session = _session()
    session.add(
        User(
            email="admin@test.it",
            hashed_password=hash_password("password"),
            full_name="Admin Test",
            role="admin",
        )
    )
    session.commit()
    session.close()


def test_login_creates_audit_log(client) -> None:
    _setup_admin(client)
    client.post("/api/core/auth/login", json={"email": "admin@test.it", "password": "password"})
    session = _session()
    entries = session.query(AuditLog).all()
    session.close()
    assert len(entries) >= 1
    login_entries = [e for e in entries if e.action == "login"]
    assert len(login_entries) >= 1


def test_create_user_creates_audit_log(client) -> None:
    _setup_admin(client)
    token = _login(client)
    client.post(
        "/api/core/users",
        json={"email": "nuovo@test.it", "password": "x", "full_name": "Nuovo", "role": "reception"},
        headers={"Authorization": f"Bearer {token}"},
    )
    session = _session()
    entries = session.query(AuditLog).filter(AuditLog.action == "user.create").all()
    session.close()
    assert len(entries) == 1
    assert entries[0].resource == "user"


def test_branding_update_creates_audit_log(client) -> None:
    _setup_admin(client)
    token = _login(client)
    client.put(
        "/api/core/branding",
        json={"brand_name": "Test Brand", "brand_primary_color": "#123456"},
        headers={"Authorization": f"Bearer {token}"},
    )
    session = _session()
    entries = session.query(AuditLog).filter(AuditLog.action == "branding.update").all()
    session.close()
    assert len(entries) == 1
    assert entries[0].resource_id == "global"


def test_member_create_creates_audit_log(client) -> None:
    _setup_admin(client)
    token = _login(client)
    client.post(
        "/api/anagrafica/members",
        json={"first_name": "Mario", "last_name": "Rossi", "fiscal_code": "RSSMRA80A01H501U"},
        headers={"Authorization": f"Bearer {token}"},
    )
    session = _session()
    entries = session.query(AuditLog).filter(AuditLog.action == "member.create").all()
    session.close()
    assert len(entries) == 1
    assert entries[0].resource == "member"
