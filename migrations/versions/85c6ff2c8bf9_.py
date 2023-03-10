"""empty message

Revision ID: 85c6ff2c8bf9
Revises: c3ab81b31cae
Create Date: 2023-02-08 21:48:17.182284

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '85c6ff2c8bf9'
down_revision = 'c3ab81b31cae'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Products', schema=None) as batch_op:
        batch_op.alter_column('sizes',
               existing_type=sa.VARCHAR(length=10),
               type_=sa.String(length=120),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Products', schema=None) as batch_op:
        batch_op.alter_column('sizes',
               existing_type=sa.String(length=120),
               type_=sa.VARCHAR(length=10),
               existing_nullable=True)

    # ### end Alembic commands ###
