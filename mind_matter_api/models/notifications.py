import sqlalchemy as sa
from . import db

class Notification(db.Model):
    __tablename__ = 'notifications'

    notification_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, server_default=sa.func.now())
    read_at = db.Column(db.DateTime, nullable=True)
    type = db.Column(db.String(50), nullable=False)  # e.g., 'survey_reminder', 'nudge', 'emergency_alert'

    # Relationship to User
    user = db.relationship("User", back_populates="notifications")
