from typing import Any, Dict, List, Optional
from mind_matter_api.models.incentives_rewards import Incentive
from mind_matter_api.repositories.types import Repository
from mind_matter_api.models import db
class IncentiveRepository(Repository):
    def __init__(self):
        self.session = db.session

    def create(self, incentive: Incentive) -> Incentive:
        self.session.add(incentive)
        self.session.commit()
        return incentive

    def get_by_id(self, resource_id: Any) -> Optional[Incentive]:
        return self.session.query(Incentive).get(resource_id)

    def get_all(self, page: int = 1, page_size: int = 10, filters: Optional[Dict[str, Any]] = None) -> List[Incentive]:
        query = self.session.query(Incentive)
        if filters:
            for attr, value in filters.items():
                query = query.filter(getattr(Incentive, attr) == value)
        return query.offset((page - 1) * page_size).limit(page_size).all()

    def update(self, resource_id: Any, data: Dict[str, Any]) -> Incentive:
        incentive = self.get_by_id(resource_id)
        if not incentive:
            raise ValueError("Resource not found")
        for key, value in data.items():
            setattr(incentive, key, value)
        self.session.commit()
        return incentive

    def delete(self, resource_id: Any) -> None:
        incentive = self.get_by_id(resource_id)
        if not incentive:
            raise ValueError("Resource not found")
        self.session.delete(incentive)
        self.session.commit()
