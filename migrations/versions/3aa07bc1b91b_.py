"""empty message

Revision ID: 3aa07bc1b91b
Revises: b5700abf848e
Create Date: 2023-02-01 23:37:12.384586

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3aa07bc1b91b'
down_revision = 'b5700abf848e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Products',
    sa.Column('user_id', sa.String(length=130), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('item_name', sa.String(length=500), nullable=False),
    sa.Column('item_price', sa.Integer(), nullable=False),
    sa.Column('item_description', sa.String(length=500), nullable=False),
    sa.Column('picture_path1', sa.String(length=500), nullable=False),
    sa.Column('filename1', sa.String(length=500), nullable=False),
    sa.Column('picture_path2', sa.String(length=500), nullable=True),
    sa.Column('filename2', sa.String(length=500), nullable=True),
    sa.Column('picture_path3', sa.String(length=500), nullable=True),
    sa.Column('filename3', sa.String(length=500), nullable=True),
    sa.Column('picture_path4', sa.String(length=500), nullable=True),
    sa.Column('filename4', sa.String(length=500), nullable=True),
    sa.Column('picture_path5', sa.String(length=500), nullable=True),
    sa.Column('filename5', sa.String(length=500), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['User.id'], ),
    sa.PrimaryKeyConstraint('product_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Products')
    # ### end Alembic commands ###
