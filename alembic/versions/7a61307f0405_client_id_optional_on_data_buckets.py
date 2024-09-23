"""client_id optional on data_buckets

Revision ID: 7a61307f0405
Revises: 84d3e3934aca
Create Date: 2024-09-12 15:58:35.229497

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '7a61307f0405'
down_revision = '84d3e3934aca'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('data_bucket', 'client_id',
               existing_type=mysql.CHAR(length=32),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    op.alter_column('data_bucket', 'client_id',
               existing_type=mysql.CHAR(length=32),
               nullable=False)
    # ### end Alembic commands ###