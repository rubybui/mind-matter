from typing import List, Dict, Any
from mind_matter_api.services.types import BaseService
from mind_matter_api.models.incentives_rewards import Incentive
from mind_matter_api.repositories.incentives import IncentiveRepository

class IncentiveService(BaseService):
    def __init__(self, incentive_repository: IncentiveRepository):
        self.incentive_repository = incentive_repository

    def get_campaign_incentives(self, campaign_id: int) -> List[Incentive]:
        """Get all incentives for a specific campaign"""
        return self.incentive_repository.get_all(filters={'campaign_id': campaign_id})

    def create_incentive(self, data: Dict[str, Any]) -> Incentive:
        """Create a new incentive"""
        incentive = Incentive(**data)
        return self.incentive_repository.create(incentive)

    def update_incentive(self, incentive_id: int, data: Dict[str, Any]) -> Incentive:
        """Update an existing incentive"""
        return self.incentive_repository.update(incentive_id, data)

    def delete_incentive(self, incentive_id: int) -> None:
        """Delete an incentive"""
        self.incentive_repository.delete(incentive_id) 