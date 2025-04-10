from flask_marshmallow import Marshmallow
from marshmallow import fields, Schema, validate
from mind_matter_api.models import User

ma = Marshmallow()


# User Schema
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True

    id = fields.Str(dump_only=True)  # Explicitly declare 'id' as a dump-only integer
    username = fields.Str(required=True)
    email = fields.Email(required=True)


# Marshmallow Schema for Query/Path/Body validation
class UserQuerySchema(Schema):
    username = fields.Str(required=True, example="john_doe")


class UserBodySchema(Schema):
    username = fields.Str(required=True, validate=fields.Length(min=3, max=50))
    email = fields.Email(required=True, example="john@example.com")
    lastname = fields.Str(
        required=True, validate=fields.Length(min=1, max=50), example="Doe"
    )
    password = fields.Str(required=True, validate=fields.Length(min=6), load_only=True)


class UserLoginSchema(Schema):
    email = fields.Email(required=True, example="user@example.com")
    password = fields.Str(required=True, load_only=True, example="securepassword")

