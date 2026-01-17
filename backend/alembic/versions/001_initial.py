"""Initial migration

Revision ID: 001
Create Date: 2026-01-17

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Users table
    op.create_table(
        'users',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('email', sa.String(255), unique=True, nullable=False, index=True),
        sa.Column('hashed_password', sa.String(255), nullable=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('photo_url', sa.String(500), nullable=True),
        sa.Column('bio', sa.String(500), nullable=True),
        sa.Column('training_level', sa.String(20), default='beginner'),
        sa.Column('visibility', sa.String(20), default='private'),
        sa.Column('oauth_provider', sa.String(50), nullable=True),
        sa.Column('oauth_id', sa.String(255), nullable=True),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('is_verified', sa.Boolean(), default=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )

    # Gyms table
    op.create_table(
        'gyms',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('name', sa.String(200), nullable=False, index=True),
        sa.Column('address', sa.String(500), nullable=False),
        sa.Column('latitude', sa.Float(), nullable=False),
        sa.Column('longitude', sa.Float(), nullable=False),
        sa.Column('phone', sa.String(50), nullable=True),
        sa.Column('website', sa.String(300), nullable=True),
        sa.Column('photo_url', sa.String(500), nullable=True),
        sa.Column('google_place_id', sa.String(100), unique=True, nullable=True),
        sa.Column('is_custom', sa.Boolean(), default=False),
        sa.Column('created_by_id', sa.String(36), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )

    # User favorite gyms
    op.create_table(
        'user_favorite_gyms',
        sa.Column('user_id', sa.String(36), sa.ForeignKey('users.id'), primary_key=True),
        sa.Column('gym_id', sa.String(36), sa.ForeignKey('gyms.id'), primary_key=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # Friendships table
    op.create_table(
        'friendships',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('requester_id', sa.String(36), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('addressee_id', sa.String(36), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('status', sa.String(20), default='pending'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )

    # Groups table
    op.create_table(
        'groups',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('description', sa.String(500), nullable=True),
        sa.Column('photo_url', sa.String(500), nullable=True),
        sa.Column('owner_id', sa.String(36), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('is_private', sa.Boolean(), default=True),
        sa.Column('max_members', sa.Integer(), default=50),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )

    # Sessions table
    op.create_table(
        'sessions',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('gym_id', sa.String(36), sa.ForeignKey('gyms.id'), nullable=False),
        sa.Column('scheduled_at', sa.DateTime(), nullable=False, index=True),
        sa.Column('duration_minutes', sa.Integer(), default=60),
        sa.Column('visibility', sa.String(20), default='friends'),
        sa.Column('group_id', sa.String(36), sa.ForeignKey('groups.id'), nullable=True),
        sa.Column('max_participants', sa.Integer(), nullable=True),
        sa.Column('creator_id', sa.String(36), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('is_recurring', sa.Boolean(), default=False),
        sa.Column('recurrence_rule', sa.String(100), nullable=True),
        sa.Column('is_cancelled', sa.Boolean(), default=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )

    # Session participants
    op.create_table(
        'session_participants',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('session_id', sa.String(36), sa.ForeignKey('sessions.id'), nullable=False),
        sa.Column('user_id', sa.String(36), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('rsvp_status', sa.String(20), default='going'),
        sa.Column('checked_in', sa.Boolean(), default=False),
        sa.Column('checked_in_at', sa.DateTime(), nullable=True),
        sa.Column('invited_by_id', sa.String(36), nullable=True),
        sa.Column('invite_message', sa.String(300), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # Session exercises
    op.create_table(
        'session_exercises',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('session_id', sa.String(36), sa.ForeignKey('sessions.id'), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('sets', sa.Integer(), nullable=True),
        sa.Column('reps', sa.String(50), nullable=True),
        sa.Column('duration_seconds', sa.Integer(), nullable=True),
        sa.Column('notes', sa.String(300), nullable=True),
        sa.Column('order', sa.Integer(), default=0),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('session_exercises')
    op.drop_table('session_participants')
    op.drop_table('sessions')
    op.drop_table('groups')
    op.drop_table('friendships')
    op.drop_table('user_favorite_gyms')
    op.drop_table('gyms')
    op.drop_table('users')
