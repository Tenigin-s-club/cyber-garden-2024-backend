"""empty message

Revision ID: 860c97cfdc76
Revises: 1bcba0b6f0fb
Create Date: 2024-11-23 18:33:00.673963

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '860c97cfdc76'
down_revision: Union[str, None] = '1bcba0b6f0fb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('whorehouse',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('office_id', sa.Integer(), nullable=False),
    sa.Column('inventory_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['inventory_id'], ['inventory.id'], ),
    sa.ForeignKeyConstraint(['office_id'], ['offices.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('whorehouse')
    # ### end Alembic commands ###