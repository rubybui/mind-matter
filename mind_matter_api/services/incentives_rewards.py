from mind_matter_api.services.types import BaseService
from mind_matter_api.models.incentives_rewards import IncentivesRewards
from mind_matter_api.repositories.incentives_rewards import IncentivesRewardsRepository

class IncentivesRewardsService(BaseService):
    def __init__(self, incentives_rewards_repository: IncentivesRewardsRepository):
        self.incentives_rewards_repository = incentives_rewards_repository

    def get_incentives_rewards(self, user_id: str) -> IncentivesRewards:
        incentives_rewards = self.incentives_rewards_repository.get(user_id)
        return incentives_rewards

    def create_incentives_rewards(self, user_data: IncentivesRewards) -> IncentivesRewards:
        new_incentives_rewards = IncentivesRewards(**user_data)
        created_incentives_rewards = self.incentives_rewards_repository.create(new_incentives_rewards)
        return created_incentives_rewards
    def update_incentives_rewards(self, user_id: str, incentives_rewards_data: IncentivesRewards) -> IncentivesRewards: 
        incentives_rewards = self.incentives_rewards_repository.get(user_id)
        incentives_rewards.update(**incentives_rewards_data)
        self.incentives_rewards_repository.update(incentives_rewards)
        return incentives_rewards
    def delete_incentives_rewards(self, user_id: str) -> None:
        incentives_rewards = self.incentives_rewards_repository.get(user_id)
        self.incentives_rewards_repository.delete(incentives_rewards)