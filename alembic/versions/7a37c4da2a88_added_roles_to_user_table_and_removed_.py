"""added roles to user table and removed LONGTEXT to pass sqlite tests

Revision ID: 7a37c4da2a88
Revises: 8d2203595f7e
Create Date: 2023-09-21 17:06:50.116644

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '7a37c4da2a88'
down_revision = '8d2203595f7e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('roles', sa.JSON(), nullable=False))
    op.alter_column('website_keywordcorpus', 'corpus',
               existing_type=mysql.LONGTEXT(),
               type_=sa.Text(length=4000000000),
               existing_nullable=False)
    op.alter_column('website_keywordcorpus', 'rawtext',
               existing_type=mysql.LONGTEXT(),
               type_=sa.Text(length=4000000000),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('website_keywordcorpus', 'rawtext',
               existing_type=sa.Text(length=4000000000),
               type_=mysql.LONGTEXT(),
               existing_nullable=False)
    op.alter_column('website_keywordcorpus', 'corpus',
               existing_type=sa.Text(length=4000000000),
               type_=mysql.LONGTEXT(),
               existing_nullable=False)
    op.drop_column('user', 'roles')
    # ### end Alembic commands ###
