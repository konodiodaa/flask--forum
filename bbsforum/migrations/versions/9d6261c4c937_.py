"""empty message

Revision ID: 9d6261c4c937
Revises: fc1f722d904b
Create Date: 2019-12-07 22:18:49.541670

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '9d6261c4c937'
down_revision = 'fc1f722d904b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('photo', sa.String(length=100), nullable=True))
    op.drop_column('user', 'avatar')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('avatar', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_column('user', 'photo')
    # ### end Alembic commands ###
