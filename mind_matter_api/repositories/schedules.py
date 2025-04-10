from typing import Any, Dict, List, Optional
from mind_matter_api.models.schedules import SurveySchedule
from mind_matter_api.repositories.type import Repository
from mind_matter_api.models import db   

class SurveyScheduleRepository(Repository):
    def __init__(self):
        self.session = db.session

    def create(self, schedule: SurveySchedule) -> SurveySchedule:
        self.session.add(schedule)
        self.session.commit()
        return schedule

    def get_by_id(self, resource_id: Any) -> Optional[SurveySchedule]:
        return self.session.query(SurveySchedule).get(resource_id)

    def get_all(self, page: int = 1, page_size: int = 10, filters: Optional[Dict[str, Any]] = None) -> List[SurveySchedule]:
        query = self.session.query(SurveySchedule)
        if filters:
            for attr, value in filters.items():
                query = query.filter(getattr(SurveySchedule, attr) == value)
        return query.offset((page - 1) * page_size).limit(page_size).all()

    def update(self, resource_id: Any, data: Dict[str, Any]) -> SurveySchedule:
        schedule = self.get_by_id(resource_id)
        if not schedule:
            raise ValueError("Resource not found")
        for key, value in data.items():
            setattr(schedule, key, value)
        self.session.commit()
        return schedule

    def delete(self, resource_id: Any) -> None:
        schedule = self.get_by_id(resource_id)
        if not schedule:
            raise ValueError("Resource not found")
        self.session.delete(schedule)
        self.session.commit()
