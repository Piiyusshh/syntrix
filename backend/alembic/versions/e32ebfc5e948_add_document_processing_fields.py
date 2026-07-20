"""add document processing fields

Revision ID: e32ebfc5e948
Revises: f78ce7ce2134
Create Date: 2026-07-20 18:54:30.809091

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e32ebfc5e948"
down_revision: Union[str, Sequence[str], None] = "f78ce7ce2134"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "documents",
        sa.Column(
            "extracted_text",
            sa.Text(),
            nullable=True,
        ),
    )

    op.add_column(
        "documents",
        sa.Column(
            "processing_status",
            sa.String(length=20),
            nullable=False,
            server_default="PENDING",
        ),
    )

    op.add_column(
        "documents",
        sa.Column(
            "processed_at",
            sa.DateTime(),
            nullable=True,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column("documents", "processed_at")
    op.drop_column("documents", "processing_status")
    op.drop_column("documents", "extracted_text")