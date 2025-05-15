import sqlalchemy as sa
from . import db

class Survey(db.Model):
    __tablename__ = 'surveys'

    survey_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=sa.func.now())
    updated_at = db.Column(db.DateTime, server_default=sa.func.now(), onupdate=sa.func.now())

    # Relationships
    user = db.relationship("User", back_populates="surveys")
    questions = db.relationship("SurveyQuestion", back_populates="survey")
    responses = db.relationship("SurveyResponse", back_populates="survey")
    schedules = db.relationship("SurveySchedule", back_populates="survey")

class SurveyQuestion(db.Model):
    __tablename__ = 'survey_questions'

    question_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    survey_id = db.Column(db.Integer, db.ForeignKey('surveys.survey_id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, server_default=sa.func.now())

    # Relationships
    survey = db.relationship("Survey", back_populates="questions")
    answers = db.relationship("SurveyAnswer", back_populates="question")

class SurveyResponse(db.Model):
    __tablename__ = 'survey_responses'

    response_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    survey_id = db.Column(db.Integer, db.ForeignKey('surveys.survey_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    submitted_at = db.Column(db.DateTime, server_default=sa.func.now())

    # Relationships
    survey = db.relationship("Survey", back_populates="responses")
    user = db.relationship("User", back_populates="survey_responses")
    answers = db.relationship("SurveyAnswer", back_populates="response")
