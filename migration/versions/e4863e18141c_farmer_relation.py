"""farmer relation

Revision ID: e4863e18141c
Revises: bf34d1d99d91
Create Date: 2024-05-21 08:32:56.522911

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = 'e4863e18141c'
down_revision: Union[str, None] = 'bf34d1d99d91'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # op.alter_column('reader', 'username',
    #            existing_type=sa.VARCHAR(),
    #            nullable=False)
    # ### end Alembic commands ###
    pass


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # op.alter_column('reader', 'username',
    #            existing_type=sa.VARCHAR(),
    #            nullable=True)
    # ### end Alembic commands ###
    pass
