"""test running migrations

Revision ID: 79683c6d5071
Revises: cb6d4e90fe31
Create Date: 2023-09-06 22:58:49.243819

"""
from typing import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "79683c6d5071"
down_revision: Union[str, None] = "cb6d4e90fe31"
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