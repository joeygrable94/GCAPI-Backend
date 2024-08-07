"""updated table tracking_link with url_hash column

Revision ID: 4d5d93c6db26
Revises: 079ba740b9e5
Create Date: 2024-08-06 13:17:42.374043

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql

from app.db.custom_types.longtext import LongText  # type: ignore

# revision identifiers, used by Alembic.
revision = '4d5d93c6db26'
down_revision = '079ba740b9e5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('client_report', 'keys',
               existing_type=mysql.LONGBLOB(),
               type_=LongText(),
               existing_nullable=True)
    op.alter_column('go_sc_country', 'keys',
               existing_type=mysql.LONGBLOB(),
               type_=LongText(),
               existing_nullable=False)
    op.alter_column('go_sc_device', 'keys',
               existing_type=mysql.LONGBLOB(),
               type_=LongText(),
               existing_nullable=False)
    op.alter_column('go_sc_page', 'keys',
               existing_type=mysql.LONGBLOB(),
               type_=LongText(),
               existing_nullable=False)
    op.alter_column('go_sc_query', 'keys',
               existing_type=mysql.LONGBLOB(),
               type_=LongText(),
               existing_nullable=False)
    op.alter_column('go_sc_searchappearance', 'keys',
               existing_type=mysql.LONGBLOB(),
               type_=LongText(),
               existing_nullable=False)
    op.alter_column('tracking_link', 'url_hash',
               existing_type=mysql.VARCHAR(length=32),
               type_=sa.String(length=64),
               existing_nullable=False)
    op.alter_column('website_keywordcorpus', 'corpus',
               existing_type=mysql.LONGBLOB(),
               type_=LongText(),
               existing_nullable=False)
    op.alter_column('website_keywordcorpus', 'rawtext',
               existing_type=mysql.LONGBLOB(),
               type_=LongText(),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('website_keywordcorpus', 'rawtext',
               existing_type=LongText(),
               type_=mysql.LONGBLOB(),
               existing_nullable=False)
    op.alter_column('website_keywordcorpus', 'corpus',
               existing_type=LongText(),
               type_=mysql.LONGBLOB(),
               existing_nullable=False)
    op.alter_column('tracking_link', 'url_hash',
               existing_type=sa.String(length=64),
               type_=mysql.VARCHAR(length=32),
               existing_nullable=False)
    op.alter_column('go_sc_searchappearance', 'keys',
               existing_type=LongText(),
               type_=mysql.LONGBLOB(),
               existing_nullable=False)
    op.alter_column('go_sc_query', 'keys',
               existing_type=LongText(),
               type_=mysql.LONGBLOB(),
               existing_nullable=False)
    op.alter_column('go_sc_page', 'keys',
               existing_type=LongText(),
               type_=mysql.LONGBLOB(),
               existing_nullable=False)
    op.alter_column('go_sc_device', 'keys',
               existing_type=LongText(),
               type_=mysql.LONGBLOB(),
               existing_nullable=False)
    op.alter_column('go_sc_country', 'keys',
               existing_type=LongText(),
               type_=mysql.LONGBLOB(),
               existing_nullable=False)
    op.alter_column('client_report', 'keys',
               existing_type=LongText(),
               type_=mysql.LONGBLOB(),
               existing_nullable=True)
    # ### end Alembic commands ###
