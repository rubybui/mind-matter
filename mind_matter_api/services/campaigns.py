from mind_matter_api.services.types import BaseService
from mind_matter_api.models.campaigns import Campaigns
from mind_matter_api.repositories.campaigns import CampaignsRepository

class CampaignsService(BaseService):
    def __init__(self, campaigns_repository: CampaignsRepository):
        self.campaigns_repository = campaigns_repository

    def get_campaigns(self, user_id: str) -> Campaigns:
        campaigns = self.campaigns_repository.get(user_id)
        return campaigns

    def create_campaigns(self, user_data: Campaigns) -> Campaigns:
        new_campaigns = Campaigns(**user_data)
        created_campaigns = self.campaigns_repository.create(new_campaigns)
        return created_campaigns
    def update_campaigns(self, user_id: str, campaigns_data: Campaigns) -> Campaigns:
        campaigns = self.campaigns_repository.get(user_id)
        campaigns.update(**campaigns_data)
        self.campaigns_repository.update(campaigns)
        return campaigns
    def delete_campaigns(self, user_id: str) -> None:
        campaigns = self.campaigns_repository.get(user_id)
        self.campaigns_repository.delete(campaigns)