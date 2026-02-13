# db2rows.py Documentation
# Requirements

The following requirements must be met to use `db2rows.py` successfully:

- **Python Version**: Python 3.6 or higher.
- **Input File**: The file `db/serie.json` is the default input. It is automatically created if it doesn't exist (see `serie_db.py` documentation). It should contain a top-level key `serie` with a list of entries. Each entry should have a unique integer `nummer` field (1-3 digits).
- **Output Directory**: The script will create the output directory `db/rows/` if it does not exist. The user must have write permissions to the `db/` directory.
- **Entry Format**: Each entry in the `serie` list should be a dictionary. Only entries with a valid `nummer` (1-3 digits) will be processed.
- **File Overwrite**: Output files in `db/rows/` will be overwritten if they already exist.


## Overview

`db2rows.py` is a Python script that reads a JSON file containing a list of series entries and splits each entry into a separate, compact JSON file. Each output file is named according to the `nummer` field of the entry, zero-padded to three digits (e.g., `001.json`).

## How It Works

1. **Input and Output Paths**
   - Reads from: `db/serie.json`
   - Writes to: `db/rows/` (creates the directory if it doesn't exist)

2. **Processing Steps**
   - Loads the JSON data from `serie.json`.
   - Iterates over each entry in the `serie` list.
   - For each entry:
     - Extracts the `nummer` field.
     - Skips entries without a valid `nummer` (must be 1-3 digits).
     - Constructs a filename as a zero-padded 3-digit number (e.g., `007.json`).
     - Writes the entry to the output file in compact JSON format (no extra spaces or line breaks).

3. **Security**
   - Sanitizes the `nummer` to prevent path injection.
   - Ensures filenames are strictly numeric and follow the `NNN.json` pattern.

## Usage

Run the script from the command line:

```bash
python3 db2rows.py
```

## Example

Given an input `db/serie.json` like:

```json
{
  "serie": [
    {"nummer": 1, "title": "Episode 1"},
    {"nummer": 2, "title": "Episode 2"}
  ]
}
```

The script will create:
- `db/rows/001.json`
- `db/rows/002.json`

Each file will contain the corresponding entry in compact JSON format.

## Dependencies

- Python 3.6+
- Standard library modules: `json`, `os`, `re`, `logging`
- Local modules: `serie_db.py` (provides `SerieDB` class)

## Notes
- Only entries with a valid `nummer` (1-3 digits) are processed.
- Output files are overwritten if they already exist.
- Output JSON is compact (no indentation, minimal whitespace).
