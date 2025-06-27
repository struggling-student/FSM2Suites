"""Add trip status field

Revision ID: add_trip_status
Revises: 6ebe32e5abcb
Create Date: 2025-06-27 19:50:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'add_trip_status'
down_revision: Union[str, None] = '6ebe32e5abcb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add status column to trips table with default value
    op.add_column('trips', sa.Column('status', sa.String(), nullable=False, server_default='draft'))


def downgrade() -> None:
    # Remove status column from trips table
    op.drop_column('trips', 'status')
