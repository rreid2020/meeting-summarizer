# subscription.py
import stripe
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..models import Subscription
from ..config import Settings

class SubscriptionService:
    def __init__(self):
        self.settings = Settings()
        stripe.api_key = self.settings.stripe_secret_key

    async def check_meeting_limit(self, user_id: int, db: Session):
        subscription = db.query(Subscription).filter_by(user_id=user_id).first()
        if subscription.plan == "free" and subscription.meetings_used >= 5:
            raise HTTPException(403, "Monthly meeting limit reached")
        return True

    async def handle_webhook(self, request):
        event = stripe.Webhook.construct_event(
            request.body(), 
            request.headers['stripe-signature'],
            self.settings.stripe_webhook_secret
        )
        
        if event.type == "customer.subscription.created":
            await self._handle_subscription_created(event.data.object)
        elif event.type == "customer.subscription.deleted":
            await self._handle_subscription_deleted(event.data.object)
        
        return {"status": "processed"}