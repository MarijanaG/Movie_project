from movies import main as movies_main
from storage_json import StorageJson


def main():
    """
    Main function to initialize the movie storage and run the movie management application.
    """
    storage = StorageJson('data.json')
    movies_main(storage)


if __name__ == "__main__":
    main()
