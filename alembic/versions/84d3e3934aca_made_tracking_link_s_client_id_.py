"""made tracking link's client_id relationship optional

Revision ID: 84d3e3934aca
Revises: 5ad33d8352c3
Create Date: 2024-09-12 15:33:24.298998

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "84d3e3934aca"
down_revision = "5ad33d8352c3"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "tracking_link", "client_id", existing_type=sa.CHAR(length=32), nullable=True
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "tracking_link", "client_id", existing_type=sa.CHAR(length=32), nullable=False
    )
    # ### end Alembic commands ###
