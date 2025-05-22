import sqlalchemy as sa
from . import db

class Incentive(db.Model):
    __tablename__ = 'incentives'

    incentive_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.campaign_id'), nullable=False)
    points = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.String(255), nullable=True)
    awarded_at = db.Column(db.DateTime, server_default=sa.func.now())

    # Relationship to Campaign
    campaign = db.relationship("Campaign", back_populates="incentives")

class Reward(db.Model):
    __tablename__ = 'rewards'

    reward_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    cost_points = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, server_default=sa.func.now())
    updated_at = db.Column(db.DateTime, server_default=sa.func.now(), onupdate=sa.func.now())

class RewardRedemption(db.Model):
    __tablename__ = 'reward_redemptions'

    redemption_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reward_id = db.Column(db.Integer, db.ForeignKey('rewards.reward_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    points_spent = db.Column(db.Integer, nullable=False)
    redeemed_at = db.Column(db.DateTime, server_default=sa.func.now())

    # Relationships
    reward = db.relationship("Reward", backref="redemptions")
    user = db.relationship("User", back_populates="reward_redemptions")