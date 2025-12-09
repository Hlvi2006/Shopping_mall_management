import json
import os
from src.exceptions.custom_exceptions import NotFoundException

DB_PATH = "data/data.json"

class BaseRepository:
    """
    Generic Repository. Bütün fayl oxuma/yazma əməliyyatlarını mərkəzləşdirir.
    key_name: JSON-da hansı açarı oxuyacağını təyin edir (məs: 'shops', 'rentals').
    model_cls: Hansı Modelə çevirəcəyini təyin edir.
    id_field: Obyektin unikal ID sahəsinin adı.
    """
    def __init__(self, key_name, model_cls, id_field):
        self.key_name = key_name
        self.model_cls = model_cls
        self.id_field = id_field
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        # Ensure the directory for DB_PATH exists (so tests can change DB_PATH)
        dir_name = os.path.dirname(DB_PATH) or "."
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        if not os.path.exists(DB_PATH):
            with open(DB_PATH, "w") as f:
                json.dump({"shops": [], "rentals": [], "maintenance": []}, f)

    def _load_full_db(self):
        with open(DB_PATH, "r") as f:
            return json.load(f)

    def _save_full_db(self, data):
        with open(DB_PATH, "w") as f:
            json.dump(data, f, indent=4)

    def get_all(self):
        db = self._load_full_db()
        items = db.get(self.key_name, [])
        return [self.model_cls.from_dict(i) for i in items]

    def get_by_id(self, item_id):
        items = self.get_all()
        for item in items:
            if getattr(item, self.id_field) == str(item_id):
                return item
        return None

    def add(self, item):
        db = self._load_full_db()
        db[self.key_name].append(item.to_dict())
        self._save_full_db(db)

    def update(self, item_id, updated_item):
        db = self._load_full_db()
        items = db[self.key_name]
        for i, raw_item in enumerate(items):
            if str(raw_item[self.id_field]) == str(item_id):
                items[i] = updated_item.to_dict()
                self._save_full_db(db)
                return
        raise NotFoundException(f"{self.key_name} with id {item_id} not found")

    def delete(self, item_id):
        db = self._load_full_db()
        initial_len = len(db[self.key_name])
        # List comprehension ilə filterləyirik
        db[self.key_name] = [i for i in db[self.key_name] if str(i[self.id_field]) != str(item_id)]
        
        if len(db[self.key_name]) == initial_len:
            raise NotFoundException("Item not found to delete")
        
        self._save_full_db(db)