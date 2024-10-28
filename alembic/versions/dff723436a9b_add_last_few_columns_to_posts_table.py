"""add last few columns to posts table

Revision ID: dff723436a9b
Revises: 247aa9f4ffcb
Create Date: 2024-10-28 16:30:28.415956

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dff723436a9b'
down_revision: Union[str, None] = '247aa9f4ffcb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", 
                  sa.Column("published", sa.Boolean(), nullable=False, server_default="TRUE"),
                  )
    op.add_column("posts",
                  sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")),
                  )
    pass


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
