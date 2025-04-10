import sqlalchemy as sa
from . import db

class MoodActivityLog(db.Model):
    __tablename__ = 'mood_activity_log'

    log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    mood_level = db.Column(db.Integer, nullable=True)  # e.g., 1-10 scale
    activity_notes = db.Column(db.Text, nullable=True)
    logged_at = db.Column(db.DateTime, server_default=sa.func.now())

    # Relationship to User
    user = db.relationship("User", back_populates="mood_logs")
