"""CRUD operations for WebhookEvent model."""

from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from airweave.crud._base_public import CRUDPublic
from airweave.models.webhook_event import WebhookEvent


class WebhookEventCreate:
    """Schema for creating webhook events."""

    stripe_event_id: str
    event_type: str
    status: str
    processed_at: datetime
    error_message: Optional[str] = None


class WebhookEventUpdate:
    """Schema for updating webhook events."""

    status: Optional[str] = None
    error_message: Optional[str] = None


class CRUDWebhookEvent(CRUDPublic[WebhookEvent, WebhookEventCreate, WebhookEventUpdate]):
    """CRUD operations for WebhookEvent model."""

    async def get_by_stripe_event_id(
        self,
        db: AsyncSession,
        *,
        stripe_event_id: str,
    ) -> Optional[WebhookEvent]:
        """Get webhook event by Stripe event ID.

        Args:
            db: Database session
            stripe_event_id: Stripe event ID

        Returns:
            WebhookEvent or None
        """
        query = select(self.model).where(self.model.stripe_event_id == stripe_event_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def create_event(
        self,
        db: AsyncSession,
        *,
        stripe_event_id: str,
        event_type: str,
        status: str = "processed",
        error_message: Optional[str] = None,
    ) -> WebhookEvent:
        """Create a new webhook event record.

        Args:
            db: Database session
            stripe_event_id: Stripe event ID
            event_type: Event type
            status: Processing status (processed, failed)
            error_message: Error message if processing failed

        Returns:
            Created WebhookEvent
        """
        event = WebhookEvent(
            stripe_event_id=stripe_event_id,
            event_type=event_type,
            status=status,
            processed_at=datetime.utcnow(),
            error_message=error_message,
        )
        db.add(event)
        await db.flush()
        return event


# Create instance
webhook_event = CRUDWebhookEvent(WebhookEvent)
