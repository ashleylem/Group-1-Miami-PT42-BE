"""empty message

Revision ID: 3a35ab893854
Revises: 2c17f8136552
Create Date: 2023-01-25 23:35:52.273126

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3a35ab893854'
down_revision = '2c17f8136552'
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
    sa.ForeignKeyConstraint(['user_id'], ['User.id'], ),
    sa.PrimaryKeyConstraint('video_id'),
    sa.UniqueConstraint('product_id')
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
