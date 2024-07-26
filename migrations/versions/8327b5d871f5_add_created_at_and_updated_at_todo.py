"""Add created_at and updated_at todo

Revision ID: 8327b5d871f5
Revises: 384425108320
Create Date: 2024-07-23 13:41:46.961283

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8327b5d871f5'
down_revision: Union[str, None] = '384425108320'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# SQLite has limited support for modifying existing tables and setting default values using ALTER TABLE.
# In SQLite, you can't directly add a column with a default value or an ON UPDATE clause.

def upgrade():
    # Step 1: Create a new table with the new structure
    op.create_table(
        'todos_new',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('state', sa.Enum('draft', 'todo', 'doing', 'done', 'trash', name='todostate'), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False,
                  server_onupdate=sa.text('(CURRENT_TIMESTAMP)')),
    )

    # Step 2: Drop the old table
    op.drop_table('todos')

    # Step 3: Rename the new table to the old table's name
    op.rename_table('todos_new', 'todos')


def downgrade():
    # Step 1: Create the old table structure
    op.create_table('todos_old',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('state', sa.Enum('draft', 'todo', 'doing', 'done', 'trash', name='todostate'), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )

    # Step 2: Drop the new table
    op.drop_table('todos')

    # Step 3: Rename the old table back to its original name
    op.rename_table('todos_old', 'todos')
