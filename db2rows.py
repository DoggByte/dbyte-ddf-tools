import json
import os
import re
CONFIG = {
  "input_path": os.getenv('INPUT_PATH', 'db/serie.json'),
  "output_dir": os.getenv('OUTPUT_DIR', 'db/rows')
}

def main():

  os.makedirs(CONFIG["output_dir"], exist_ok=True)

  with open(CONFIG["input_path"], 'r', encoding='utf-8') as f:
    data = json.load(f)

  for entry in data.get('serie', []):
    nummer = entry.get('nummer')
    if nummer is None:
      continue
    # Sanitize nummer to prevent path injection
    nummer_str = str(nummer)
    if not re.fullmatch(r'\d{1,3}', nummer_str):
      continue  # skip invalid nummer
    filename = f"{int(nummer_str):03}.json"
    # Ensure filename is only digits and .json
    if not re.fullmatch(r'\d{3}\.json', filename):
      continue
    output_path = os.path.join(CONFIG["output_dir"], filename)
    # Export entry as pretty JSON
    with open(output_path, 'w', encoding='utf-8') as out_f:
      json.dump(entry, out_f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
  main()
