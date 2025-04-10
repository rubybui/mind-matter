from typing import Any, Dict, List, Optional
from mind_matter_api.models.campaigns import Campaign
from mind_matter_api.repositories.type import Repository
from mind_matter_api.models import db   

class CampaignRepository(Repository):
    def __init__(self):
        self.session = db.session

    def create(self, campaign: Campaign) -> Campaign:
        self.session.add(campaign)
        self.session.commit()
        return campaign

    def get_by_id(self, resource_id: Any) -> Optional[Campaign]:
        return self.session.query(Campaign).get(resource_id)

    def get_all(self, page: int = 1, page_size: int = 10, filters: Optional[Dict[str, Any]] = None) -> List[Campaign]:
        query = self.session.query(Campaign)
        if filters:
            for attr, value in filters.items():
                query = query.filter(getattr(Campaign, attr) == value)
        return query.offset((page - 1) * page_size).limit(page_size).all()

    def update(self, resource_id: Any, data: Dict[str, Any]) -> Campaign:
        campaign = self.get_by_id(resource_id)
        if not campaign:
            raise ValueError("Resource not found")
        for key, value in data.items():
            setattr(campaign, key, value)
        self.session.commit()
        return campaign

    def delete(self, resource_id: Any) -> None:
        campaign = self.get_by_id(resource_id)
        if not campaign:
            raise ValueError("Resource not found")
        self.session.delete(campaign)
        self.session.commit()