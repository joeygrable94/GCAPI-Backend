"""added data_bucket bdx_feed and gcflytour rel

Revision ID: c8a2683f41b6
Revises: 878fb66794d9
Create Date: 2024-05-11 18:07:35.976703

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql
from sqlalchemy_utils.types.uuid import UUIDType  # type: ignore

# revision identifiers, used by Alembic.
revision = 'c8a2683f41b6'
down_revision = '878fb66794d9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('client', sa.Column('slug', sa.String(length=64), nullable=False))
    op.create_index(op.f('ix_client_slug'), 'client', ['slug'], unique=True)
    op.add_column('data_bucket', sa.Column('bdx_feed_id', UUIDType(binary=False), nullable=True))
    op.add_column('data_bucket', sa.Column('gcft_id', UUIDType(binary=False), nullable=True))
    op.create_foreign_key(None, 'data_bucket', 'gcft', ['gcft_id'], ['id'])
    op.create_foreign_key(None, 'data_bucket', 'bdx_feed', ['bdx_feed_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'data_bucket', type_='foreignkey')  # type: ignore
    op.drop_constraint(None, 'data_bucket', type_='foreignkey')  # type: ignore
    op.drop_column('data_bucket', 'gcft_id')
    op.drop_column('data_bucket', 'bdx_feed_id')
    op.drop_index(op.f('ix_client_slug'), table_name='client')
    op.drop_column('client', 'slug')
    # ### end Alembic commands ###
