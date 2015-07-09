"""Create User Table

Revision ID: 300eb7b9958
Revises: None
Create Date: 2015-07-09 14:33:27.228463

"""

# revision identifiers, used by Alembic.
revision = '300eb7b9958'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=True),
        sa.Column('username', sa.String(length=200), nullable=True),
        sa.Column('email', sa.String(length=200), nullable=True),
        sa.Column('user_id', sa.String(length=255), nullable=True),
        sa.Column('provider', sa.String(length=255), nullable=True),
        sa.Column('picture', sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('provider'),
        sa.UniqueConstraint('user_id')
    )


def downgrade():
    op.drop_table('users')
