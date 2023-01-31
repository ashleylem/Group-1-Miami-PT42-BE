"""empty message

Revision ID: c4dda8b894ea
Revises: b068f49805d8
Create Date: 2023-01-31 17:52:07.002160

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c4dda8b894ea'
down_revision = 'b068f49805d8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('VideoUploads', schema=None) as batch_op:
        batch_op.add_column(sa.Column('picture_url', sa.String(length=500), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('VideoUploads', schema=None) as batch_op:
        batch_op.drop_column('picture_url')

    # ### end Alembic commands ###
