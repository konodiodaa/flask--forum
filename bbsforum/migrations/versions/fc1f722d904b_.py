"""empty message

Revision ID: fc1f722d904b
Revises: 83cb8ea8512f
Create Date: 2019-12-07 21:32:49.619966

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fc1f722d904b'
down_revision = '83cb8ea8512f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('avatar', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'avatar')
    # ### end Alembic commands ###
