"""encrypted medical certificate metadata"""

import sqlalchemy as sa
from alembic import op

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "medical_certificates",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("member_id", sa.Integer(), sa.ForeignKey("members.id"), nullable=False),
        sa.Column("original_filename", sa.String(255), nullable=False),
        sa.Column("storage_filename", sa.String(80), nullable=False, unique=True),
        sa.Column("content_type", sa.String(120), nullable=False),
        sa.Column("file_size", sa.Integer(), nullable=False),
        sa.Column("valid_from", sa.Date(), nullable=True),
        sa.Column("expires_on", sa.Date(), nullable=False),
        sa.Column("consent_confirmed", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_medical_certificates_member_id", "medical_certificates", ["member_id"])
    op.create_index("ix_medical_certificates_expires_on", "medical_certificates", ["expires_on"])


def downgrade() -> None:
    op.drop_index("ix_medical_certificates_expires_on", table_name="medical_certificates")
    op.drop_index("ix_medical_certificates_member_id", table_name="medical_certificates")
    op.drop_table("medical_certificates")
