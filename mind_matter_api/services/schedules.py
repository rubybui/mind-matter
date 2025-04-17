from mind_matter_api.services.types import BaseService
from mind_matter_api.models.schedules import Schedule

from mind_matter_api.repositories.schedules import ScheduleRepository

class ScheduleService(BaseService):
    """
    Service class for managing schedules.
    """
    def __init__(self):
        """
        Initialize the ScheduleService.
        """
        super().__init__(Schedule, ScheduleRepository)
        self.repository = ScheduleRepository()
        self.model = Schedule
    def get_schedule(self, user_id: str):
        """
        Get the schedule for a specific user.
        """
        return self.repository.get_schedule(user_id)
    def create_schedule(self, schedule_data: dict):
        """
        Create a new schedule.
        """
        schedule = self.model(**schedule_data)
        self.create(schedule)
        return schedule
    def update_schedule(self, schedule_id: str, schedule_data: dict):
        """
        Update an existing schedule.
        """
        schedule = self.repository.get(schedule_id)
        for key, value in schedule_data.items():
            setattr(schedule, key, value)
        self.update(schedule)
        return schedule
    def delete_schedule(self, schedule_id: str):
        """
        Delete a schedule.
        """
        schedule = self.repository.get(schedule_id)
        self.delete(schedule)
        return schedule