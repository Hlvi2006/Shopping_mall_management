from src.repositories.rental_repository import RentalRepository
from src.repositories.shop_repository import ShopRepository
from src.models.rental import Rental
from src.exceptions.custom_exceptions import BusinessRuleException, NotFoundException, ValidationException
from src.logging_config import get_logger

logger = get_logger("RentalService")

class RentalService:
    def __init__(self):
        self.rental_repo = RentalRepository()
        self.shop_repo = ShopRepository()

    def create_rental(self, rental_id, shop_id, tenant, start, end):
        # (Köhnə kod olduğu kimi qalır...)
        shop = self.shop_repo.get_by_id(shop_id)
        if not shop:
            raise NotFoundException("Shop not found!")
        
        if shop.is_rented:
            raise BusinessRuleException("This shop is already rented!")

        rental = Rental(rental_id, shop_id, tenant, start, end, shop.price)
        self.rental_repo.add(rental)

        shop.is_rented = True
        self.shop_repo.update(shop_id, shop)
        logger.info(f"Created Rental {rental_id} for Shop {shop_id}")

    # --- YENİ UPDATE METODU ---
    def update_rental(self, rental_id, **kwargs):
        rental = self.rental_repo.get_by_id(rental_id)
        if not rental:
            raise NotFoundException("Rental not found")
        
        # Gələn dəyərləri yeniləyirik
        for key, value in kwargs.items():
            if value and hasattr(rental, key):
                setattr(rental, key, value) # Setterlər işə düşür və yoxlayır
        
        self.rental_repo.update(rental_id, rental)
        logger.info(f"Updated Rental ID: {rental_id}")

    def delete_rental(self, rental_id):
        # (Köhnə kod olduğu kimi qalır...)
        rental = self.rental_repo.get_by_id(rental_id)
        if not rental:
            raise NotFoundException("Rental not found")

        shop = self.shop_repo.get_by_id(rental.shop_id)
        if shop:
            shop.is_rented = False
            self.shop_repo.update(shop.shop_id, shop)

        self.rental_repo.delete(rental_id)
        logger.info(f"Deleted Rental {rental_id}")

    def get_all_rentals(self):
        return self.rental_repo.get_all()