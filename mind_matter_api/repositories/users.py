from mind_matter_api.models.users import User
from mind_matter_api.repositories.types import Repository

from mind_matter_api.models import db
from typing import Any, Dict, List, Optional


class UserRepository(Repository):
    def __init__(self):  # TODO: pass db session here
        self.session = db.session

    def create(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        return user

    def get(self, user_id: str) -> User:
        return self.session.query(User).get(user_id)
    
    def get_by_email(self, email: str) -> User:
        return self.session.query(User).filter_by(email=email).first()

    def get_all(self, page: int = 1, page_size: int = 10, filters: Optional[Dict[str, Any]] = None) -> List[User]:
        query = self.session.query(User)
        if filters:
            for attr, value in filters.items():
                query = query.filter(getattr(User, attr) == value)
        return query.offset((page - 1) * page_size).limit(page_size).all()

    def get_by_id(self, resource_id: Any) -> Optional[User]:
        return self.session.query(User).get(resource_id)


    def update(self, resource_id: Any, data: Dict[str, Any]) -> User:
        user = self.get_by_id(resource_id)
        if not user:
            raise ValueError("Resource not found")
        for key, value in data.items():
            setattr(user, key, value)
        self.session.commit()
        return user
    
    def update_consent(self, resource_id: Any, consent: bool) -> User:
        user = self.get_by_id(resource_id)
        if not user:
            raise ValueError("Resource not found")
        user.share_data = consent
        self.session.commit()
        return user

    def delete(self, resource_id: Any) -> None:
        user = self.get_by_id(resource_id)
        if not user:
            raise ValueError("Resource not found")
        self.session.delete(user)
        self.session.commit()