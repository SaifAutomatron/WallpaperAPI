"""add phone number column to user table

Revision ID: f9ebc51cf6ce
Revises: 
Create Date: 2024-01-19 21:51:41.256963

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f9ebc51cf6ce'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('phone_number', sa.String(10), nullable=True))


def downgrade() -> None:
    pass
