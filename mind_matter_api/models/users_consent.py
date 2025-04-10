import sqlalchemy as sa
from . import db

class UserConsent(db.Model):
    __tablename__ = 'users_consent'

    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    share_data = db.Column(db.Boolean, nullable=False, default=False)
    updated_at = db.Column(db.DateTime, server_default=sa.func.now(), onupdate=sa.func.now())

    # Relationship back to User
    user = db.relationship("User", back_populates="consent")
