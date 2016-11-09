"""empty message

Revision ID: d9d4879dcf22
Revises: None
Create Date: 2016-11-08 22:31:39.265437

"""

# revision identifiers, used by Alembic.
revision = 'd9d4879dcf22'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'password')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password', sa.VARCHAR(length=64), autoincrement=False, nullable=True))
    ### end Alembic commands ###
