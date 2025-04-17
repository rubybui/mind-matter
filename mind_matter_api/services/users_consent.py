from mind_matter_api.models.users import User
from mind_matter_api.models.users_consent import UserConsent
from mind_matter_api.repositories.users_consent import UserConsentRepository
from mind_matter_api.schemas.users_consent import UserConsentBodySchema
from mind_matter_api.services.types import BaseService


class UserConsentService(BaseService):
    def __init__(self, user_consent_repository: UserConsentRepository):
        self.user_consent_repository = user_consent_repository

    def get_user_consent(self, user_id: str) -> UserConsent:
        user_consent = self.user_consent_repository.get(user_id)
        return user_consent
    def create_user_consent(self, user_data: UserConsent) -> UserConsent:   
        new_user_consent = User(**user_data)
        created_user_consent = self.user_consent_repository.create(new_user_consent)
        return created_user_consent

    