import statistics
import random
import requests
import pycountry

from storage import movie_storage_sql as storage

API_KEY = "c64b151d"
DATA_URL = f"http://www.omdbapi.com/?apikey={API_KEY}"
POSTER_URL = f"http://img.omdbapi.com/?apikey={API_KEY}"
STATIC_DIR = "_static"
TEMPLATE_FILE = f"{STATIC_DIR}/index_template.html"
OUTPUT_FILE = f"{STATIC_DIR}/index.html"


def command_list_movies():
    """Retrieve and display all movies from the database."""
    movies = storage.list_movies()
    print(f"{len(movies)} movies in total: \n")

    for movie, data in movies.items():
        print(f"{movie}: {data['rating']} ({data['year']})")


def command_add_movie():
    """Adds a movie to the database."""

    # Creates a valid input for title
    while True:
        title = input("Enter new movie name: ").strip()
        if title:
            break
        print("Movie name cannot be blank.")

    params = {"t": title}

    try:
        request = requests.get(DATA_URL, params)
        response = request.json()

        if response.get("Response") == "False":
            print("Movie does not exist.")
            return

        poster = response["Poster"]
        title = response["Title"]
        year = int(response["Year"])
        rating = float(response["imdbRating"])
        country = response["Country"]
        country = country.split(",")[0].strip()

        flag_url = command_get_flag(country)
        result = storage.add_movie(title, year, rating, poster, country, flag_url)
        if result is True:
            print(f"Movie {title} successfully added.")
        elif result is False:
            print(f"The movie '{title}' is already in the collection.")
        else:
            print("An unexpected error occurred while adding the movie.")

    except (KeyError, ValueError, requests.exceptions.RequestException):
        print("There was a problem accessing movie data.")


def command_del_movie():
    """Deletes a movie from the database."""

    while True:
        title = input("Enter the name of the movie to delete: ").strip()
        if not title:
            print("Movie name cannot be blank.")
            continue

        movies = storage.list_movies()
        if title in movies:
            storage.delete_movie(title)
            print(f"Movie {title} successfully deleted.")
            break

        print(f"The movie '{title}' is not in the collection. Try again.")


def command_update_movie():
    """Updates the rating of a movie in the database."""
    movies = storage.list_movies()
    # Input validation for the movie title
    while True:
        title = input("Enter movie name: ").strip()
        if title:
            break
        print("Movie name cannot be blank.")

    if title not in movies:
        print(f"The movie {title} is not inside the collection.")
        return

    # Creates a valid input for new rating
    while True:
        try:
            rating = float(input("Enter new movie rating (0-10): "))
            if 0 <= rating <= 10:
                break
            print("Rating must be between 0 and 10.")
        except ValueError:
            print("Please enter a valid number.")

    storage.update_movie(title, rating)
    print(f"Movie {title} successfully updated.")


def command_average_rating(movies):
    """Calculates and prints the average rating of all movies in the collection."""
    sum_rating = 0

    for _, data in movies.items():
        sum_rating += data["rating"]
    aver_rating = sum_rating / len(movies)
    print(f"Average rating: {round(aver_rating, 1)} ")


def command_median_ratings(movies):
    """Calculates and prints the median rating of all movies in the collection."""
    median_list = []
    for _, data in movies.items():
        median_list.append(data["rating"])
    median_rating = statistics.median(median_list)
    print(f"Median rating: {median_rating} ")


def command_best_movie_rating(movies):
    """Finds and prints the movie with the highest rating."""
    best_rating = 0
    for movie, data in movies.items():
        if data["rating"] > best_rating:
            best_rating = data["rating"]
    for movie, data in movies.items():
        if best_rating == data["rating"]:
            print(f"Best movie: {movie}, {data['rating']}")


def command_worst_movie_rating(movies):
    """Finds and prints the movie with the lowest rating."""
    worst_rating = 10
    for movie, data in movies.items():
        if data["rating"] < worst_rating:
            worst_rating = data["rating"]
    for movie, data in movies.items():
        if worst_rating == data["rating"]:
            print(f"Worst movie: {movie}, {data['rating']}")


def command_random_movie(movies):
    """Randomly selects and prints a movie recommendation from the collection."""
    movie, data = random.choice(list(movies.items()))
    print(f"Your movie for tonight: {movie}, it's rated {data['rating']}")


def command_search_movie(movies):
    """Prompts the user for a search term and lists matching movie titles."""
    while True:
        get_movie_part = input("Enter part of movie name: ").strip()
        print()
        if not get_movie_part:
            print("Movie name cannot be blank.")
            print()
            continue

        found = False
        for movie in movies:
            if get_movie_part.lower() in movie.lower():
                print(movie)
                found = True
        if not found:
            print("No matching movies found.")
        break


def command_movies_sorted_by_rating(movies):
    """Prints all movies sorted in descending order by rating."""
    sorted_movies = sorted(
        movies.items(), key=lambda pair: pair[1]["rating"], reverse=True
    )
    for movie, data in sorted_movies:
        print(f"{movie}: {data['rating']}")


def command_generate_website(movies):
    """Generates an HTML page with all movies from the database."""

    movie_grid_html = ""

    # generate HTML blocks from movies
    for title, data in movies.items():
        year = data["year"]
        poster = data["poster"]
        flag_url = data["flag_url"]
        country = data["country"]

        html_block = f"""
        <li>
          <div class="movie">
            <img class="movie-poster" src="{poster}" alt="{title} Poster">
            <div class="movie-title">
              {title}
              <img class="flag-icon" src="{flag_url}" alt="" />
            </div>
            <div class="movie-year">{year}</div>
          </div>
        </li>
        """
        movie_grid_html += html_block

    # read template
    with open(TEMPLATE_FILE, "r", encoding="utf-8") as fileobj:
        data = fileobj.read()

    # replace template
    html_with_title = data.replace("__TEMPLATE_TITLE__", "My Movie Collection")
    final_html = html_with_title.replace("__TEMPLATE_MOVIE_GRID__", movie_grid_html)

    # save HTML
    with open(OUTPUT_FILE, "w", encoding="utf-8") as fileobj:
        fileobj.write(final_html)

    print("Website was generated successfully.")


def get_country_code(country_name):
    try:
        country = pycountry.countries.search_fuzzy(country_name)[0]
        return country.alpha_2
    except LookupError:
        print(f"Country code for '{country_name}' not found.")
        return None


def command_get_flag(country):
    """Fetches a country flag URL for a given country name."""

    code = get_country_code(country)
    if not code:
        return None

    country_url = f"https://api.api-ninjas.com/v1/countryflag?country={code}"
    response = requests.get(
        country_url, headers={"X-Api-Key": "QCeokNY12dIlVFN9Tve2DA==nqesixzrPLu1QRcn"}
    )
    if response.status_code == requests.codes.ok:
        flag_data = response.json()
        if isinstance(flag_data, dict) and "rectangle_image_url" in flag_data:
            return flag_data["rectangle_image_url"]
        else:
            print("Unexpected flag API response format.")
            return None

    print("Error fetching flag from API.")
    return None


def get_menu_choice(max_choice):
    while True:
        try:
            choice = int(input(f"Enter choice (0–{max_choice}): "))
            print()
            if 0 <= choice <= max_choice:
                return choice
            print(f"Number must be between 0 and {max_choice}.")
        except ValueError:
            print("Please enter a valid number.")


def main():
    """Main program loop for displaying the menu and executing user-selected actions."""

    while True:
        print("Menu:")
        print("0. Exit")
        print("1. List movies")
        print("2. Add movie")
        print("3. Delete movie")
        print("4. Update movie")
        print("5. Stats")
        print("6. Random movie")
        print("7. Search movie")
        print("8. Movies sorted by rating")
        print("9. Generate website")
        print()

        selected_number = get_menu_choice(9)

        movies = storage.list_movies()

        MENU_ACTIONS = {
            1: command_list_movies,
            2: command_add_movie,
            3: command_del_movie,
            4: command_update_movie,
            5: lambda: (
                command_average_rating(movies),
                command_median_ratings(movies),
                command_best_movie_rating(movies),
                command_worst_movie_rating(movies),
            ),
            6: lambda: command_random_movie(movies),
            7: lambda: command_search_movie(movies),
            8: lambda: command_movies_sorted_by_rating(movies),
            9: lambda: command_generate_website(movies),
        }

        if selected_number == 0:
            print("Bye!")
            break

        action = MENU_ACTIONS.get(selected_number)
        if action:
            action()

        input("\nPress Enter to continue")


if __name__ == "__main__":
    main()