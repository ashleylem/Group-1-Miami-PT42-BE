"""empty message

Revision ID: d5af53690527
Revises: 6617cf1b21c9
Create Date: 2023-02-04 00:14:03.674447

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd5af53690527'
down_revision = '6617cf1b21c9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('User', schema=None) as batch_op:
        batch_op.add_column(sa.Column('picture_filename', sa.String(length=500), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('User', schema=None) as batch_op:
        batch_op.drop_column('picture_filename')

    # ### end Alembic commands ###