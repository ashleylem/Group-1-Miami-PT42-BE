"""empty message

Revision ID: bec9cff125cf
Revises: 7e2a2862ceb2
Create Date: 2023-01-18 01:37:57.609541

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bec9cff125cf'
down_revision = '7e2a2862ceb2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("user"),

    op.create_table("User",
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=80), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('Wishlist',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('item_name', sa.String(length=120), nullable=False),
    sa.Column('item_price', sa.Integer(), nullable=False),
    sa.Column('item_description', sa.String(length=500), nullable=False),
    sa.Column('picture_url', sa.String(length=500), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table("user",
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('email', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('password', sa.VARCHAR(length=80), autoincrement=False, nullable=False),
    sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='user_pkey'),
    sa.UniqueConstraint('email', name='user_email_key')
    )
    op.drop_table('Wishlist')
    op.drop_table('User')
    # ### end Alembic commands ###
