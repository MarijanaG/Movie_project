def generate_website(movies):
    """
    Generate an HTML website listing all the movies in the collection.

    Args:
        movies (dict): The dictionary of movies to display on the website.
    """
    # Start HTML structure with basic styling
    html_content = """
    <html>
    <head>
        <title>Movie List</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #f4f4f4;
            }
            h1 {
                text-align: center;
                color: #333;
            }
            ul {
                list-style-type: none;
                padding: 0;
            }
            li {
                padding: 10px;
                background-color: #fff;
                margin: 5px 0;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
            li:hover {
                background-color: #f1f1f1;
                cursor: pointer;
            }
            @media (max-width: 600px) {
                body { padding: 10px; }
                h1 { font-size: 1.5em; }
            }
        </style>
    </head>
    <body>
        <h1>Movie Collection</h1>
        <ul>
    """

    # Adding each movie as a list item in HTML
    for title, details in movies.items():
        html_content += f"<li><strong>{title}</strong> - Rating: {details['rating']} (Year: {details['year']})</li>"

    # Close the list and HTML tags
    html_content += """
        </ul>
    </body>
    </html>
    """

    # Try writing to file with error handling
    try:
        with open('movies.html', 'w') as file:
            file.write(html_content)
        print("Website has been generated as 'movies.html'.")
    except Exception as e:
        print(f"Error writing file: {e}")
