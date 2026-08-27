from __future__ import annotations

import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

# Forza SQLite in memoria prima di importare moduli che toccano il DB.
os.environ["ARENA_DATABASE_URL"] = "sqlite+pysqlite:///:memory:"

from arena.db import Base  # noqa: E402
from arena.modules.anagrafica.models import Family, Member  # noqa: E402
from arena.modules.core.models import User  # noqa: E402
from arena.modules.core.security import hash_password  # noqa: E402


@pytest.fixture()
def session():
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    s = sessionmaker(bind=engine)()
    yield s
    s.close()


def test_create_member(session) -> None:
    member = Member(first_name="Mario", last_name="Rossi", fiscal_code="RSSMRA80A01H501U")
    session.add(member)
    session.commit()
    assert member.id is not None


def test_member_fiscal_code_unique(session) -> None:
    session.add(Member(first_name="A", last_name="B", fiscal_code="CF1"))
    session.commit()
    session.add(Member(first_name="C", last_name="D", fiscal_code="CF1"))
    with pytest.raises(IntegrityError):
        session.commit()


def test_user_role_default(session) -> None:
    user = User(email="a@b.it", hashed_password=hash_password("x"), full_name="A B")
    session.add(user)
    session.commit()
    assert user.role == "reception"


def test_family_relation(session) -> None:
    member = Member(first_name="M", last_name="R")
    family = Family(name="Famiglia Rossi")
    session.add_all([member, family])
    session.flush()
    from arena.modules.anagrafica.models import FamilyMember

    family.members.append(FamilyMember(member_id=member.id, relation="figlio"))
    session.commit()
    assert len(family.members) == 1
