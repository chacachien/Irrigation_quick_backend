"""script

Revision ID: 1aadfaa8e8d6
Revises: e4863e18141c
Create Date: 2024-05-23 17:08:42.632033

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel 


# revision identifiers, used by Alembic.
revision: str = '1aadfaa8e8d6'
down_revision: Union[str, None] = 'e4863e18141c'
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
