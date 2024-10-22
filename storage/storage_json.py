import json


class StorageJson:
    """
    A class to handle movie storage in JSON format.
    """

    def __init__(self, file_path):
        """
        Initialize the storage with the given file path.

        Args:
            file_path (str): Path to the JSON file for storage.
        """
        self.file_path = file_path

    def list_movies(self):
        """
        List all movies stored in the JSON file.

        Returns:
            dict: A dictionary of movies or an empty dictionary if the file doesn't exist.
        """
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_movies(self, movies):
        """
        Save the current movie collection to the JSON file.

        Args:
            movies (dict): The dictionary of movies to save.
        """
        with open(self.file_path, 'w') as file:
            json.dump(movies, file, indent=4)
