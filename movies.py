import json
import random
from statistics import median
import os
import requests
from storage import storage_json
from dotenv import load_dotenv

load_dotenv()

JSON_FILE = "data/data.json"

class MovieClass:
    def __init__(self, storage):
        self.storage = storage

    def fetch_movie_data(self, title):
        """
        Fetch movie data from the OMDb API based on the movie title.
        """
        url = f"{self.api_url}?t={title}&apikey={self.api_key}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            if data.get('Response') == 'True':
                return {
                    'Title': data.get('Title'),
                    'Year': data.get('Year'),
                    'Rating': data.get('imdbRating'),
                    'Plot': data.get('Plot')
                }
            else:
                print(f"Movie '{title}' not found.")
                return None
        else:
            print("Error fetching data from API.")
            return None

    def save_movie_to_storage(self, movie_data):
        """
        Save movie data to storage (JSON file).
        """
        if movie_data:
            movies = self.storage.get_movies()
            movies[movie_data['Title']] = {
                'rating': movie_data['Rating'],
                'year': movie_data['Year'],
                'plot': movie_data['Plot']
            }
            self.storage.save_movies(movies)
            print(f"Movie '{movie_data['Title']}' added to storage.")

def load_movies_from_storage():
    """
    Load movies from the JSON storage.
    """
    with open(JSON_FILE, 'r') as file:
        movies = json.load(file)
    return movies

def list_movie(movies):
    """
    List all movies and their details in a formatted way.
    """
    movie_list = []
    for title, details in movies.items():
        movie_info = f"{title} - Rating: {details['rating']} (Year: {details['year']})"
        movie_list.append(movie_info)
    return movie_list

def add_movie(movies, storage):
    """
    Add a new movie to the collection.
    """
    key = input("Please enter the movie title: ").strip()
    while not key:
        print("Movie title cannot be empty!")
        key = input("Please enter a valid movie title: ").strip()

    try:
        value = float(input("Please rate the movie (1 - 10): "))
        if value < 1 or value > 10:
            raise ValueError("Rating should be between 1 and 10.")
    except ValueError as e:
        print(f"Invalid input for rating: {e}")
        return movies

    try:
        year_movie = int(input("Please enter the release year: "))
    except ValueError as e:
        print(f"Invalid input for year: {e}")
        return movies

    movies[key] = {"rating": value, "year": year_movie}
    print(f"Successfully added movie '{key}' with a rating of {value} and year {year_movie}")

    # Save to storage
    storage.save_movies(movies)

    return movies

def delete_movie(movies):
    """
    Delete a movie from the collection.
    """
    key = input("Please enter the movie you want to delete: ").strip()
    if key in movies:
        del movies[key]
        print(f"Movie '{key}' has been deleted.")
    else:
        print(f"Movie '{key}' is not in the list.")
    return movies

def update_movies(movies):
    """
    Update the rating and year of an existing movie.
    """
    movie_update = input("Please enter the movie you want to update: ").strip()
    if movie_update in movies:
        try:
            movie_rating = float(input("Please enter the new rating for that movie (1 - 10): "))
            if movie_rating < 1 or movie_rating > 10:
                raise ValueError("Rating should be between 1 and 10.")
        except ValueError as e:
            print(f"Invalid input for rating: {e}")
            return movies

        try:
            year_movie = int(input("Please enter the new year for that movie: "))
        except ValueError as e:
            print(f"Invalid input for year: {e}")
            return movies

        movies[movie_update] = {"rating": movie_rating, "year": year_movie}
        print(f"Movie '{movie_update}' has been updated to rating {movie_rating} and year {year_movie}")
    else:
        print(f"Movie '{movie_update}' not found in the database.")
    return movies

def rating_statistics(movies):
    """
    Calculate and display statistics for movie ratings.
    """
    if not movies:
        print("No movies found.")
        return

    # Filter valid ratings
    ratings = [movie_data['rating'] for movie_data in movies.values() if movie_data['rating'] is not None]
    if not ratings:
        print("No valid ratings found.")
        return

    # Calculate statistics
    average_rating = sum(ratings) / len(ratings)
    median_rating = median(ratings)
    best_movie = max(movies, key=lambda x: movies[x]['rating'])
    worst_movie = min(movies, key=lambda x: movies[x]['rating'])

    # results
    print(f"\nAverage rating: {average_rating:.2f}")
    print(f"Median rating: {median_rating:.2f}")
    print(f"Best movie: {best_movie} - Rating: {movies[best_movie]['rating']}")
    print(f"Worst movie: {worst_movie} - Rating: {movies[worst_movie]['rating']}")

def random_movie(movies):
    """
    Select and display a random movie from the collection.
    """
    if not movies:
        print("No movies available.")
        return None

    movie = random.choice(list(movies.items()))
    print(f"Randomly selected movie: {movie[0]} with a rating of {movie[1]['rating']}")
    return movie

def search_movie(movies):
    """
    Search for a movie by name in the collection.
    """
    movie_name = input("Please enter the movie you want to search: ").strip().lower()

    found = False
    for movie in movies:
        if movie_name in movie.lower():
            print(f"Movie '{movie}' found with rating {movies[movie]['rating']} and year {movies[movie]['year']}")
            found = True

    if not found:
        print(f"No movie found with '{movie_name}' in its title.")

def sort_movie_by_year(movies):
    """
    Sort movies by release year.
    """
    sorted_movies_year = sorted(movies.items(), key=lambda x: x[1]['year'], reverse=True)
    return sorted_movies_year

def sort_movie_by_rating(movies):
    """
    Sort movies by rating in descending order.
    """
    sorted_movies = sorted(movies.items(), key=lambda x: x[1]['rating'], reverse=True)
    return sorted_movies
