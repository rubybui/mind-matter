from typing import Any, Dict, List, Optional
from mind_matter_api.models.campaigns import CampaignParticipation
from mind_matter_api.repositories.types import Repository
from mind_matter_api.models import db   

class CampaignParticipationRepository(Repository):
    def __init__(self):
        self.session = db.session

    def create(self, participation: CampaignParticipation) -> CampaignParticipation:
        self.session.add(participation)
        self.session.commit()
        return participation

    def get_by_id(self, resource_id: Any) -> Optional[CampaignParticipation]:
        return self.session.query(CampaignParticipation).get(resource_id)

    def get_all(self, page: int = 1, page_size: int = 10, filters: Optional[Dict[str, Any]] = None) -> List[CampaignParticipation]:
        query = self.session.query(CampaignParticipation)
        if filters:
            for attr, value in filters.items():
                query = query.filter(getattr(CampaignParticipation, attr) == value)
        return query.offset((page - 1) * page_size).limit(page_size).all()

    def update(self, resource_id: Any, data: Dict[str, Any]) -> CampaignParticipation:
        participation = self.get_by_id(resource_id)
        if not participation:
            raise ValueError("Resource not found")
        for key, value in data.items():
            setattr(participation, key, value)
        self.session.commit()
        return participation

    def delete(self, resource_id: Any) -> None:
        participation = self.get_by_id(resource_id)
        if not participation:
            raise ValueError("Resource not found")
        self.session.delete(participation)
        self.session.commit()
