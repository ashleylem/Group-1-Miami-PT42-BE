"""empty message

Revision ID: c1fc16d29771
Revises: 92e2a62ed8dd
Create Date: 2023-01-26 16:20:52.692643

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c1fc16d29771'
down_revision = '92e2a62ed8dd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Cart',
    sa.Column('user_id', sa.String(length=130), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('item_name', sa.String(length=500), nullable=False),
    sa.Column('item_price', sa.Integer(), nullable=False),
    sa.Column('item_description', sa.String(length=500), nullable=False),
    sa.Column('picture_url', sa.String(length=500), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['User.id'], ),
    sa.PrimaryKeyConstraint('product_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Cart')
    # ### end Alembic commands ###
