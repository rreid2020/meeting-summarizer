# feature_guard.py
from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..models import Subscription

class FeatureGuard:
    def __init__(self, subscription_service):
        self.subscription_service = subscription_service

    async def check_access(self, user_id: int, feature: str, db: Session):
        subscription = db.query(Subscription).filter_by(user_id=user_id).first()
        
        if not subscription:
            raise HTTPException(403, "No active subscription found")
            
        feature_limits = {
            "transcription": {"free": 5, "pro": float("inf")},
            "summary": {"free": 5, "pro": float("inf")},
            "export": {"free": 2, "pro": float("inf")}
        }
        
        limit = feature_limits.get(feature, {}).get(subscription.plan)
        if limit is None:
            raise HTTPException(403, f"Feature {feature} not available")
            
        return True
