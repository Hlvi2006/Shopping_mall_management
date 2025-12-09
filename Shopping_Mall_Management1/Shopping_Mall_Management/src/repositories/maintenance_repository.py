from .base_repository import BaseRepository
from src.models.maintenance import Maintenance

class MaintenanceRepository(BaseRepository):
    def __init__(self):
        super().__init__(key_name="maintenance", model_cls=Maintenance, id_field="main_id")