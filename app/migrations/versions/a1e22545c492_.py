"""empty message

Revision ID: a1e22545c492
Revises: 2b83d3332ba3
Create Date: 2024-11-23 04:16:47.768681

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1e22545c492'
down_revision: Union[str, None] = '2b83d3332ba3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('map', sa.Column('x', sa.Integer(), nullable=False))
    op.add_column('map', sa.Column('y', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('map', 'y')
    op.drop_column('map', 'x')
    # ### end Alembic commands ###
