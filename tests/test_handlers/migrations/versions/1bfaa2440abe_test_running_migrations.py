"""test running migrations

Revision ID: 1bfaa2440abe
Revises: 7a459d1e8a8d
Create Date: 2023-09-06 16:35:36.498266

"""
from typing import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "1bfaa2440abe"
down_revision: Union[str, None] = "7a459d1e8a8d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
