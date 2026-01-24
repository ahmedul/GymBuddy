"""Add notification tokens table

Revision ID: 002
Create Date: 2026-01-24

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '002'
down_revision: Union[str, None] = '001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Notification tokens table
    op.create_table(
        'notification_tokens',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('user_id', sa.String(36), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('token', sa.String(500), nullable=False, unique=True),
        sa.Column('device_type', sa.String(20), nullable=True),  # 'ios', 'android', 'web'
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_notification_tokens_user_id', 'notification_tokens', ['user_id'])
    op.create_index('ix_notification_tokens_token', 'notification_tokens', ['token'])

    # Add notification preferences to users
    op.add_column('users', sa.Column('notify_session_invites', sa.Boolean(), server_default='true'))
    op.add_column('users', sa.Column('notify_friend_requests', sa.Boolean(), server_default='true'))
    op.add_column('users', sa.Column('notify_session_reminders', sa.Boolean(), server_default='true'))


def downgrade() -> None:
    op.drop_column('users', 'notify_session_reminders')
    op.drop_column('users', 'notify_friend_requests')
    op.drop_column('users', 'notify_session_invites')
    op.drop_index('ix_notification_tokens_token')
    op.drop_index('ix_notification_tokens_user_id')
    op.drop_table('notification_tokens')
