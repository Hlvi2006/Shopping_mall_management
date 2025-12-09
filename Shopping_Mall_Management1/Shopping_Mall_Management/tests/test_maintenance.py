import unittest
import sys
import os
import shutil

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.maintenance import Maintenance
from src.services.maintenance_service import MaintenanceService

class TestMaintenance(unittest.TestCase):
    
    def setUp(self):
        self.test_db_path = "tests/test_data/data.json"
        import src.repositories.base_repository as repo_module
        repo_module.DB_PATH = self.test_db_path
        
        self.service = MaintenanceService()

    def tearDown(self):
        if os.path.exists("tests/test_data"):
            shutil.rmtree("tests/test_data")

    def test_maintenance_model(self):
        """Modelin atributlarının yoxlanması"""
        maint = Maintenance("M1", "S1", "Broken Door", "2024-05-05", 150.0)
        self.assertEqual(maint.cost, 150.0)
        self.assertEqual(maint.description, "Broken Door")

    def test_add_maintenance_record(self):
        """Servis vasitəsilə qeyd əlavə olunması"""
        self.service.add_record("M1", "S10", "Paint", "2024-05-05", 200)
        
        records = self.service.get_all()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].cost, 200.0)

if __name__ == '__main__':
    unittest.main()