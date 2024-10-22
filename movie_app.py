import requests
class MovieApp:
    def __init__(self, storage):
        """Initialize the app with the given storage type."""
        self._storage = storage

    def _command_list_movies(self):
        """List all movies in the storage."""
        movies = self._storage.list_movies()
        if movies:
            for title, details in movies.items():
                print(f"{title}: {details['rating']} ({details['year']})")
        else:
            print("No movies found.")

    def _command_add_movie(self):
        """Add a movie by fetching data from the OMDb API."""
        api_key = "73a25159"
        title = input("Enter the movie title: ")
        url = f"http://www.omdbapi.com/?apikey={api_key}&t={title}"

        try:
            response = requests.get(url)
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
            self._storage.add_movie(movie_title, year, rating,
                                    poster)  # Ensure this method exists in your storage class
            print(f"Movie '{movie_title}' added successfully!")

        except requests.exceptions.RequestException as e:
            print(f"Error: Could not access the API. {e}")

    def run(self):
        """Run the main loop for the movie app."""
        while True:
            print("\nMenu:")
            print("1. List Movies")
            print("2. Add Movie")
            print("3. Quit")

            choice = input("Enter your choice: ")

            if choice == "1":
                self._command_list_movies()
            elif choice == "2":
                self._command_add_movie()
            elif choice == "3":
                print("Exiting the app.")
                break
            else:
                print("Invalid choice, try again.")


    def _generate_website(self):
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
        """Run the main loop for the movie app."""
        while True:
            print("\nMenu:")
            print("1. List Movies")
            print("2. Add Movie")
            print("3. Quit")

            choice = input("Enter your choice: ")

            if choice == "1":
                self._command_list_movies()
            elif choice == "2":
                self._command_add_movie()
            elif choice == "3":
                print("Exiting the app.")
                break
            else:
                print("Invalid choice, try again.")



