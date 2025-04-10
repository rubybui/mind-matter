from flask_marshmallow import Marshmallow
from marshmallow import fields, Schema, validate
from mind_matter_api.models import (
    User,
    UserConsent,
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
    username = fields.Str(required=True)
    email = fields.Email(required=True)


# Marshmallow Schemas for Query/Path/Body validation (User)
class UserQuerySchema(Schema):
    username = fields.Str(required=True, example="john_doe")


class UserBodySchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    email = fields.Email(required=True, example="john@example.com")
    lastname = fields.Str(required=True, validate=validate.Length(min=1, max=50), example="Doe")
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


class SurveyAnswerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SurveyAnswer
        load_instance = True
        include_fk = True


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


# -------------------------------------------------------------
# User Consent Schema
# -------------------------------------------------------------
class UserConsentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserConsent
        load_instance = True
        include_fk = True
    user = fields.Nested(UserSchema, only=("id", "username", "email"))
    consent_given = fields.Boolean(required=True)
    updated_at = fields.DateTime(dump_only=True)
    created_at = fields.DateTime(dump_only=True)    