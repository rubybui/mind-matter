from typing import Any, Dict, List, Optional
from mind_matter_api.models.notifications import Notification
from mind_matter_api.repositories.type import Repository
from mind_matter_api.models import db   


class NotificationRepository(Repository):
    def __init__(self):
        self.session = db.session

    def create(self, notification: Notification) -> Notification:
        self.session.add(notification)
        self.session.commit()
        return notification

    def get_by_id(self, resource_id: Any) -> Optional[Notification]:
        return self.session.query(Notification).get(resource_id)

    def get_all(self, page: int = 1, page_size: int = 10, filters: Optional[Dict[str, Any]] = None) -> List[Notification]:
        query = self.session.query(Notification)
        if filters:
            for attr, value in filters.items():
                query = query.filter(getattr(Notification, attr) == value)
        return query.offset((page - 1) * page_size).limit(page_size).all()

    def update(self, resource_id: Any, data: Dict[str, Any]) -> Notification:
        notification = self.get_by_id(resource_id)
        if not notification:
            raise ValueError("Resource not found")
        for key, value in data.items():
            setattr(notification, key, value)
        self.session.commit()
        return notification

    def delete(self, resource_id: Any) -> None:
        notification = self.get_by_id(resource_id)
        if not notification:
            raise ValueError("Resource not found")
        self.session.delete(notification)
        self.session.commit()