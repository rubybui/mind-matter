from mind_matter_api.models.users_consent import UserConsent
from typing import Any, Dict, List, Optional
from mind_matter_api.repositories.types import Repository

from mind_matter_api.models import db


class UserConsentRepository(Repository):
    def __init__(self):
        self.session = db.session

    def create(self, consent: UserConsent) -> UserConsent:
        self.session.add(consent)
        self.session.commit()
        return consent

    def get_by_id(self, resource_id: Any) -> Optional[UserConsent]:
        return self.session.query(UserConsent).get(resource_id)

    def get_all(self, page: int = 1, page_size: int = 10, filters: Optional[Dict[str, Any]] = None) -> List[UserConsent]:
        query = self.session.query(UserConsent)
        if filters:
            for attr, value in filters.items():
                query = query.filter(getattr(UserConsent, attr) == value)
        return query.offset((page - 1) * page_size).limit(page_size).all()

    def update(self, resource_id: Any, data: Dict[str, Any]) -> UserConsent:
        consent = self.get_by_id(resource_id)
        if not consent:
            raise ValueError("Resource not found")
        for key, value in data.items():
            setattr(consent, key, value)
        self.session.commit()
        return consent

    def delete(self, resource_id: Any) -> None:
        consent = self.get_by_id(resource_id)
        if not consent:
            raise ValueError("Resource not found")
        self.session.delete(consent)
        self.session.commit()
