import json


def get_movies():
    """Load and return all movies from the JSON file."""
    with open("data.json", "r") as fileobj:
        data = json.load(fileobj)
        return data


def save_movies(movies):
    """Save the given movies dictionary to the JSON file."""
    with open("data.json", "w") as fileobj:
        json.dump(movies, fileobj, indent=4)


def add_movie(title, rating, year_of_release):
    """Add a new movie with rating and release year to the JSON file."""
    with open("data.json", "r") as fileobj:
        data = json.load(fileobj)

        # Adds the new movie to the dictionary
        data[title] = {"rating": rating, "year_of_release": year_of_release}

        # Save the updated movie list
        with open("data.json", "w") as fileobj:
            json.dump(data, fileobj, indent=4)


def delete_movie(title):
    """Delete a movie by title from the JSON file."""
    with open("data.json", "r") as fileobj:
        data = json.load(fileobj)

    if title in data:
        del data[title]

    with open("data.json", "w") as fileobj:
        json.dump(data, fileobj, indent=4)


def update_movie(title, rating):
    """Update the rating of an existing movie in the JSON file."""
    with open("data.json", "r") as fileobj:
        data = json.load(fileobj)

        if title in data:
            data[title]["rating"] = rating

        with open("data.json", "w") as fileobj:
            json.dump(data, fileobj, indent=4)
