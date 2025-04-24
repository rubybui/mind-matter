from mind_matter_api.models.users import User
from mind_matter_api.repositories.users import UserRepository
from mind_matter_api.schemas import UserBodySchema
from mind_matter_api.services.types import BaseService
from werkzeug.security import check_password_hash


class UserService(BaseService):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_user(self, user_id: str) -> User:
        user = self.user_repository.get(user_id)
        return user 

    def create_user(self, user_data: UserBodySchema) -> User:
        new_user = User(**user_data)
        created_user = self.user_repository.create(new_user)
        return created_user

    def get_users(self) -> list[User]:
        # TODO: call UserRepository.get_users when it is implemented
        return [User(full_name="john_doe", email="john.doe@gmail.com")]

    def authenticate_user(self, login_data: dict) -> User:
        email = login_data.get("email")
        password = login_data.get("password")
        user = self.user_repository.get_by_email(email)
        if user and user.check_password(password):
            return user
        return None
    
    def register_user(self, user_data: dict) -> User:
        new_user = User(**user_data)
        new_user.set_password(user_data.pop("password"))
        return self.user_repository.create(new_user)
    
    def validate_new_email(self, email: str) -> bool:
        if self.user_repository.get_by_email(email):
            return False
        return True
#
    def update_user(self, user_id: str, user_data: dict) -> User:
        user = self.user_repository.get(user_id)
        if not user:
            raise ValueError("User not found")
        for key, value in user_data.items():
            setattr(user, key, value)
        self.user_repository.update(user)
        return user
    def delete_user(self, user_id: str) -> None:
        user = self.user_repository.get(user_id)
        if not user:
            raise ValueError("User not found")
        self.user_repository.delete(user)
    def update_consent(self, user_id: str, consent: bool) -> User:
        user = self.user_repository.get(user_id)
        if not user:
            raise ValueError("User not found")
        user.share_data = consent
        self.user_repository.update(user)
        return user