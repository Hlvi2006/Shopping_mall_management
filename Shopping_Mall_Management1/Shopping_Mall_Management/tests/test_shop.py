import unittest
import sys
import os
import shutil

# Src qovluğunu tapmaq üçün yol əlavə edirik
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.shop import Shop
from src.services.shop_service import ShopService
from src.repositories.base_repository import BaseRepository

class TestShop(unittest.TestCase):
    
    def setUp(self):
        """Hər testdən əvvəl işə düşür. Test üçün ayrıca qovluq yaradırıq."""
        # Orijinal data.json korlanmasın deyə test bazası yolunu dəyişirik
        self.test_db_path = "tests/test_data/data.json"
        
        # Repository-nin yolunu müvəqqəti olaraq dəyişmək üçün trick edirik
        # (Real layihədə bu config faylı ilə edilir, amma burada sadə olsun deyə belə edirik)
        import src.repositories.base_repository as repo_module
        repo_module.DB_PATH = self.test_db_path
        
        self.service = ShopService()

    def tearDown(self):
        """Hər testdən sonra işə düşür. Yaradılan faylları silir."""
        if os.path.exists("tests/test_data"):
            shutil.rmtree("tests/test_data")

    def test_shop_model_creation(self):
        """Shop obyektinin düzgün yaradılmasını yoxlayır"""
        shop = Shop("101", "Nike", "Ali", "Sport", 500)
        self.assertEqual(shop.name, "Nike")
        self.assertEqual(shop.price, 500.0)
        self.assertFalse(shop.is_rented) # Default False olmalıdır

    def test_create_shop_service(self):
        """Servis vasitəsilə dükan yaradılmasını yoxlayır"""
        self.service.create_shop("102", "Adidas", "Vali", "Sport", 600)
        
        shops = self.service.get_all_shops()
        self.assertEqual(len(shops), 1)
        self.assertEqual(shops[0].shop_id, "102")

    def test_delete_shop(self):
        """Dükanın silinməsini yoxlayır"""
        self.service.create_shop("103", "Puma", "Hasan", "Sport", 400)
        self.service.delete_shop("103")
        
        shops = self.service.get_all_shops()
        self.assertEqual(len(shops), 0)

if __name__ == '__main__':
    unittest.main()