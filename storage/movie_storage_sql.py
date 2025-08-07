from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError

# Define the database URL
DB_URL = "sqlite:///data/movies.db"

# Create the engine
engine = create_engine(DB_URL)

# Create the movies table if it does not exist
with engine.connect() as connection:
    connection.execute(
        text(
            """
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            year INTEGER NOT NULL,
            rating REAL NOT NULL,
            poster TEXT,
            country TEXT,
            flag_url TEXT
        )
    """
        )
    )
    connection.commit()


def list_movies():
    """Retrieve all movies from the database."""
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT title, year, rating, poster, country, flag_url FROM movies")
        )
        movies = result.fetchall()

    return {
        row[0]: {
            "year": row[1],
            "rating": row[2],
            "poster": row[3],
            "country": row[4],
            "flag_url": row[5],
        }
        for row in movies
    }


def add_movie(title, year, rating, poster, country, flag_url):
    """Add a new movie to the database.

    Returns:
        True if the movie was added,
        False if it already exists,
        None if an unexpected error occurred.
    """
    try:
        with engine.connect() as connection:
            connection.execute(
                text(
                    "INSERT INTO movies (title, year, rating, poster, country, flag_url) "
                    "VALUES (:title, :year, :rating, :poster, :country, :flag_url)"
                ),
                {
                    "title": title,
                    "year": year,
                    "rating": rating,
                    "poster": poster,
                    "country": country,
                    "flag_url": flag_url,
                },
            )
            connection.commit()
        return True
    except IntegrityError:
        return False
    except Exception as e:
        print(f"Error while adding movie: {e}")
        return None


def delete_movie(title):
    """Delete a movie from the database."""
    with engine.connect() as connection:
        try:
            connection.execute(
                text("DELETE FROM movies WHERE title = :title"),
                {"title": title},
            )
            connection.commit()
            print(f"Movie '{title}' deleted successfully.")
        except Exception as e:
            print(f"Error: {e}")


def update_movie(title, rating):
    """Update a movie's rating in the database."""
    with engine.connect() as connection:
        try:
            connection.execute(
                text("UPDATE movies SET rating = :rating WHERE title = :title"),
                {"title": title, "rating": rating},
            )
            connection.commit()
            print(f"Movie '{title}' updated successfully.")
        except Exception as e:
            print(f"Error: {e}")
