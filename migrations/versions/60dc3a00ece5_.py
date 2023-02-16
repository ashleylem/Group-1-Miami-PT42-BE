"""empty message

Revision ID: 60dc3a00ece5
Revises: 85c6ff2c8bf9
Create Date: 2023-02-13 15:52:34.004178

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '60dc3a00ece5'
down_revision = '85c6ff2c8bf9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Products', schema=None) as batch_op:
        batch_op.add_column(sa.Column('seller_name', sa.String(length=130), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Products', schema=None) as batch_op:
        batch_op.drop_column('seller_name')

    # ### end Alembic commands ###