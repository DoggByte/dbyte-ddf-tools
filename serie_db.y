import json
from typing import List, Dict, Any, Optional

class SerieDB:
    def __init__(self, json_path: str):
        self.json_path = json_path
        self._load()

    def _load(self):
        with open(self.json_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        self.series = self.data.get('serie', [])

    def get_all_series(self) -> List[Dict[str, Any]]:
        return self.series

    def get_serie_by_nummer(self, nummer: int) -> Optional[Dict[str, Any]]:
        for serie in self.series:
            if serie.get('nummer') == nummer:
                return serie
        return None

    def search_by_title(self, title: str) -> List[Dict[str, Any]]:
        return [s for s in self.series if title.lower() in s.get('titel', '').lower()]

    def add_serie(self, serie: Dict[str, Any]):
        self.series.append(serie)
        self._save()

    def _save(self):
        self.data['serie'] = self.series
        with open(self.json_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    db = SerieDB('db/serie.json')
    print('All series:')
    for s in db.get_all_series()[:1]:  # Print only the first for brevity
        print(s['titel'])
    print('\nSearch for "Papagei":')
    for s in db.search_by_title('Papagei'):
        print(s['titel'])
    print('\nGet serie nummer 1:')
    print(db.get_serie_by_nummer(1))
