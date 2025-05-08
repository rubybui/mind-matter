from flask_marshmallow import Marshmallow
from marshmallow import fields, Schema, validate
from mind_matter_api.models import (
    User,
    Survey,
    SurveyQuestion,
    SurveyResponse,
    SurveyAnswer,
    SurveySchedule,
    Notification,
    MoodActivityLog,
    Campaign,
    CampaignParticipation,
    Incentive,
    Reward,
    RewardRedemption,
    EmergencyContact
)

ma = Marshmallow()


# -------------------------------------------------------------
# User Schemas
# -------------------------------------------------------------
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        include_fk = True  # Include foreign keys in the schema

    id = fields.Str(dump_only=True)  # Explicitly declare 'id' as dump-only
    full_name = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=100),
        example="John Doe"
    )
    email = fields.Email(required=True)
    share_data = fields.Boolean(default=False)


# Marshmallow Schemas for Query/Path/Body validation (User)
class UserQuerySchema(Schema):
    full_name = fields.Str(required=True, example="john_doe")


class UserBodySchema(Schema):
    full_name = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    email = fields.Email(required=True, example="john@example.com")

    password = fields.Str(required=True, validate=validate.Length(min=6), load_only=True)


class UserLoginSchema(Schema):
    email = fields.Email(required=True, example="user@example.com")
    password = fields.Str(required=True, load_only=True, example="securepassword")


# -------------------------------------------------------------
# Survey Schemas
# -------------------------------------------------------------
class SurveySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Survey
        load_instance = True
        include_fk = True

class SurveyQuestionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SurveyQuestion
        load_instance = True
        include_fk = True

class SurveyResponseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SurveyResponse
        load_instance = True
        include_fk = True
        
    response_id = fields.Int(dump_only=True, required=False)  # Make it optional and read-only
    survey_id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    submitted_at = fields.DateTime(dump_only=True)
    
    # Relationships - exclude nested answers to prevent circular reference
    survey = fields.Nested(SurveySchema, dump_only=True)
    user = fields.Nested(UserSchema, dump_only=True)
    answers = fields.Nested('SurveyAnswerSchema', many=True, dump_only=True, exclude=('response',))

class SurveyAnswerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SurveyAnswer
        load_instance = True
        include_fk = True
        
    answer_id = fields.Int(dump_only=True)  # Auto-generated
    response_id = fields.Int(required=True)  # Required when creating
    question_id = fields.Int(required=True)
    answer_value = fields.Str(required=True)
    
    # Relationships - exclude nested response to prevent circular reference
    response = fields.Nested('SurveyResponseSchema', dump_only=True, exclude=('answers',))
    question = fields.Nested(SurveyQuestionSchema, dump_only=True)


class SurveyScheduleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SurveySchedule
        load_instance = True
        include_fk = True


# -------------------------------------------------------------
# Notification Schemas
# -------------------------------------------------------------
class NotificationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Notification
        load_instance = True
        include_fk = True


# -------------------------------------------------------------
# Mood & Activity Schema
# -------------------------------------------------------------
class MoodActivityLogSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = MoodActivityLog
        load_instance = True
        include_fk = True


# -------------------------------------------------------------
# Campaign Schemas
# -------------------------------------------------------------
class CampaignSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Campaign
        load_instance = True
        include_fk = True


class CampaignParticipationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CampaignParticipation
        load_instance = True
        include_fk = True


# -------------------------------------------------------------
# Incentive & Reward Schemas
# -------------------------------------------------------------
class IncentiveSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Incentive
        load_instance = True
        include_fk = True


class RewardSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Reward
        load_instance = True
        include_fk = True


class RewardRedemptionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RewardRedemption
        load_instance = True
        include_fk = True


# -------------------------------------------------------------
# Emergency Contact Schema
# -------------------------------------------------------------
class EmergencyContactSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = EmergencyContact
        load_instance = True
        include_fk = True


  