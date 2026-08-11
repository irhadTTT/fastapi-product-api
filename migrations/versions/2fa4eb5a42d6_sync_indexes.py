"""sync indexes

Revision ID: 2fa4eb5a42d6
Revises: 9a8c2e0bc54d
Create Date: 2026-08-11 15:43:12.807137

"""

from collections.abc import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "2fa4eb5a42d6"
down_revision: str | Sequence[str] | None = "9a8c2e0bc54d"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
