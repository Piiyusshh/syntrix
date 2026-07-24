"""add_document_summary

Revision ID: c7dd1164411d
Revises: cfa7fabaf5ac
Create Date: 2026-07-24 16:41:59.164139

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c7dd1164411d"
down_revision: Union[str, Sequence[str], None] = "cfa7fabaf5ac"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "documents",
        sa.Column(
            "summary",
            sa.Text(),
            nullable=True,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column(
        "documents",
        "summary",
    )