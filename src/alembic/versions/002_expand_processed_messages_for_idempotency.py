"""expand processed_messages for idempotency lifecycle

Revision ID: 002_expand_processed_messages_for_idempotency
Revises: 001_create_outbox_messages
Create Date: 2026-02-19
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "002_expand_processed_messages_for_idempotency"
down_revision: Union[str, None] = "001_create_outbox_messages"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "processed_messages",
        sa.Column("status", sa.String(length=20), nullable=False, server_default=sa.text("'processing'")),
    )
    op.add_column(
        "processed_messages",
        sa.Column(
            "first_seen_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
    )
    op.add_column(
        "processed_messages",
        sa.Column("last_error", sa.String(length=2000), nullable=True),
    )
    op.add_column(
        "processed_messages",
        sa.Column("attempt_count", sa.Integer(), nullable=False, server_default=sa.text("1")),
    )
    op.alter_column("processed_messages", "processed_at", existing_type=sa.DateTime(timezone=True), nullable=True)


def downgrade() -> None:
    op.execute(
        sa.text(
            """
            UPDATE processed_messages
            SET processed_at = COALESCE(processed_at, CURRENT_TIMESTAMP)
            """
        )
    )
    op.alter_column("processed_messages", "processed_at", existing_type=sa.DateTime(timezone=True), nullable=False)
    op.drop_column("processed_messages", "attempt_count")
    op.drop_column("processed_messages", "last_error")
    op.drop_column("processed_messages", "first_seen_at")
    op.drop_column("processed_messages", "status")
