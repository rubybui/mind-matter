from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Type, TypeVar, Generic
from mind_matter_api.models import db

T = TypeVar('T')

class Repository(Generic[T]):
    """Base repository class that provides common CRUD operations."""
    
    def __init__(self, model_class: Type[T]):
        self.session = db.session
        self.model_class = model_class

    def create(self, resource: T) -> T:
        """Create a new resource."""
        self.session.add(resource)
        self.session.commit()
        return resource

    def get_by_id(self, resource_id: Any) -> Optional[T]:
        """Retrieve a resource by its ID."""
        return self.session.get(self.model_class, resource_id)

    def get_all(self, page: int = 1, page_size: int = 10, filters: Optional[Dict[str, Any]] = None) -> List[T]:
        """Retrieve a paginated list of resources, optionally filtered."""
        query = self.session.query(self.model_class)
        if filters:
            for attr, value in filters.items():
                query = query.filter(getattr(self.model_class, attr) == value)
        return query.offset((page - 1) * page_size).limit(page_size).all()

    def get_count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """Get total count of resources, optionally filtered."""
        query = self.session.query(self.model_class)
        if filters:
            for attr, value in filters.items():
                query = query.filter(getattr(self.model_class, attr) == value)
        return query.count()

    def update(self, resource_id: Any, data: Dict[str, Any]) -> T:
        """Update an existing resource."""
        resource = self.get_by_id(resource_id)
        if not resource:
            raise ValueError("Resource not found")
        for key, value in data.items():
            setattr(resource, key, value)
        self.session.commit()
        return resource

    def delete(self, resource_id: Any) -> None:
        """Delete a resource by its ID."""
        resource = self.get_by_id(resource_id)
        if not resource:
            raise ValueError("Resource not found")
        self.session.delete(resource)
        self.session.commit()
