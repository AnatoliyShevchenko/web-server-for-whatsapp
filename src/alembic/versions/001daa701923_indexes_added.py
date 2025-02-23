"""indexes added

Revision ID: 001daa701923
Revises: 624e222e180a
Create Date: 2024-07-30 19:15:31.635594

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '001daa701923'
down_revision: Union[str, None] = '624e222e180a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_clients_wa_id'), 'clients', ['wa_id'], unique=False)
    op.create_index(op.f('ix_clients_wa_number'), 'clients', ['wa_number'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_clients_wa_number'), table_name='clients')
    op.drop_index(op.f('ix_clients_wa_id'), table_name='clients')
    # ### end Alembic commands ###
