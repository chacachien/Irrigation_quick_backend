"""update password

Revision ID: 30fb7beb83d9
Revises: 15826a471bda
Create Date: 2024-04-22 11:21:13.754302

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel 


# revision identifiers, used by Alembic.
revision: str = '30fb7beb83d9'
down_revision: Union[str, None] = '15826a471bda'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reader', sa.Column('username', sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    op.add_column('reader', sa.Column('hashed_password', sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    op.alter_column('reader', 'email',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('reader', 'email',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_column('reader', 'hashed_password')
    op.drop_column('reader', 'username')
    # ### end Alembic commands ###
