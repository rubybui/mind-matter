import sqlalchemy as sa
from . import db

class SurveySchedule(db.Model):
    __tablename__ = 'survey_schedule'

    schedule_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    survey_id = db.Column(db.Integer, db.ForeignKey('surveys.survey_id'), nullable=False)
    schedule_type = db.Column(db.String(50), nullable=False)  # e.g., 'weekly', 'monthly', 'event_triggered'
    start_date = db.Column(db.DateTime, nullable=True)
    end_date = db.Column(db.DateTime, nullable=True)

    # Relationship to Survey
    survey = db.relationship("Survey", back_populates="schedules")
