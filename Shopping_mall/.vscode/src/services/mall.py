import logging
from repositories.repository import Repository
from models.shop import Shop, SpecialtyShop
from models.rental import Rental
from models.maintenance import Maintenance
from datetime import date

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ShopFactory:
    """Factory pattern for creating shops."""
    @staticmethod
    def create_shop(shop_type, *args):
        if shop_type == 'standard':
            return Shop(*args)
        elif shop_type == 'specialty':
            return SpecialtyShop(*args)
        raise ValueError("Unknown shop type")

class Mall:
    """Controller class (GRASP) managing mall operations."""
    def __init__(self, repo: Repository):
        self._repo = repo  # Dependency inversion

    def add_shop(self, shop_type, name, location, size_sqft, specialty=None):
        try:
            shop_id = self._repo.get_next_id('shops')
            args = (shop_id, name, location, size_sqft)
            if shop_type == 'specialty':
                args += (specialty,)
            shop = ShopFactory.create_shop(shop_type, *args)
            self._repo.create_shop(shop)
            logging.info(f"Added shop: {shop.name}")
            return shop
        except Exception as e:
            logging.error(f"Error adding shop: {e}")
            raise

    def add_rental(self, shop_id, tenant_name, start_date, end_date, monthly_rent):
        try:
            rental_id = self._repo.get_next_id('rentals')
            rental = Rental(rental_id, shop_id, tenant_name, date.fromisoformat(start_date), date.fromisoformat(end_date), monthly_rent)
            self._repo.create_rental(rental)
            logging.info(f"Added rental for shop {shop_id}")
            return rental
        except Exception as e:
            logging.error(f"Error adding rental: {e}")
            raise

    def add_maintenance(self, shop_id, description, request_date, status="Pending"):
        try:
            maint_id = self._repo.get_next_id('maintenance')
            maint = Maintenance(
                maint_id,
                shop_id,
                description,
                date.fromisoformat(request_date),
                status=status.strip() if status else "Pending"   # burda status qəbul edir
            )
            self._repo.create_maintenance(maint)
            logging.info(f"Maintenance əlavə olundu → Shop {shop_id} | Status: {maint.status}")
            return maint
        except Exception as e:
            logging.error(f"Maintenance əlavə edilə bilmədi: {e}")
            raise

    # Read methods
    def get_all_shops(self):
        return self._repo.read_all_shops()

    def get_all_rentals(self):
        return self._repo.read_all_rentals()

    def get_all_maintenance(self):
        return self._repo.read_all_maintenance()

    