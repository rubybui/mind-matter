from typing import Any, Dict, List, Optional
from mind_matter_api.models.surveys import SurveyQuestion
from mind_matter_api.repositories.types import Repository
from mind_matter_api.models import db   

class SurveyQuestionRepository(Repository[SurveyQuestion]):
    def __init__(self):
        super().__init__(SurveyQuestion)
