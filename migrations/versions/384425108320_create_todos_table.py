"""create todos table

Revision ID: 384425108320
Revises: f32fa0fe48d6
Create Date: 2024-07-21 14:35:42.478348

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '384425108320'
down_revision: Union[str, None] = 'f32fa0fe48d6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('todos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('state', sa.Enum('draft', 'todo', 'doing', 'done', 'trash', name='todostate'), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id']),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('todos')
