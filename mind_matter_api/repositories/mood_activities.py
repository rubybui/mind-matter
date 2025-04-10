from typing import Any, Dict, List, Optional
from mind_matter_api.models.mood_activities import MoodActivityLog
from mind_matter_api.repositories.types import Repository
from mind_matter_api.models import db


class MoodActivityLogRepository(Repository):
    def __init__(self):
        self.session = db.session

    def create(self, mood_log: MoodActivityLog) -> MoodActivityLog:
        self.session.add(mood_log)
        self.session.commit()
        return mood_log

    def get_by_id(self, resource_id: Any) -> Optional[MoodActivityLog]:
        return self.session.query(MoodActivityLog).get(resource_id)

    def get_all(self, page: int = 1, page_size: int = 10, filters: Optional[Dict[str, Any]] = None) -> List[MoodActivityLog]:
        query = self.session.query(MoodActivityLog)
        if filters:
            for attr, value in filters.items():
                query = query.filter(getattr(MoodActivityLog, attr) == value)
        return query.offset((page - 1) * page_size).limit(page_size).all()

    def update(self, resource_id: Any, data: Dict[str, Any]) -> MoodActivityLog:
        mood_log = self.get_by_id(resource_id)
        if not mood_log:
            raise ValueError("Resource not found")
        for key, value in data.items():
            setattr(mood_log, key, value)
        self.session.commit()
        return mood_log

    def delete(self, resource_id: Any) -> None:
        mood_log = self.get_by_id(resource_id)
        if not mood_log:
            raise ValueError("Resource not found")
        self.session.delete(mood_log)
        self.session.commit()
