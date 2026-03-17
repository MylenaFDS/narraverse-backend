from sqlalchemy.orm import Session
from app.models.notification import Notification


def create_notification(db: Session, user_id: int, message: str):

    notification = Notification(
        user_id=user_id,
        message=message
    )

    db.add(notification)
    db.commit()