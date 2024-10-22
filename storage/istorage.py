from abc import ABC, abstractmethod


class IStorage(ABC):
    """
    Abstract base class for movie storage systems.
    """

    @abstractmethod
    def list_movies(self):
        """
        List all movies in the storage system.
        """
        pass

    @abstractmethod
    def save_movies(self, movies):
        """
        Save the movies to the storage system.

        Args:
            movies (dict): The dictionary of movies to save.
        """
        pass
