"""add content column to posts table'

Revision ID: bcb633534940
Revises: 5f3d8c6e3272
Create Date: 2024-10-28 16:06:35.105294

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bcb633534940'
down_revision: Union[str, None] = '5f3d8c6e3272'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
