"""add 'hidden' column to app_variants table

Revision ID: 7cc66fc40298
Revises: 6161b674688d
Create Date: 2025-03-27 14:40:47.770949

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "7cc66fc40298"
down_revision: Union[str, None] = "6161b674688d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("app_variants", sa.Column("hidden", sa.Boolean(), nullable=True))
    op.add_column(
        "app_variant_revisions", sa.Column("hidden", sa.Boolean(), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("app_variants", "hidden")
    op.drop_column("app_variant_revisions", "hidden")
    # ### end Alembic commands ###
