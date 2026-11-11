"""members, staff, families tables

Revision ID: 0001
Revises:
Create Date: 2026-08-27
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def _timestamps() -> list[sa.Column]:
    return [
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    ]


def upgrade() -> None:
    op.create_table(
        "members",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("first_name", sa.String(length=120), nullable=False),
        sa.Column("last_name", sa.String(length=120), nullable=False),
        sa.Column("fiscal_code", sa.String(length=16), nullable=True),
        sa.Column("birth_date", sa.Date(), nullable=True),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("phone", sa.String(length=32), nullable=True),
        sa.Column("address", sa.String(length=255), nullable=True),
        sa.Column("city", sa.String(length=120), nullable=True),
        sa.Column("province", sa.String(length=8), nullable=True),
        sa.Column("postal_code", sa.String(length=8), nullable=True),
        sa.Column("gdpr_consent", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        *_timestamps(),
        sa.UniqueConstraint("fiscal_code"),
    )
    op.create_index("ix_members_fiscal_code", "members", ["fiscal_code"])

    op.create_table(
        "staff",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("first_name", sa.String(length=120), nullable=False),
        sa.Column("last_name", sa.String(length=120), nullable=False),
        sa.Column("role", sa.String(length=64), nullable=False, server_default="istruttore"),
        sa.Column("qualifications", sa.Text(), nullable=True),
        sa.Column("certifications", sa.Text(), nullable=True),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("phone", sa.String(length=32), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        *_timestamps(),
    )

    op.create_table(
        "families",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        *_timestamps(),
    )

    op.create_table(
        "family_members",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "family_id",
            sa.Integer(),
            sa.ForeignKey("families.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "member_id",
            sa.Integer(),
            sa.ForeignKey("members.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("relation", sa.String(length=64), nullable=False, server_default="figlio"),
        *_timestamps(),
    )


def downgrade() -> None:
    op.drop_table("family_members")
    op.drop_table("families")
    op.drop_table("staff")
    op.drop_index("ix_members_fiscal_code", table_name="members")
    op.drop_table("members")
