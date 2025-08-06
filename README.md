# Movie Website Generator

This project allows you to store and display your favorite movies in a simple website, including poster, year and
rating.

## Features

- Add movies manually or via OMDb API
- Store movies in SQLite
- Generate a responsive HTML website

## Purpose

This project was created as part of a software development training to practice:

- Working with files and folders
- Connecting to APIs (OMDb)
- Handling SQLite databases
- Building dynamic HTML with Python
- Managing real-world project structure

## Setup

1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `python main.py`

## Example Usage

Run the app and follow the menu:

1. Add movie → “Inception”
2. The app will create a new database file in /data/movies.db when run for the first time.
3. Generate website
4. Open index.html in your browser

You’ll see a fully styled movie card including year, poster and rating.

## Folder Structure

- `data/` → your SQLite database
- `static/` → HTML/CSS website files
- `storage/` → Python modules for saving/loading data