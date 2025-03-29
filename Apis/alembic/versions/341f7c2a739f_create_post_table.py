"""create post table

Revision ID: 341f7c2a739f
Revises: d80a20b5dc1f
Create Date: 2025-03-25 23:09:42.637619

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '341f7c2a739f'
down_revision: Union[str, None] = 'd80a20b5dc1f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
