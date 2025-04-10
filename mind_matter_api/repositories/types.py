from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

class Repository(ABC):
    @abstractmethod
    def get_all(self, page: int = 1, page_size: int = 10, filters: Optional[Dict[str, Any]] = None) -> List[Any]:
        """
        Retrieve all resources with pagination and optional filtering.

        :param page: The page number to retrieve.
        :param page_size: The number of items per page.
        :param filters: A dictionary of filters to apply.
        :return: A list of resources.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    @abstractmethod
    def get_by_id(self, resource_id: Any) -> Any:
        """
        Retrieve a single resource by its ID.

        :param resource_id: The ID of the resource.
        :return: The resource object.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    @abstractmethod
    def create(self, data: Dict[str, Any]) -> Any:
        """
        Create a new resource.

        :param data: A dictionary containing the resource data.
        :return: The created resource object.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    @abstractmethod
    def update(self, resource_id: Any, data: Dict[str, Any]) -> Any:
        """
        Update an existing resource.

        :param resource_id: The ID of the resource to update.
        :param data: A dictionary containing the updated data.
        :return: The updated resource object.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    @abstractmethod
    def delete(self, resource_id: Any) -> None:
        """
        Delete a resource by its ID.

        :param resource_id: The ID of the resource to delete.
        :return: None.
        """
        raise NotImplementedError("Subclasses must implement this method.")
