import os
import socket
import logging
import re
import urllib.request
import urllib.error
from typing import List, Dict, Any, Optional

from serie_db import SerieDB
from utils import expand_umlauts, write_file

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

CONFIG = {
    'db_path': os.getenv('DDF_DB_PATH', 'db/serie.json'),
    'output_dir': os.getenv('DDF_SCAFFOLD_DIR', 'dist'),
    'template_path': os.getenv('DDF_TEMPLATE_PATH', 'templates/tmpl_episode_info.txt'),
    'chapter_template_path': os.getenv('DDF_CHAPTER_TEMPLATE_PATH', 'templates/tmpl_episodes_chapters.txt'),
    'split_marker': '---\nDO NOT PARSE BELOW THIS LINE'
}


def load_template(path: str) -> str:
    """Reads and parses the template file, removing documentation sections."""
    try:
        with open(path, 'r', encoding='utf-8') as tmpl_file:
            content = tmpl_file.read()

        if CONFIG['split_marker'] in content:
            return content.split(CONFIG['split_marker'])[0].rstrip()
        return content
    except FileNotFoundError:
        logger.error(f"Template file not found: {path}")
        raise
    except Exception as e:
        logger.error(f"Error reading template {path}: {e}")
        raise


def get_info_title(nummer: int, titel: str) -> str:
    """Composes the formatted info title."""
    prefix = f"{nummer}. "
    if titel.strip().lower().startswith("und"):
        return f"{prefix}Die Drei ??? {titel}"
    return f"{prefix}Die Drei ??? - {titel}"


def get_folder_name(nummer_str: str, titel: str) -> str:
    """Creates a folder name friendly version of the title."""
    titel_expanded = expand_umlauts(titel)
    # Remove special characters except spaces, preserve case
    titel_sanitized = re.sub(r'[^a-zA-Z0-9 ]', '', titel_expanded)
    return f"{nummer_str} - {titel_sanitized}"


def download_cover(url: str, dest_path: str, identifier: str):
    """Downloads cover art if it doesn't exist."""
    if os.path.exists(dest_path):
        logger.info(f"Cover art already exists for {identifier}, skipping download.")
        return

    try:
        urllib.request.urlretrieve(url, dest_path)
        logger.info(f"Downloaded cover art for {identifier} to {dest_path}")
    except (urllib.error.URLError, urllib.error.HTTPError, socket.timeout) as e:
        logger.warning(f"Failed to download cover art for {identifier}: {e}")
    except Exception as e:
        logger.error(f"Unexpected error downloading cover art for {identifier}: {e}")
        raise


def main():
    try:
        db = SerieDB(CONFIG['db_path'])
    except Exception as e:
        logger.error(f"Failed to load database: {e}")
        return

    series = sorted(db.get_all_series(), key=lambda s: s.get('nummer', 0))
    tmpl_episode_info = load_template(CONFIG['template_path'])
    tmpl_chapters = load_template(CONFIG['chapter_template_path'])

    # Ensure output directory exists
    os.makedirs(CONFIG['output_dir'], exist_ok=True)

    outputs = []
    titles = []
    cover_art_urls = []
    episode_durations = []

    for serie in series:
        nummer = serie.get('nummer', 0)
        titel = serie.get('titel', '')
        nummer_str = str(nummer).zfill(3)
        gesamtdauer = serie.get('gesamtdauer')  # Can be None
        beschreibung = serie.get('beschreibung', '')

        # Collect data for summary files
        episode_durations.append(str(gesamtdauer) if gesamtdauer is not None else '')
        titles.append(titel)

        links = serie.get('links', {})
        cover_art_url = links.get('cover', '') if isinstance(links, dict) else ''
        cover_art_urls.append(cover_art_url)

        # Process title and folder name
        info_titel = get_info_title(nummer, titel)
        folder_name = get_folder_name(nummer_str, titel)
        outputs.append(folder_name)

        # Duration conversion
        gesamtdauer_min = int(gesamtdauer) // 60000 if gesamtdauer is not None else 0

        # Create folder
        folder_path = os.path.join(CONFIG['output_dir'], folder_name)
        os.makedirs(folder_path, exist_ok=True)

        # Download cover
        if cover_art_url:
            cover_path = os.path.join(folder_path, f'{nummer_str}.jpg')
            download_cover(cover_art_url, cover_path, folder_name)

        # Write info.txt
        info_path = os.path.join(folder_path, 'info.txt')
        try:
            episode_info = tmpl_episode_info.format(
                nummer=nummer,
                nummer_str=nummer_str,
                titel=titel,
                beschreibung=beschreibung,
                gesamtdauer=gesamtdauer if gesamtdauer is not None else '',
                gesamtdauer_min=gesamtdauer_min,
                info_titel=info_titel,
                cover_art_url=cover_art_url
            )
            write_file(info_path, episode_info)
        except KeyError as e:
            logger.error(f"Template formatting error in info: missing key {e}")
        except Exception as e:
            logger.error(f"Failed to write info file for {folder_name}: {e}")

        # Write chapters.txt
        chapters = serie.get('kapitel', [])
        if chapters:
            chapters_content = []
            for chapter in chapters:
                try:
                    chapter_text = tmpl_chapters.format(
                        kapitel_titel=chapter.get('titel', ''),
                        kapitel_timestart=chapter.get('start', ''),
                        kapitel_timeend=chapter.get('end', '')
                    )
                    chapters_content.append(chapter_text)
                except KeyError as e:
                    logger.error(f"Template formatting error in chapters: missing key {e}")
            
            if chapters_content:
                chapters_path = os.path.join(folder_path, f'{nummer_str}-chapters.txt')
                full_chapters_content = ';FFMETADATA1\n' + '\n'.join(chapters_content)
                write_file(chapters_path, full_chapters_content)

    # Write summary files
    summary_files = {
        'folder-names.txt': '\n'.join(outputs) + '\n',
        'titles.txt': '\n'.join(titles) + '\n',
        'cover-art-urls.txt': '\n'.join(cover_art_urls) + '\n',
        'episodes-time-ms.txt': '\n'.join(episode_durations) + '\n'
    }

    for filename, content in summary_files.items():
        path = os.path.join(CONFIG['output_dir'], filename)
        write_file(path, content)
        if filename == 'folder-names.txt':
            logger.info(f"Folder-friendly names written to: {path}")
        elif filename == 'titles.txt':
            logger.info(f"Original titles written to: {path}")

    logger.info(f"Scaffolding complete. Output written to: {CONFIG['output_dir']}")


if __name__ == '__main__':
    main()
