"""empty message

Revision ID: 7df8b60df075
Revises: c1e4522427c6
Create Date: 2023-01-26 00:35:08.195891

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7df8b60df075'
down_revision = 'c1e4522427c6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('VideoUploads', schema=None) as batch_op:
        batch_op.alter_column('product_id',
               existing_type=sa.VARCHAR(length=130),
               type_=sa.Integer(),
               existing_nullable=False)
        batch_op.alter_column('video_id',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=130),
               existing_nullable=False,
               existing_server_default=sa.text('nextval(\'"VideoUploads_video_id_seq"\'::regclass)'))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('VideoUploads', schema=None) as batch_op:
        batch_op.alter_column('video_id',
               existing_type=sa.String(length=130),
               type_=sa.INTEGER(),
               existing_nullable=False,
               existing_server_default=sa.text('nextval(\'"VideoUploads_video_id_seq"\'::regclass)'))
        batch_op.alter_column('product_id',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(length=130),
               existing_nullable=False)

    # ### end Alembic commands ###
