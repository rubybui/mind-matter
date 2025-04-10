import sqlalchemy as sa
from . import db

class EmergencyContact(db.Model):
    __tablename__ = 'emergency_contacts'

    contact_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    contact_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, server_default=sa.func.now())
