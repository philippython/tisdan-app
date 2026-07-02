"""make bookings.user_id nullable

Revision ID: 3bf5a1b2c3d
Revises: 2ca0a4692434
Create Date: 2026-07-02 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3bf5a1b2c3d'
down_revision = '2ca0a4692434'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Make bookings.user_id nullable."""
    op.alter_column('bookings', 'user_id', existing_type=sa.Uuid(), nullable=True)


def downgrade() -> None:
    """Revert user_id to non-nullable."""
    op.alter_column('bookings', 'user_id', existing_type=sa.Uuid(), nullable=False)
