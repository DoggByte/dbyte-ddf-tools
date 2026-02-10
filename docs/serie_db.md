# serie_db.py Documentation
# Requirements

To use `serie_db.py` and the `SerieDB` class, the following requirements must be met:

- **Python Version**: Python 3.6 or higher.
- **Database File**: The JSON file (default: `db/serie.json`) must exist and be readable. It should contain a top-level key `serie` with a list of dictionaries, each representing a series entry.
- **Entry Format**: Each entry should have at least a `nummer` (int) and `titel` (str). Additional fields are supported.
- **Write Permissions**: To add or update entries, the user must have write permissions to the JSON file.


## Overview

`serie_db.py` provides the `SerieDB` class, a simple Python interface for managing a collection of audio series (such as "Die Drei ???") stored in a JSON file. It supports loading, querying, searching, and updating the series database.

## Features

- Loads series data from a JSON file (default: `db/serie.json`).
- Retrieves all series entries.
- Looks up a series by its track number (`nummer`).
- Searches for series by (partial) title.
- Adds new series entries and saves them to the database.

## Class: SerieDB

### Initialization

```python
db = SerieDB(json_path)
```
- `json_path`: Path to the JSON file containing the series database.

### Methods

#### get_all_series()
- **Returns:** `List[Dict[str, Any]]`
- **Description:** Returns a list of all series entries in the database.

#### get_serie_by_nummer(nummer)
- **Arguments:**
  - `nummer` (`int`): The track number of the series to retrieve.
- **Returns:** `Optional[Dict[str, Any]]`
- **Description:** Returns the series entry with the given track number, or `None` if not found.

#### search_by_title(title)
- **Arguments:**
  - `title` (`str`): The (partial) title to search for (case-insensitive).
- **Returns:** `List[Dict[str, Any]]`
- **Description:** Returns a list of series entries whose titles contain the given string.

#### add_serie(serie)
- **Arguments:**
  - `serie` (`Dict[str, Any]`): The new series entry to add.
- **Description:** Appends the new series entry to the database and saves the updated data to the JSON file.

## Data Format

The JSON file should have the following structure:

```json
{
  "serie": [
    {
      "nummer": 1,
      "titel": "...",
      ...
    },
    ...
  ]
}
```

## Example Usage

```python
from serie_db import SerieDB

db = SerieDB('db/serie.json')

# Get all series
episodes = db.get_all_series()

# Search by title
results = db.search_by_title('Papagei')

# Get by nummer
episode = db.get_serie_by_nummer(1)

# Add a new series
db.add_serie({"nummer": 999, "titel": "Test Episode"})
```

## Command-Line Example

If run as a script, prints:
- The first series title
- All series with "Papagei" in the title
- The series with track number 1

## Dependencies

- Python 3.x
- Standard library: `json`, `typing`

## License

This script is provided as-is. Ensure you have appropriate rights to modify and use the series database.
