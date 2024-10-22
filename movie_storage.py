import json


"""Read and load movies from JSON file"""


def get_movies():
    try:
        with open('data.json', 'r') as file:
            movies = json.load(file)
    except FileNotFoundError:
        movies = {}  
    return movies


"""Gets all movies as an argument and saves to the JSON file."""


def save_movies(movies):
    with open('data.json', 'w') as file:
        json.dump(movies, file, indent=4)
    print("Movies data saved successfully.")


"""Adding movies with title rating and a year in a list"""


def add_movie(title, year, rating):
    movies = get_movies()
    if title in movies:
        print(f"Warning: '{title}' already exists. It will be overwritten.")
    movies[title] = {"rating": rating, "year": year}
    save_movies(movies)
    print(f"Added movie: '{title}' with rating {rating} and year {year}.")


"""Deleting movie from the list"""


def delete_movie(title):
    movies = get_movies()
    if title in movies:
        del movies[title]
        save_movies(movies)
        print(f"Deleted movie: '{title}'.")
    else:
        print(f"Error: Movie '{title}' not found.")


"""Update movie by title and a new rating"""


def update_movie(title, rating):
    movies = get_movies()
    if title in movies:
        movies[title]["rating"] = rating
        save_movies(movies)
        print(f"Updated movie: '{title}' with new rating {rating}.")
    else:
        print(f"Error: Movie '{title}' not found.")
