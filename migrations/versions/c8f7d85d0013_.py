"""empty message

Revision ID: c8f7d85d0013
Revises: 9831467bd304
Create Date: 2023-01-26 01:03:03.529681

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c8f7d85d0013'
down_revision = '9831467bd304'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('VideoUploads', schema=None) as batch_op:
        batch_op.drop_column('picture_url')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('VideoUploads', schema=None) as batch_op:
        batch_op.add_column(sa.Column('picture_url', sa.VARCHAR(length=500), autoincrement=False, nullable=False))

    # ### end Alembic commands ###
