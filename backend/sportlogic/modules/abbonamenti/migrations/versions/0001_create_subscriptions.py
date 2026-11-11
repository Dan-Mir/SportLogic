"""subscription plans, subscriptions and manual payments"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def _timestamps() -> list[sa.Column]:
    return [
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    ]


def upgrade() -> None:
    op.create_table(
        "subscription_plans",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(160), nullable=False),
        sa.Column("billing_type", sa.String(32), nullable=False, server_default="monthly"),
        sa.Column("price", sa.Numeric(10, 2), nullable=False),
        sa.Column("duration_days", sa.Integer(), nullable=False, server_default="30"),
        sa.Column("included_entries", sa.Integer(), nullable=True),
        sa.Column("auto_renew", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("notes", sa.Text(), nullable=True),
        *_timestamps(),
    )
    op.create_table(
        "subscriptions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("member_id", sa.Integer(), sa.ForeignKey("members.id"), nullable=False),
        sa.Column("plan_id", sa.Integer(), sa.ForeignKey("subscription_plans.id"), nullable=False),
        sa.Column("starts_on", sa.Date(), nullable=False),
        sa.Column("ends_on", sa.Date(), nullable=False),
        sa.Column("status", sa.String(24), nullable=False, server_default="active"),
        sa.Column("auto_renew", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("notes", sa.Text(), nullable=True),
        *_timestamps(),
    )
    op.create_index("ix_subscriptions_member_id", "subscriptions", ["member_id"])
    op.create_index("ix_subscriptions_plan_id", "subscriptions", ["plan_id"])
    op.create_index("ix_subscriptions_status", "subscriptions", ["status"])
    op.create_table(
        "subscription_payments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("subscription_id", sa.Integer(), sa.ForeignKey("subscriptions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("amount", sa.Numeric(10, 2), nullable=False),
        sa.Column("paid_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("method", sa.String(32), nullable=False, server_default="cash"),
        sa.Column("reference", sa.String(120), nullable=True),
        sa.Column("status", sa.String(24), nullable=False, server_default="completed"),
        sa.Column("notes", sa.Text(), nullable=True),
    )
    op.create_index("ix_subscription_payments_subscription_id", "subscription_payments", ["subscription_id"])


def downgrade() -> None:
    op.drop_index("ix_subscription_payments_subscription_id", table_name="subscription_payments")
    op.drop_table("subscription_payments")
    op.drop_index("ix_subscriptions_status", table_name="subscriptions")
    op.drop_index("ix_subscriptions_plan_id", table_name="subscriptions")
    op.drop_index("ix_subscriptions_member_id", table_name="subscriptions")
    op.drop_table("subscriptions")
    op.drop_table("subscription_plans")
