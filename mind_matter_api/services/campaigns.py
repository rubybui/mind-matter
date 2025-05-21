from mind_matter_api.services.types import BaseService
from mind_matter_api.models.campaigns import Campaigns, CampaignParticipation
from mind_matter_api.repositories.campaigns import CampaignsRepository

class CampaignsService(BaseService):
    def __init__(self, campaigns_repository: CampaignsRepository):
        self.campaigns_repository = campaigns_repository

    def get_campaigns(self, user_id: str) -> Campaigns:
        campaigns = self.campaigns_repository.get(user_id)
        return campaigns

    def get_survey_responses_count(self, campaign_id: str) -> int:
        survey_responses_count = self.campaigns_repository.get_survey_responses_count(campaign_id)
        return survey_responses_count
    
    def get_campaign_participation(self, campaign_id: str) -> CampaignParticipation:
        campaign_participation = self.campaigns_repository.get_campaign_participation(campaign_id)
        return campaign_participation
    
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