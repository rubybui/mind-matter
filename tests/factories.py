from factory import Factory, Faker, LazyFunction, SubFactory
from werkzeug.security import generate_password_hash
import uuid
from datetime import datetime
from mind_matter_api.models import User
from mind_matter_api.extensions import db
from mdgen import MarkdownPostProvider
from faker import Faker as BaseFaker
import random

base_faker = BaseFaker()
base_faker.add_provider(MarkdownPostProvider)
# Predefined tags
possible_tags = ["vegan", "meat", "gluten-free", "dairy-free", "spicy", "sweet", "low-carb", "keto"]


class UserFactory(Factory):
    class Meta:
        model = User

    id = LazyFunction(lambda: str(uuid.uuid4()))
    full_name = Faker("user_name")
    email = Faker("email")
    password = LazyFunction(lambda: generate_password_hash(str(Faker("password"))))

