"""empty message

Revision ID: 7c8371c33943
Revises: 1bdbe89ed72c
Create Date: 2023-01-19 01:02:21.163112

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7c8371c33943'
down_revision = '1bdbe89ed72c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('User', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(length=120), nullable=False))
        batch_op.alter_column('id',
               existing_type=sa.VARCHAR(length=120),
               type_=sa.String(length=130),
               existing_nullable=False,
               existing_server_default=sa.text('nextval(\'"User_id_seq"\'::regclass)'))
        batch_op.drop_constraint('User_first_name_key', type_='unique')
        batch_op.drop_constraint('User_last_name_key', type_='unique')
        batch_op.drop_column('last_name')
        batch_op.drop_column('first_name')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('User', schema=None) as batch_op:
        batch_op.add_column(sa.Column('first_name', sa.VARCHAR(length=120), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('last_name', sa.VARCHAR(length=120), autoincrement=False, nullable=False))
        batch_op.create_unique_constraint('User_last_name_key', ['last_name'])
        batch_op.create_unique_constraint('User_first_name_key', ['first_name'])
        batch_op.alter_column('id',
               existing_type=sa.String(length=130),
               type_=sa.VARCHAR(length=120),
               existing_nullable=False,
               existing_server_default=sa.text('nextval(\'"User_id_seq"\'::regclass)'))
        batch_op.drop_column('name')

    # ### end Alembic commands ###