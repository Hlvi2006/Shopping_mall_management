import unittest
import sys
import os
import shutil

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.rental import Rental
from src.services.rental_service import RentalService
from src.services.shop_service import ShopService
from src.exceptions.custom_exceptions import BusinessRuleException

class TestRental(unittest.TestCase):
    
    def setUp(self):
        self.test_db_path = "tests/test_data/data.json"
        import src.repositories.base_repository as repo_module
        repo_module.DB_PATH = self.test_db_path
        
        self.rental_service = RentalService()
        self.shop_service = ShopService()

    def tearDown(self):
        if os.path.exists("tests/test_data"):
            shutil.rmtree("tests/test_data")

    def test_rental_cost_calculation(self):
        """İcarə haqqının düzgün hesablanması (2 ay)"""
        # Yanvar-Mart = 2 ay
        rental = Rental("R1", "S1", "Tenant", "2024-01-01", "2024-03-01", monthly_price=100)
        self.assertEqual(rental.total_cost, 200.0)

    def test_rental_cost_min_one_month(self):
        """Əgər eyni aydırsa, minimum 1 ay hesablanmalıdır"""
        rental = Rental("R2", "S1", "Tenant", "2024-01-01", "2024-01-05", monthly_price=100)
        self.assertEqual(rental.total_cost, 100.0)

    def test_create_rental_success(self):
        """Uğurlu icarə prosesi"""
        # Əvvəl dükan yaratmalıyıq
        self.shop_service.create_shop("S1", "Shop A", "Owner", "Cat", 500)
        
        self.rental_service.create_rental("R1", "S1", "Ali", "2024-01-01", "2024-02-01")
        
        rentals = self.rental_service.get_all_rentals()
        self.assertEqual(len(rentals), 1)
        
        # Dükanın statusu Rented olmalıdır
        shop = self.shop_service.repo.get_by_id("S1")
        self.assertTrue(shop.is_rented)

    def test_prevent_double_rental(self):
        """Artıq icarədə olan dükanı yenidən icarəyə vermək olmaz (BusinessRuleException)"""
        self.shop_service.create_shop("S2", "Shop B", "Owner", "Cat", 500)
        
        # Birinci icarə
        self.rental_service.create_rental("R1", "S2", "Ali", "2024-01-01", "2024-02-01")
        
        # İkinci icarə cəhdi - Xəta verməlidir
        with self.assertRaises(BusinessRuleException):
            self.rental_service.create_rental("R2", "S2", "Vali", "2024-03-01", "2024-04-01")

if __name__ == '__main__':
    unittest.main()