import json
import os
import re
import logging
from serie_db import SerieDB

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

CONFIG = {
    'db_path': os.getenv('DDF_DB_PATH', 'db/serie.json'),
    'output_dir': os.getenv('DDF_ROWS_DIR', 'db/rows')
}

def main():
    try:
        os.makedirs(CONFIG['output_dir'], exist_ok=True)
    except OSError as e:
        logging.error(f"Could not create output directory {CONFIG['output_dir']}: {e}")
        return

    try:
        db = SerieDB(CONFIG['db_path'])
        series = db.get_all_series()
    except (FileNotFoundError, ValueError) as e:
        logging.error(f"Failed to load database: {e}")
        return

    count = 0
    for entry in series:
        nummer = entry.get('nummer')
        if nummer is None:
            continue

        # Sanitize nummer to prevent path injection
        nummer_str = str(nummer)
        if not re.fullmatch(r'\d{1,3}', nummer_str):
            logging.warning(f"Skipping entry with invalid nummer: {nummer}")
            continue

        filename = f"{int(nummer_str):03}.json"
        # Ensure filename is only digits and .json
        if not re.fullmatch(r'\d{3}\.json', filename):
            continue

        output_path = os.path.join(CONFIG['output_dir'], filename)

        try:
            # Export entry as pretty JSON
            with open(output_path, 'w', encoding='utf-8') as out_f:
                json.dump(entry, out_f, ensure_ascii=False, indent=2)
            count += 1
        except OSError as e:
            logging.error(f"Failed to write to {output_path}: {e}")

    logging.info(f"Successfully exported {count} episodes to {CONFIG['output_dir']}")

if __name__ == "__main__":
    main()
