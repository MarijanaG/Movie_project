import json
import os

class StorageJson:
    def __init__(self, file_path):
        self.file_path = file_path
        if not os.path.exists(self.file_path):
            # Create an empty file if it doesn't exist
            with open(self.file_path, 'w') as file:
                json.dump({}, file)

    def get_movies(self):
        """Retrieve movies from the storage (JSON file)."""
        with open(self.file_path, 'r') as file:
            return json.load(file)

    def save_movies(self, movies):
        """Save the updated list of movies to the JSON file."""
        with open(self.file_path, 'w') as file:
            json.dump(movies, file, indent=4)
