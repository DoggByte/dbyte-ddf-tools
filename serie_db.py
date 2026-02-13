import json
import os
import tempfile
import shutil
from typing import List, Dict, Any, Optional, TypedDict

class Serie(TypedDict, total=False):
    nummer: int
    titel: str

class SerieDB:
    def __init__(self, json_path: str):
        self.json_path = json_path
        self.data: Dict[str, Any] = {'serie': []}
        self.series: List[Serie] = []
        self._index: Dict[int, Serie] = {}
        self._load()

    def _load(self):
        if not os.path.exists(self.json_path):
            self.series = []
            self._rebuild_index()
            return

        try:
            with open(self.json_path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            self.series = self.data.get('serie', [])
            self._rebuild_index()
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in database: {e}")

    def _rebuild_index(self):
        self._index = {s.get('nummer'): s for s in self.series if 'nummer' in s}

    def get_all_series(self) -> List[Serie]:
        return self.series

    def get_serie_by_nummer(self, nummer: int) -> Optional[Serie]:
        return self._index.get(nummer)

    def search_by_title(self, title: str) -> List[Serie]:
        return [s for s in self.series if title.lower() in s.get('titel', '').lower()]

    def add_serie(self, serie: Serie):
        required_fields = {'nummer', 'titel'}  # Define based on your schema
        if not all(field in serie for field in required_fields):
            raise ValueError(f"Missing required fields: {required_fields}")
        
        self.series.append(serie)
        self._index[serie['nummer']] = serie
        self._save()

    def _save(self):
        self.data['serie'] = self.series
        dir_name = os.path.dirname(self.json_path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
            
        tmp_path = None
        try:
            with tempfile.NamedTemporaryFile(mode='w', delete=False, 
                                              encoding='utf-8', dir=dir_name) as tmp:
                json.dump(self.data, tmp, ensure_ascii=False, indent=4)
                tmp_path = tmp.name
            shutil.move(tmp_path, self.json_path)
        except Exception:
            if tmp_path and os.path.exists(tmp_path):
                os.remove(tmp_path)
            raise

if __name__ == '__main__':
    # Use a temporary file for the example if the default doesn't exist
    example_path = 'db/serie.json'
    if not os.path.exists(os.path.dirname(example_path)):
        os.makedirs(os.path.dirname(example_path), exist_ok=True)
    
    # For demonstration, ensure it exists or create it
    if not os.path.exists(example_path):
        with open(example_path, 'w', encoding='utf-8') as f:
            json.dump({"serie": [{"nummer": 1, "titel": "Der Super-Papagei"}]}, f)

    db = SerieDB(example_path)
    print('All series:')
    for s in db.get_all_series()[:1]:  # Print only the first for brevity
        print(s['titel'])
    print('\nSearch for "Papagei":')
    for s in db.search_by_title('Papagei'):
        print(s['titel'])
    print('\nGet serie nummer 1:')
    print(db.get_serie_by_nummer(1))
