"""updated website keyword tables and username in user table

Revision ID: 8d2203595f7e
Revises: 4bb1a741a074
Create Date: 2023-09-21 16:12:54.683735

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '8d2203595f7e'
down_revision = '4bb1a741a074'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
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
    # ### end Alembic commands ###