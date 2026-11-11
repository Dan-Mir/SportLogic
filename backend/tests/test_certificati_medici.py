from __future__ import annotations

import os

os.environ["SPORTLOGIC_DATABASE_URL"] = "sqlite+pysqlite:///:memory:"
os.environ["SPORTLOGIC_MODULES_ENABLED"] = "core,anagrafica,certificati_medici"

import pytest
from fastapi.testclient import TestClient

import sportlogic.db as db
from sportlogic.config import get_settings
from sportlogic.db import Base
from sportlogic.main import create_app
from sportlogic.modules.anagrafica.models import Member
from sportlogic.modules.core.models import User
from sportlogic.modules.core.security import hash_password


@pytest.fixture()
def admin_client(tmp_path):
    db._engine = None
    db._session_factory = None
    get_settings.cache_clear()
    Base.metadata.create_all(db.get_engine())
    get_settings().document_storage_path = str(tmp_path)
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


def test_certificate_is_encrypted_and_downloadable(admin_client) -> None:
    upload = admin_client.post(
        "/api/certificati-medici",
        data={
            "member_id": "1",
            "valid_from": "2026-01-01",
            "expires_on": "2027-01-01",
            "consent_confirmed": "true",
        },
        files={"file": ("certificato.txt", b"dato sanitario", "text/plain")},
    )
    assert upload.status_code == 201, upload.text
    certificate_id = upload.json()["id"]

    downloaded = admin_client.get(f"/api/certificati-medici/{certificate_id}/download")
    assert downloaded.status_code == 200
    assert downloaded.content == b"dato sanitario"
