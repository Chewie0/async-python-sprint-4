"""DB creation2

Revision ID: d4f1b0958dac
Revises: 776553ba4212
Create Date: 2023-12-13 20:26:13.619556

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd4f1b0958dac'
down_revision: Union[str, None] = '776553ba4212'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('urls_original_url_key', 'urls', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('urls_original_url_key', 'urls', ['original_url'])
    # ### end Alembic commands ###