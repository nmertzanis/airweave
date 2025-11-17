"""Webhook event model for idempotency tracking."""

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.schema import Index

from airweave.models._base import Base


class WebhookEvent(Base):
    """Tracks processed webhook events for idempotency.

    Stripe webhooks may be retried multiple times. This model
    ensures we process each event exactly once by tracking
    the event ID.
    """

    __tablename__ = "webhook_event"

    # Stripe event ID (e.g., "evt_1234567890")
    stripe_event_id: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    # Event type (e.g., "customer.subscription.created")
    event_type: Mapped[str] = mapped_column(String(255), nullable=False)

    # Processing status
    status: Mapped[str] = mapped_column(String(50), nullable=False)  # processed, failed

    # When the event was processed
    processed_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False)

    # Error message if processing failed
    error_message: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    __table_args__ = (
        # Index for efficient lookups by event ID
        Index("ix_webhook_event_stripe_event_id", "stripe_event_id", unique=True),
        # Index for querying by status
        Index("ix_webhook_event_status", "status"),
    )
