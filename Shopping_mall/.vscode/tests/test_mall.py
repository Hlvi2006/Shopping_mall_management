import unittest
from src.services.mall import Mall, ShopFactory
from src.repositories.repository import Repository
from src.models.shop import Shop, SpecialtyShop
from src.models.rental import Rental
from src.models.maintenance import Maintenance
from datetime import date

class TestMall(unittest.TestCase):
    def setUp(self):
        self.repo = Repository()
        self.mall = Mall(self.repo)

    def test_add_shop(self):
        shop = self.mall.add_shop('standard', 'Test Shop', 'Floor 1', 1000)
        self.assertIsInstance(shop, Shop)
        self.assertEqual(shop.name, 'Test Shop')

    def test_add_specialty_shop(self):
        shop = self.mall.add_shop('specialty', 'Special Shop', 'Floor 2', 500, 'Electronics')
        self.assertIsInstance(shop, SpecialtyShop)
        self.assertEqual(shop.specialty, 'Electronics')

    def test_polymorphism_rent_calc(self):
        standard = ShopFactory.create_shop('standard', 1, 'Std', 'Loc', 1000)
        specialty = ShopFactory.create_shop('specialty', 2, 'Spec', 'Loc', 1000, 'Tech')
        self.assertEqual(standard.calculate_rent(), 10000)
        self.assertEqual(specialty.calculate_rent(), 12000)

    def test_add_rental(self):
        self.mall.add_shop('standard', 'Shop1', 'Loc1', 100)
        rental = self.mall.add_rental(1, 'Tenant1', '2025-01-01', '2025-12-31', 5000)
        self.assertIsInstance(rental, Rental)
        self.assertTrue(rental.is_active())

    def test_add_maintenance(self):
        self.mall.add_shop('standard', 'Shop2', 'Loc2', 200)
        maint = self.mall.add_maintenance(1, 'Fix lights', '2025-11-27')
        self.assertIsInstance(maint, Maintenance)
        self.assertEqual(maint.status, 'Pending')

    def test_update_and_delete(self):
        self.mall.add_shop('standard', 'Shop3', 'Loc3', 300)
        self.mall.add_rental(1, 'Tenant', '2025-01-01', '2025-06-01', 3000)
        self.mall.update_rental(1, '2025-12-31')
        rentals = self.mall.get_all_rentals()
        self.assertEqual(rentals[0].end_date, date(2025, 12, 31))
        self.mall.delete_shop(1)
        self.assertEqual(len(self.mall.get_all_shops()), 0)  # Assuming prior tests cleaned up

if __name__ == '__main__':
    unittest.main()