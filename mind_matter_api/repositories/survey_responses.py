from typing import Any, Dict, List, Optional
from mind_matter_api.models.surveys import SurveyResponse
from mind_matter_api.repositories.types import Repository
from mind_matter_api.models import db   

class SurveyResponseRepository(Repository[SurveyResponse]):
    def __init__(self):
        super().__init__(SurveyResponse)

    def create(self, response: SurveyResponse) -> SurveyResponse:
        self.session.add(response)
        self.session.commit()
        return response

    def get_by_id(self, resource_id: Any) -> Optional[SurveyResponse]:
        return self.session.query(SurveyResponse).get(resource_id)

    def get_all(self, page: int = 1, page_size: int = 10, filters: Optional[Dict[str, Any]] = None) -> List[SurveyResponse]:
        query = self.session.query(SurveyResponse)
        if filters:
            for attr, value in filters.items():
                query = query.filter(getattr(SurveyResponse, attr) == value)
        return query.offset((page - 1) * page_size).limit(page_size).all()

    def update(self, resource_id: Any, data: Dict[str, Any]) -> SurveyResponse:
        response = self.get_by_id(resource_id)
        if not response:
            raise ValueError("Resource not found")
        for key, value in data.items():
            setattr(response, key, value)
        self.session.commit()
        return response

    def delete(self, resource_id: Any) -> None:
        response = self.get_by_id(resource_id)
        if not response:
            raise ValueError("Resource not found")
        self.session.delete(response)
        self.session.commit()
