from src.repositories.maintenance_repository import MaintenanceRepository
from src.models.maintenance import Maintenance
from src.exceptions.custom_exceptions import NotFoundException
from src.logging_config import get_logger

logger = get_logger("MaintenanceService")

class MaintenanceService:
    def __init__(self):
        self.repo = MaintenanceRepository()

    def add_record(self, m_id, shop_id, desc, date, cost):
        record = Maintenance(m_id, shop_id, desc, date, cost)
        self.repo.add(record)
        logger.info(f"Added Maintenance {m_id} for Shop {shop_id}")

    # --- YENİ UPDATE METODU ---
    def update_record(self, m_id, **kwargs):
        record = self.repo.get_by_id(m_id)
        if not record:
            raise NotFoundException("Maintenance record not found")

        for key, value in kwargs.items():
            if value and hasattr(record, key):
                setattr(record, key, value)
        
        self.repo.update(m_id, record)
        logger.info(f"Updated Maintenance ID: {m_id}")

    def get_all(self):
        return self.repo.get_all()