from mind_matter_api.services.types import BaseService
from mind_matter_api.models.emergency_contacts import EmergencyContact
from mind_matter_api.repositories.emergency_contacts import EmergencyContactRepository
from typing import List, Dict, Any
import logging

logging.basicConfig(level=logging.DEBUG)

class EmergencyContactsService(BaseService):
    def __init__(self, emergency_contacts_repository: EmergencyContactRepository):
        self.emergency_contacts_repository = emergency_contacts_repository

    def get_emergency_contacts(self, user_id: str) -> List[EmergencyContact]:
        emergency_contacts = self.emergency_contacts_repository.get_by_user_id(user_id)
        return emergency_contacts

    def create_emergency_contacts(self, user_id: str, contact_data: Dict[str, Any]) -> EmergencyContact:
        new_contact = EmergencyContact(**contact_data)
        created_contact = self.emergency_contacts_repository.create(new_contact)
        return created_contact

    def update_emergency_contacts(self, contact_id: int, contact_data: Dict[str, Any]) -> EmergencyContact:
        # If contact_data is an EmergencyContact instance, convert it to a dict
        if isinstance(contact_data, EmergencyContact):
            contact_data = {
                'contact_name': contact_data.contact_name,
                'phone_number': contact_data.phone_number,
                'description': contact_data.description
            }

        return self.emergency_contacts_repository.update(contact_id, contact_data)

    def delete_emergency_contacts(self, contact_id: int) -> None:
        self.emergency_contacts_repository.delete(contact_id)
    