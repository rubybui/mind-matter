from typing import Any, Dict, List, Optional
from mind_matter_api.models.incentives_rewards import Reward, RewardRedemption
from mind_matter_api.repositories.types import Repository
from mind_matter_api.models import db


class RewardRepository(Repository):
    def __init__(self):
        self.session = db.session

    def create(self, reward: Reward) -> Reward:
        self.session.add(reward)
        self.session.commit()
        return reward

    def get_by_id(self, resource_id: Any) -> Optional[Reward]:
        return self.session.query(Reward).get(resource_id)

    def get_all(self, page: int = 1, page_size: int = 10, filters: Optional[Dict[str, Any]] = None) -> List[Reward]:
        query = self.session.query(Reward)
        if filters:
            for attr, value in filters.items():
                query = query.filter(getattr(Reward, attr) == value)
        return query.offset((page - 1) * page_size).limit(page_size).all()

    def update(self, resource_id: Any, data: Dict[str, Any]) -> Reward:
        reward = self.get_by_id(resource_id)
        if not reward:
            raise ValueError("Resource not found")
        for key, value in data.items():
            setattr(reward, key, value)
        self.session.commit()
        return reward

    def delete(self, resource_id: Any) -> None:
        reward = self.get_by_id(resource_id)
        if not reward:
            raise ValueError("Resource not found")
        self.session.delete(reward)
        self.session.commit()

class RewardRedemptionRepository(Repository):
    def __init__(self):
        self.session = db.session

    def create(self, redemption: RewardRedemption) -> RewardRedemption:
        self.session.add(redemption)
        self.session.commit()
        return redemption

    def get_by_id(self, resource_id: Any) -> Optional[RewardRedemption]:
        return self.session.query(RewardRedemption).get(resource_id)

    def get_all(self, page: int = 1, page_size: int = 10, filters: Optional[Dict[str, Any]] = None) -> List[RewardRedemption]:
        query = self.session.query(RewardRedemption)
        if filters:
            for attr, value in filters.items():
                query = query.filter(getattr(RewardRedemption, attr) == value)
        return query.offset((page - 1) * page_size).limit(page_size).all()

    def update(self, resource_id: Any, data: Dict[str, Any]) -> RewardRedemption:
        redemption = self.get_by_id(resource_id)
        if not redemption:
            raise ValueError("Resource not found")
        for key, value in data.items():
            setattr(redemption, key, value)
        self.session.commit()
        return redemption

    def delete(self, resource_id: Any) -> None:
        redemption = self.get_by_id(resource_id)
        if not redemption:
            raise ValueError("Resource not found")
        self.session.delete(redemption)
        self.session.commit()