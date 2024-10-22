import json
import random
from statistics import median
from movie_storage import get_movies, save_movies
from storage_json import StorageJson
from web_generator import generate_website

JSON_FILE = "data.json"


def load_movies_from_storage():
    """
    Load movies from the JSON storage.

    Returns:
        dict: A dictionary of movies.
    """
    with open(JSON_FILE, 'r') as file:
        movies = json.load(file)
    return movies


def list_movie(movies):
    """
    List all movies and their details in a formatted way.

    Args:
        movies (dict): The dictionary of movies.

    Returns:
        list: A list of movie details as strings.
    """
    movie_list = []
    for title, details in movies.items():
        movie_info = f"{title} - Rating: {details['rating']} (Year: {details['year']})"
        movie_list.append(movie_info)
    return movie_list


def add_movie(movies):
    """
    Add a new movie to the collection.

    Args:
        movies (dict): The current movie dictionary.

    Returns:
        dict: Updated movie dictionary.
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
    return movies


def delete_movie(movies):
    """
    Delete a movie from the collection.

    Args:
        movies (dict): The current movie dictionary.

    Returns:
        dict: Updated movie dictionary.
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

    Args:
        movies (dict): The current movie dictionary.

    Returns:
        dict: Updated movie dictionary.
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

    Args:
        movies (dict): The current movie dictionary.
    """
    if not movies:
        print("No movies found.")
        return

    ratings = [movie_data['rating'] for movie_data in movies.values()]
    average_rating = sum(ratings) / len(ratings)
    median_rating = median(ratings)
    best_movie = max(movies, key=lambda x: movies[x]['rating'])
    worst_movie = min(movies, key=lambda x: movies[x]['rating'])

    print(f"\nAverage rating: {average_rating:.2f}")
    print(f"Median rating: {median_rating:.2f}")
    print(f"Best movie: {best_movie} - Rating: {movies[best_movie]['rating']}")
    print(f"Worst movie: {worst_movie} - Rating: {movies[worst_movie]['rating']}")


def random_movie(movies):
    """
    Select and display a random movie from the collection.

    Args:
        movies (dict): The current movie dictionary.

    Returns:
        tuple: The randomly selected movie.
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

    Args:
        movies (dict): The current movie dictionary.
    """
    movie_name = input("Please enter the movie you want to search: ").strip().lower()

    found = False
    for movie in movies:
        if movie_name in movie.lower():
            print(f"Movie '{movie}' found with rating {movies[movie]['rating']} and year {movies[movie]['year']}")
            found = True

    if not found:
        print(f"No movie found with '{movie_name}' in its title.")


def sort_movie_by_rating(movies):
    """
    Sort movies by rating in descending order.

    Args:
        movies (dict): The current movie dictionary.

    Returns:
        list: A sorted list of movies by rating.
    """
    sorted_movies = sorted(movies.items(), key=lambda x: x[1]['rating'], reverse=True)
    return sorted_movies


def initialize_movies(storage):
    """
    Initialize the movie collection by loading data from storage.

    Args:
        storage (IStorage): The storage system to use.

    Returns:
        dict: A dictionary of movies.
    """
    return storage.list_movies()


def main(storage):
    """
    Main function to run the movie application.

    Args:
        storage (IStorage): The storage system to use.
    """
    movies = initialize_movies(storage)

    while True:
        print("\n0. Exit\n"
              "1. List Movies\n"
              "2. Add Movie\n"
              "3. Delete Movie\n"
              "4. Update Movie\n"
              "5. Statistics\n"
              "6. Random Movie\n"
              "7. Search Movie\n"
              "8. Movies sorted by rating\n"
              "9. Generate website\n"
              )

        user_choice = input("Choose from the menu: ").strip()
        if user_choice == "1":
            movie_list = list_movie(movies)
            for movie in movie_list:
                print(movie)
        elif user_choice == "2":
            movies = add_movie(movies)
        elif user_choice == "3":
            movies = delete_movie(movies)
        elif user_choice == "4":
            movies = update_movies(movies)
        elif user_choice == "5":
            rating_statistics(movies)
        elif user_choice == "6":
            random_movie(movies)
        elif user_choice == "7":
            search_movie(movies)
        elif user_choice == "8":
            sorted_movies = sort_movie_by_rating(movies)
            for movie, details in sorted_movies:
                print(f"{movie}: {details['rating']} (Year: {details['year']})")
        elif user_choice == "9":
            generate_website(movies)

        elif user_choice == "0":
            print("Saving changes and exiting...")
            storage.add_movie(movies)
            break
        else:
            print("Invalid input. Please choose again.")


# The storage system you want to use
storage = StorageJson('movies.json')

# Running the main program
if __name__ == "__main__":
    main(storage)
