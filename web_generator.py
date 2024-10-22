def generate_website(movies):
    """
    Generate an HTML website listing all the movies in the collection.

    Args:
        movies (dict): The dictionary of movies to display on the website.
    """
    html_content = "<html><head><title>Movie List</title></head><body>"
    html_content += "<h1>Movie Collection</h1><ul>"

    for title, details in movies.items():
        html_content += f"<li>{title} - Rating: {details['rating']} (Year: {details['year']})</li>"

    html_content += "</ul></body></html>"

    with open('movies.html', 'w') as file:
        file.write(html_content)

    print("Website has been generated as 'movies.html'.")
