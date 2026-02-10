# Die Drei ??? Collection Tools

This project provides a set of Python tools to help you organize and manage your collection of "Die Drei ???" audio series. It is designed to automate the process of splitting, structuring, and documenting your episode database, making it easier to browse, archive, and enjoy your collection.

## Features

- **Database Management:** Load, search, and update your episode database with simple Python scripts.
- **Episode Splitting:** Automatically split a master JSON database into individual episode files for easier access and management.
- **Folder Structuring:** Generate organized folders for each episode, complete with metadata and cover art.
- **Custom Metadata:** Use templates to create detailed info files for each episode.

## Requirements

- Python 3.6 or higher
- A valid `db/serie.json` file containing your episode data

## Documentation

See the `docs/` directory for detailed documentation on each tool:
- `db2rows.md`: Split your database into per-episode files
- `db2scaffold.md`: Generate folders and metadata for each episode
- `serie_db.md`: Python interface for managing your database

## Getting Started
## Available Scripts

| Script            | Description                                                                 |
|-------------------|-----------------------------------------------------------------------------|
| db2rows.py        | Splits the master database (`db/serie.json`) into individual episode files in `db/rows/`, one JSON file per episode. |
| db2scaffold.py    | Generates a structured folder for each episode in `dist/`, including metadata (`info.txt`) and cover art (if available), using a customizable template. |
| serie_db.py       | Provides the `SerieDB` class for loading, searching, and updating the episode database. Can be used as a library or run directly for basic queries. |

1. Place your `serie.json` database in the `db/` folder.
2. Run the provided scripts as described in the documentation.
3. Enjoy a well-organized and documented collection of "Die Drei ???" episodes!

---

This project is not affiliated with the official "Die Drei ???" series. Please ensure you have the rights to use and distribute any cover art or episode data.

This is a work in progress !
