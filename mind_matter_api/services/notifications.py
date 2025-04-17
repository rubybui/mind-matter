from mind_matter_api.services.types import BaseService
from mind_matter_api.models.notifications import Notification
from mind_matter_api.repositories.notifications import NotificationRepository

class NotificationsService(BaseService):
    """
    Service class for managing notifications.
    """
    def __init__(self):
        """
        Initializes the NotificationsService with a NotificationRepository.
        """
        super().__init__(NotificationRepository())
    
    def get_notifications(self, user_id: str) -> list[Notification]:
        """
        Retrieves notifications for a specific user.

        Args:
            user_id (str): The ID of the user for whom to retrieve notifications.

        Returns:
            list[Notification]: A list of notifications for the specified user.
        """
        return self.repository.get_notifications(user_id)
    def get_notification(self, notification_id: str) -> Notification:
        """
        Retrieves a specific notification by its ID.

        Args:
            notification_id (str): The ID of the notification to retrieve.

        Returns:
            Notification: The notification with the specified ID.
        """
        return self.repository.get(notification_id)
    def create_notification(self, notification_data: dict) -> Notification:
        """
        Creates a new notification.
        Args:
            notification_data (dict): The data for the new notification.
        Returns:
            Notification: The created notification.
        """
        notification = Notification(**notification_data)
        self.repository.create(notification)
        return notification
    def update_notification(self, notification_id: str, notification_data: dict) -> Notification:
        """
        Updates an existing notification.
        Args:
            notification_id (str): The ID of the notification to update.
            notification_data (dict): The updated data for the notification.
        Returns:
            Notification: The updated notification.
        """
        notification = self.repository.get(notification_id)
        for key, value in notification_data.items():
            setattr(notification, key, value)
        self.repository.update(notification)
        return notification
    def delete_notification(self, notification_id: str) -> None:
        """ 
        Deletes a notification by its ID.
        Args:
            notification_id (str): The ID of the notification to delete.
        """
        notification = self.repository.get(notification_id)
        self.repository.delete(notification)
        return notification
