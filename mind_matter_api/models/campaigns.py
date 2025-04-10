import sqlalchemy as sa
from . import db

class Campaign(db.Model):
    __tablename__ = 'campaigns'

    campaign_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=sa.func.now())
    updated_at = db.Column(db.DateTime, server_default=sa.func.now(), onupdate=sa.func.now())

    # Relationship to CampaignParticipation
    participants = db.relationship("CampaignParticipation", back_populates="campaign")

class CampaignParticipation(db.Model):
    __tablename__ = 'campaign_participation'

    participation_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.campaign_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    joined_at = db.Column(db.DateTime, server_default=sa.func.now())
    status = db.Column(db.String(50), nullable=False, default='active')  # e.g., 'active', 'completed'

    # Relationships
    campaign = db.relationship("Campaign", back_populates="participants")
    user = db.relationship("User", back_populates="campaign_participation")
