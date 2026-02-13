# db2scaffold.py Documentation
# Requirements

To use `db2scaffold.py`, ensure the following requirements are met:

- **Python Version**: Python 3.6 or higher.
- **Input Database**: The file `db/serie.json` must exist and be a valid JSON file with a top-level key `serie` containing a list of episode dictionaries. Each episode should have at least a `nummer` (int) and `titel` (str).
- **Template File**: The template file `templates/tmpl_episode_info.txt` must exist and be readable. It should contain valid Python string formatting placeholders for the episode metadata.
- **Output Directory**: The script will create the `dist/` directory and subfolders as needed. The user must have write permissions to the project directory.
- **Internet Access**: To download cover art, the machine must have internet access and the URLs in the database must be reachable.
- **File Overwrite**: Output files in `dist/` will be overwritten if they already exist.


## Overview

`db2scaffold.py` is a Python script designed to automate the process of generating structured output folders and metadata files for a collection of audio series episodes. It reads episode data from a JSON database, processes each entry, and creates a corresponding folder structure with metadata, cover art, and summary files. This is particularly useful for organizing large audio collections, such as the German series "Die Drei ???".

## Features

- Loads episode data from a JSON database (`db/serie.json`).
- Sorts episodes by track number (`nummer`).
- Generates folder-friendly names for each episode, handling German umlauts and special characters.
- Downloads cover art for each episode if available.
- Creates an `info.txt` file in each episode folder using a customizable template (`tmpl_episode_info.txt`).
- Outputs summary files listing folder names, original titles, cover art URLs, and episode durations.

## Folder Structure

- `dist/` — Output directory containing:
  - One folder per episode, named as `<nummer_str> - <titel_folder>`
  - Each episode folder contains:
    - `info.txt` — Metadata file for the episode
    - `<nummer_str>.jpg` — Cover art (if available)
- `dist/folder-names.txt` — List of all generated folder names
- `dist/titles.txt` — List of original episode titles
- `dist/cover-art-urls.txt` — List of cover art URLs
- `dist/episodes-time-ms.txt` — List of episode durations in milliseconds

## Usage

Run the script from the project root:

```bash
python3 db2scaffold.py
```

Ensure the following files exist:
- `db/serie.json` — The main database of episodes
- `tmpl_episode_info.txt` — The template for the `info.txt` files

## Main Steps

1. **Load Database**: Uses the `SerieDB` class from `serie_db.py` to load episode data from `db/serie.json`.
2. **Sort Episodes**: Sorts all episodes by their track number (`nummer`).
3. **Prepare Template**: Reads the `info.txt` template from `tmpl_episode_info.txt`, removing any non-parsable documentation section.
4. **Process Each Episode**:
   - Extracts metadata (number, title, description, duration, cover art URL).
   - Expands German umlauts in titles for folder names.
   - Removes special characters from folder names.
   - Creates a folder for each episode in `dist/`.
   - Downloads cover art if a URL is provided and the file does not already exist.
   - Writes an `info.txt` file in each folder using the template and episode metadata.
5. **Write Summary Files**: Outputs lists of folder names, titles, cover art URLs, and durations to text files in `dist/`.

## Key Functions and Utilities

- **expand_umlauts(text)**: Replaces German umlauts and ß with their ASCII equivalents for folder naming (imported from `utils.py`).
- **write_file(path, content)**: Utility to write content to a file with UTF-8 encoding (imported from `utils.py`).
- **Template Handling**: Reads and processes the `tmpl_episode_info.txt` template, supporting a split marker to ignore documentation sections.
- **Folder and File Creation**: Uses `os.makedirs` to create folders and `urllib.request.urlretrieve` to download cover art.

## Customization

- **Template**: Modify `tmpl_episode_info.txt` to change the format of the `info.txt` files.
- **Database**: Update `db/serie.json` to add or edit episode data.

## Error Handling

- Skips downloading cover art if the file already exists.
- Prints errors if cover art download fails.
- Handles missing or `None` values for episode duration and cover art URLs.

## Example Output Structure

```
dist/
├── 001 - Die Drei ??? und der Super-Papagei/
│   ├── info.txt
│   └── 001.jpg
├── 002 - Die Drei ??? und .../
│   ├── info.txt
│   └── 002.jpg
├── folder-names.txt
├── titles.txt
├── cover-art-urls.txt
└── episodes-time-ms.txt
```

## Dependencies

- Python 3.6+
- Standard library modules: `os`, `re`, `urllib.request`, `socket`, `logging`
- Local modules: 
  - `serie_db.py` (provides `SerieDB` class and `Serie` type)
  - `utils.py` (provides `expand_umlauts` and `write_file` utilities)

## License

This script is provided as-is. Please ensure you have the rights to download and use any cover art referenced in your database.
