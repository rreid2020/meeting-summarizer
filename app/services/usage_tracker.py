# usage_tracker.py
from datetime import datetime
from sqlalchemy.orm import Session
from ..models import Meeting

class UsageTracker:
    async def track_meeting(self, user_id: int, meeting_data: dict, db: Session):
        meeting = Meeting(
            user_id=user_id,
            duration=meeting_data.get('duration', 0),
            created_at=datetime.utcnow()
        )
        db.add(meeting)
        db.commit()

    async def get_usage_metrics(self, user_id: int, db: Session):
        return db.query(Meeting).filter_by(user_id=user_id).all()