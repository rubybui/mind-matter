import sqlalchemy as sa
from . import db

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.String(20), default='student')
    created_at = db.Column(db.DateTime, server_default=sa.func.now())
    updated_at = db.Column(db.DateTime, server_default=sa.func.now(), onupdate=sa.func.now())

    # Example relationships:
    consent = db.relationship("UserConsent", back_populates="user", uselist=False)
    survey_responses = db.relationship("SurveyResponse", back_populates="user")
    mood_logs = db.relationship("MoodActivityLog", back_populates="user")
    notifications = db.relationship("Notification", back_populates="user")
    campaign_participation = db.relationship("CampaignParticipation", back_populates="user")
    incentives = db.relationship("Incentive", back_populates="user")
    reward_redemptions = db.relationship("RewardRedemption", back_populates="user")
