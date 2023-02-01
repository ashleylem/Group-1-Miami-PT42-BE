"""empty message

Revision ID: dbb21ae9dd45
Revises: 03c0125175f8
Create Date: 2023-01-25 22:31:50.434029

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dbb21ae9dd45'
down_revision = '03c0125175f8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('VideoUploads',
    sa.Column('user_id', sa.String(length=130), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('video_id', sa.Integer(), nullable=False),
    sa.Column('video_name', sa.String(length=500), nullable=False),
    sa.Column('video_description', sa.String(length=500), nullable=False),
    sa.Column('picture_url', sa.String(length=500), nullable=False),
    sa.Column('video_path', sa.String(length=500), nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['Wishlist.product_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['User.id'], ),
    sa.PrimaryKeyConstraint('video_id')
    )
    with op.batch_alter_table('Wishlist', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['product_id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Wishlist', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    op.drop_table('VideoUploads')
    # ### end Alembic commands ###