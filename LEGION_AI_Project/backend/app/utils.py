"""
Utility functions for data retrieval and processing.
"""

from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from . import models


def get_recent_health_data(db: Session, user_id: int, hours: int = 24) -> List[models.HealthData]:
    """
    Retrieve health data for a user within the last `hours` hours.
    """
    since = datetime.utcnow() - timedelta(hours=hours)
    return db.query(models.HealthData).filter(models.HealthData.user_id == user_id, models.HealthData.timestamp >= since).all()


def get_recent_mood_logs(db: Session, user_id: int, days: int = 7) -> List[models.MoodLog]:
    """Retrieve mood logs for a user within the last `days` days."""
    since = datetime.utcnow() - timedelta(days=days)
    return db.query(models.MoodLog).filter(models.MoodLog.user_id == user_id, models.MoodLog.timestamp >= since).all()


def get_recent_spending(db: Session, user_id: int, days: int = 30) -> List[models.SpendingLog]:
    """Retrieve spending logs for a user within the last `days` days."""
    since = datetime.utcnow() - timedelta(days=days)
    return db.query(models.SpendingLog).filter(models.SpendingLog.user_id == user_id, models.SpendingLog.timestamp >= since).all()