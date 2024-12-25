# storage_csv.py
import csv
from storage.istorage import IStorage


class StorageCsv(IStorage):
    def __init__(self, file_path):
        self.file_path = file_path

    def list_movies(self):
        """Read movies from the CSV file and return a dictionary of dictionaries."""
        movies = {}
        try:
            with open(self.file_path, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    title = row['title']
                    try:
                        year = int(row['year'])
                    except ValueError:
                        year = row['year']

                    movies[title] = {
                        'rating': float(row['rating']),
                        'year': year,
                        'poster': row['poster']
                    }
        except FileNotFoundError:
            print("File not found. Returning an empty list of movies.")
        return movies

    def add_movie(self, title, year, rating, poster):
        """Add a new movie to the CSV file."""
        with open(self.file_path, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['title', 'year', 'rating', 'poster'])
            if file.tell() == 0:  # Check if file is empty, to write headers
                writer.writeheader()
            writer.writerow({
                'title': title,
                'year': year,
                'rating': rating,
                'poster': poster
            })

    def delete_movie(self, title):
        """Delete a movie from the CSV file."""
        movies = self.list_movies()
        if title in movies:
            del movies[title]
            self.save_movies(movies)  # Save updated movies after deletion
            print(f"Movie '{title}' deleted successfully.")
        else:
            print(f"Movie '{title}' not found.")

    def update_movie(self, title, rating):
        """Update a movie's rating in the CSV file."""
        movies = self.list_movies()
        if title in movies:
            movies[title]['rating'] = rating
            self.save_movies(movies)  # Save updated movies after update
            print(f"Movie '{title}' updated successfully.")
        else:
            print(f"Movie '{title}' not found.")

    def save_movies(self, movies):
        """Save the movies back to the CSV file."""
        with open(self.file_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['title', 'year', 'rating', 'poster'])
            writer.writeheader()
            for movie_title, movie_data in movies.items():
                writer.writerow({
                    'title': movie_title,
                    'year': movie_data['year'],
                    'rating': movie_data['rating'],
                    'poster': movie_data['poster']
                })
        print("Movies saved to the CSV file.")
