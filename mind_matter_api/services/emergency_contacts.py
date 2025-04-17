from mind_matter_api.services.types import BaseService
from mind_matter_api.models.emergency_contacts import EmergencyContacts
from mind_matter_api.repositories.emergency_contacts import EmergencyContactsRepository

class EmergencyContactsService(BaseService):
    def __init__(self, emergency_contacts_repository: EmergencyContactsRepository):
        self.emergency_contacts_repository = emergency_contacts_repository

    def get_emergency_contacts(self, user_id: str) -> EmergencyContacts:
        emergency_contacts = self.emergency_contacts_repository.get(user_id)
        return emergency_contacts

    def create_emergency_contacts(self, user_data: EmergencyContacts) -> EmergencyContacts:
        new_emergency_contacts = EmergencyContacts(**user_data)
        created_emergency_contacts = self.emergency_contacts_repository.create(new_emergency_contacts)
        return created_emergency_contacts
    def update_emergency_contacts(self, user_id: str, emergency_contacts_data: EmergencyContacts) -> EmergencyContacts:
        emergency_contacts = self.emergency_contacts_repository.get(user_id)
        emergency_contacts.update(**emergency_contacts_data)
        self.emergency_contacts_repository.update(emergency_contacts)
        return emergency_contacts
    def delete_emergency_contacts(self, user_id: str) -> None:
        emergency_contacts = self.emergency_contacts_repository.get(user_id)
        self.emergency_contacts_repository.delete(emergency_contacts)
    