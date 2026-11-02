import json
from pathlib import Path

class SaveManager:
    def __init__(self):
        self.path = Path(__file__).resolve().parent.parent / 'save.json'

    def save(self, data):
        if not isinstance(data, dict):
            return False

        temporary_path = self.path.with_suffix('.tmp')

        try:
            with temporary_path.open('w', encoding='utf-8') as save_file:
                json.dump(data, save_file, indent=4, allow_nan=False)

            temporary_path.replace(self.path)
            return True
        except (OSError, TypeError, ValueError):
            return False

    def load(self):
        try:
            with self.path.open('r', encoding='utf-8') as save_file:
                data = json.load(save_file)

            return data if isinstance(data, dict) else None
        except (OSError, ValueError):
            return None
