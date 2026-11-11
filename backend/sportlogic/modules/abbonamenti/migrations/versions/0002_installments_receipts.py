"""add subscription installments and receipts"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "subscription_installments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "subscription_id",
            sa.Integer(),
            sa.ForeignKey("subscriptions.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("number", sa.Integer(), nullable=False),
        sa.Column("due_on", sa.Date(), nullable=False),
        sa.Column("amount", sa.Numeric(10, 2), nullable=False),
        sa.Column("paid_amount", sa.Numeric(10, 2), nullable=False, server_default="0"),
        sa.Column("status", sa.String(24), nullable=False, server_default="pending"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.UniqueConstraint("subscription_id", "number"),
    )
    op.create_index(
        "ix_subscription_installments_subscription_id",
        "subscription_installments",
        ["subscription_id"],
    )
    op.create_index("ix_subscription_installments_due_on", "subscription_installments", ["due_on"])
    op.create_index("ix_subscription_installments_status", "subscription_installments", ["status"])
    op.add_column(
        "subscription_payments",
        sa.Column("installment_id", sa.Integer(), nullable=True),
    )
    op.create_foreign_key(
        "fk_subscription_payments_installment_id",
        "subscription_payments",
        "subscription_installments",
        ["installment_id"],
        ["id"],
    )
    op.create_index("ix_subscription_payments_installment_id", "subscription_payments", ["installment_id"])
    op.create_table(
        "subscription_receipts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "payment_id",
            sa.Integer(),
            sa.ForeignKey("subscription_payments.id", ondelete="CASCADE"),
            nullable=False,
            unique=True,
        ),
        sa.Column("receipt_number", sa.String(64), nullable=False, unique=True),
        sa.Column("issued_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("amount", sa.Numeric(10, 2), nullable=False),
    )
    op.create_index("ix_subscription_receipts_payment_id", "subscription_receipts", ["payment_id"])
    op.create_index("ix_subscription_receipts_receipt_number", "subscription_receipts", ["receipt_number"])


def downgrade() -> None:
    op.drop_index("ix_subscription_receipts_receipt_number", table_name="subscription_receipts")
    op.drop_index("ix_subscription_receipts_payment_id", table_name="subscription_receipts")
    op.drop_table("subscription_receipts")
    op.drop_index("ix_subscription_payments_installment_id", table_name="subscription_payments")
    op.drop_constraint(
        "fk_subscription_payments_installment_id", "subscription_payments", type_="foreignkey"
    )
    op.drop_column("subscription_payments", "installment_id")
    op.drop_index("ix_subscription_installments_status", table_name="subscription_installments")
    op.drop_index("ix_subscription_installments_due_on", table_name="subscription_installments")
    op.drop_index(
        "ix_subscription_installments_subscription_id", table_name="subscription_installments"
    )
    op.drop_table("subscription_installments")
