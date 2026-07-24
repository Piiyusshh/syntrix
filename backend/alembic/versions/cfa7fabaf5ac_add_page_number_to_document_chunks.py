"""add page_number to document_chunks

Revision ID: cfa7fabaf5ac
Revises: 825cc908e540
Create Date: 2026-07-22 22:38:18.337788

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "cfa7fabaf5ac"
down_revision: Union[str, Sequence[str], None] = "825cc908e540"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # Step 1: Add nullable column
    op.add_column(
        "document_chunks",
        sa.Column(
            "page_number",
            sa.Integer(),
            nullable=True,
        ),
    )

    # Step 2: Populate existing rows
    op.execute(
        "UPDATE document_chunks SET page_number = 1"
    )

    # Step 3: Make column NOT NULL
    op.alter_column(
        "document_chunks",
        "page_number",
        nullable=False,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column(
        "document_chunks",
        "page_number",
    )