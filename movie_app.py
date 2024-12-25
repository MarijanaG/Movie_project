import requests
import os
from dotenv import load_dotenv
import movie_storage
from storage.storage_csv import StorageCsv

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv("OMDB_API_KEY")


class MovieApp:
    def __init__(self, storage):
        """Initialize the app with the given storage type.

        Args:
            storage: An instance of the storage class for managing movies.
        """
        self._storage = storage

    def run(self):
        movies = self.storage.list_movies()
        print(movies)

    def _command_list_movies(self):
        """List all movies in the storage.

        Retrieves movies from the storage and displays their title, rating, and year.
        """
        movies = self._storage.list_movies()
        if movies:
            for title, details in movies.items():
                print(f"{title}: {details['rating']} ({details['year']})")
        else:
            print("No movies found.")

    def _command_add_movie(self):
        """Add a movie by fetching data from the OMDb API.

        Prompts the user for a movie title, fetches its details from the OMDb API,
        and stores the movie details in the storage system.
        """
        api_key = os.getenv("OMDB_API_KEY")
        if not api_key:
            print("Error: API key not found. Please set OMDB_API_KEY in your .env file.")
            return

        title = input("Enter the movie title: ")
        url = f"http://www.omdbapi.com/?apikey={api_key}&t={title}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            # Handle if movie not found
            if data.get('Response') == 'False':
                print(f"Movie '{title}' not found in OMDb API.")
                return

            # Extract required fields
            movie_title = data.get('Title')
            year = data.get('Year')
            rating = data.get('imdbRating')
            poster = data.get('Poster')

            # Check if rating is valid and convert to float
            if rating and rating != "N/A":
                rating = float(rating)
            else:
                rating = None  # Handle case where rating is not available

            # Store movie details in your storage
            self._storage.add_movie(movie_title, year, rating, poster)
            print(f"Movie '{movie_title}' added successfully!")

        except requests.exceptions.RequestException as e:
            print(f"Error: Could not access the API. {e}")

    def _generate_website(self):
        """Generate an HTML file to display the list of movies.

        Creates a simple HTML page containing the list of movies stored in the system.
        """
        movies = self._storage.list_movies()

        # HTML template
        html_content = """
                <html>
                    <head>
                        <title>My Movie List</title>
                        <style>
                            body {
                                font-family: Arial, sans-serif;
                                background-color: #f4f4f9;
                                color: #333;
                                margin: 20px;
                            }
                            h1 {
                                text-align: center;
                            }
                            .movie {
                                border: 1px solid #ddd;
                                padding: 10px;
                                margin-bottom: 10px;
                                border-radius: 5px;
                                background-color: #fff;
                            }
                            .movie h2 {
                                margin: 0;
                            }
                            .movie p {
                                margin: 5px 0;
                            }
                        </style>
                    </head>
                    <body>
                        <h1>My Movie List</h1>
                """

        # Inject movie data into the HTML
        for title, info in movies.items():
            html_content += f"""
                        <div class="movie">
                            <h2>{title}</h2>
                            <p>Rating: {info['rating']}</p>
                            <p>Year: {info['year']}</p>
                        </div>
                    """

        # Closing HTML tags
        html_content += """
                    </body>
                </html>
                """

        # Write the HTML to a file
        with open("movie_list.html", "w") as file:
            file.write(html_content)

        print("Website generated successfully as 'movie_list.html'.")

    def run(self):
        """Run the main loop for the movie app.

        Displays a menu for the user to list movies, add a new movie, or quit the app.
        """
        while True:
            print("\nMenu:")
            print("1. List Movies")
            print("2. Add Movie")
            print("3. Generate Website")
            print("4. Quit")

            choice = input("Enter your choice: ")

            if choice == "1":
                self._command_list_movies()
            elif choice == "2":
                self._command_add_movie()
            elif choice == "3":
                self._generate_website()
            elif choice == "4":
                print("Exiting the app.")
                break
            else:
                print("Invalid choice, try again.")
