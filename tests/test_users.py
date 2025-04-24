import pytest
from tests.factories import UserFactory

from mind_matter_api.models import User

@pytest.fixture
def user_fixture(db_session):
    """Fixture to create a user."""
    user = UserFactory()
    db_session.add(user)
    db_session.commit()
    return user


def test_user_creation(user_fixture):
    """Test that a user is created successfully."""
    user = User.query.first()
    assert user.full_name is not None
    assert user.email is not None
    print(f"Created user: {user.full_name}, {user.email}")
