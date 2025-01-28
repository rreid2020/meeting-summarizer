# feature_guard.py
class FeatureGuard:
    def __init__(self, subscription_service):
        self.subscription_service = subscription_service

    async def check_access(self, user_id: int, feature: str, db: Session):
        subscription = db.query(Subscription).filter_by(user_id=user_id).first()
        features = {
            "free": ["basic_summary"],
            "pro": ["basic_summary", "custom_templates", "zoom_integration"],
            "enterprise": ["basic_summary", "custom_templates", "zoom_integration", "teams_integration"]
        }
        if feature not in features.get(subscription.plan, []):
            raise HTTPException(403, f"Feature {feature} not available in your plan")
        return True
