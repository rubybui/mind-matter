import sqlalchemy as sa
from . import db

class SurveyAnswer(db.Model):
    __tablename__ = 'survey_answers'

    answer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    response_id = db.Column(db.Integer, db.ForeignKey('survey_responses.response_id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('survey_questions.question_id'), nullable=False)
    answer_value = db.Column(db.Text, nullable=True)

    # Example relationships:
    response = db.relationship("SurveyResponse", back_populates="answers")
    question = db.relationship("SurveyQuestion", back_populates="answers")
