import sqlalchemy as sa
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import logging
from flask import current_app as app

logging.basicConfig(level=logging.DEBUG)

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(100), nullable=False)
    share_data = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
        doc="Whether the user consents to share survey data with university staff"
    )
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.String(20), default='student')
    password = db.Column(db.String(128), nullable=False)

    created_at = db.Column(db.DateTime, server_default=sa.func.now())
    updated_at = db.Column(db.DateTime, server_default=sa.func.now(), onupdate=sa.func.now())

    # Example relationships:
    survey_responses = db.relationship("SurveyResponse", back_populates="user")
    mood_logs = db.relationship("MoodActivityLog", back_populates="user")
    notifications = db.relationship("Notification", back_populates="user")
    campaign_participation = db.relationship("CampaignParticipation", back_populates="user")
    incentives = db.relationship("Incentive", back_populates="user")
    reward_redemptions = db.relationship("RewardRedemption", back_populates="user")
    
    def set_password(self, password: str):
        self.password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    def get_id(self):
        return self.user_id
    def encode_auth_token(self, user_id):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=3600),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            token = jwt.encode(payload, app.secret_key, algorithm='HS256')
            app.logger.debug(f"app.secret_key: {app.secret_key}")
            app.logger.debug(f"payload: {payload}")

            if isinstance(token, bytes):  # for PyJWT < 2.0
                token = token.decode('utf-8')
            return token
        except Exception as e:
            # log error
            import traceback
            print("Token encoding failed:", traceback.format_exc())
            return None  # ✅ Don't return the error object

    
    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'