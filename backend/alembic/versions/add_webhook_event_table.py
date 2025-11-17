"""Add webhook_event table for idempotency tracking

Revision ID: add_webhook_event_001
Revises: add_yearly_prepay_001
Create Date: 2025-11-17 10:00:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import uuid


# revision identifiers, used by Alembic.
revision = 'add_webhook_event_001'
down_revision = 'add_yearly_prepay_001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create webhook_event table for tracking processed webhook events
    op.create_table(
        'webhook_event',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('modified_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('stripe_event_id', sa.String(length=255), nullable=False, unique=True),
        sa.Column('event_type', sa.String(length=255), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('processed_at', sa.DateTime(), nullable=False),
        sa.Column('error_message', sa.String(), nullable=True),
    )

    # Create indexes
    op.create_index('ix_webhook_event_stripe_event_id', 'webhook_event', ['stripe_event_id'], unique=True)
    op.create_index('ix_webhook_event_status', 'webhook_event', ['status'])


def downgrade() -> None:
    # Drop indexes
    op.drop_index('ix_webhook_event_status', table_name='webhook_event')
    op.drop_index('ix_webhook_event_stripe_event_id', table_name='webhook_event')

    # Drop table
    op.drop_table('webhook_event')
