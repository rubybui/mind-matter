
from typing import Any, Dict, List, Optional
from mind_matter_api.models.emergency_contacts import EmergencyContact
from mind_matter_api.repositories.types import Repository   
from mind_matter_api.models import db


class EmergencyContactRepository(Repository):
    def __init__(self):
        self.session = db.session

    def create(self, contact: EmergencyContact) -> EmergencyContact:
        self.session.add(contact)
        self.session.commit()
        return contact

    def get_by_id(self, resource_id: Any) -> Optional[EmergencyContact]:
        return self.session.query(EmergencyContact).get(resource_id)

    def get_all(self, page: int = 1, page_size: int = 10, filters: Optional[Dict[str, Any]] = None) -> List[EmergencyContact]:
        query = self.session.query(EmergencyContact)
        if filters:
            for attr, value in filters.items():
                query = query.filter(getattr(EmergencyContact, attr) == value)
        return query.offset((page - 1) * page_size).limit(page_size).all()

    def update(self, resource_id: Any, data: Dict[str, Any]) -> EmergencyContact:
        contact = self.get_by_id(resource_id)
        if not contact:
            raise ValueError("Resource not found")
        for key, value in data.items():
            setattr(contact, key, value)
        self.session.commit()
        return contact

    def delete(self, resource_id: Any) -> None:
        contact = self.get_by_id(resource_id)
        if not contact:
            raise ValueError("Resource not found")
        self.session.delete(contact)
        self.session.commit()