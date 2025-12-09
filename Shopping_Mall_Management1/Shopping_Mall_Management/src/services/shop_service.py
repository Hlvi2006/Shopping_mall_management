from src.repositories.shop_repository import ShopRepository
from src.models.shop import Shop
from src.logging_config import get_logger
from src.exceptions.custom_exceptions import ValidationException, NotFoundException

logger = get_logger("ShopService")

class ShopService:
    def __init__(self):
        self.repo = ShopRepository()

    def create_shop(self, shop_id, name, owner, category, price):
        # 1. Yoxlayırıq: ID artıq varmı?
        if self.repo.get_by_id(shop_id):
            logger.warning(f"Attempt to create existing shop ID {shop_id}")
            raise ValidationException("Shop ID already exists!")
        
        # 2. Model yaradırıq (Model özü validation edəcək, məs: mənfi qiymət)
        new_shop = Shop(shop_id, name, owner, category, price)
        self.repo.add(new_shop)
        logger.info(f"Created Shop: {name} (ID: {shop_id})")

    def get_all_shops(self):
        return self.repo.get_all()

    def update_shop(self, shop_id, **kwargs):
        """
        Dinamik update metodu.
        kwargs (keyword arguments) vasitəsilə gələn dəyərləri yeniləyir.
        """
        # 1. Dükanı axtarırıq
        shop = self.repo.get_by_id(shop_id)
        if not shop:
            raise NotFoundException("Shop not found")
        
        # 2. Dəyərləri yeniləyirik
        # kwargs = {"name": "Zara", "price": "100"} kimi gəlir
        for key, value in kwargs.items():
            # hasattr yoxlayır ki, Shop class-ında belə bir property varmı?
            if hasattr(shop, key) and value:
                # setattr edəndə Model-dəki @setter işə düşür.
                # Əgər səhv məlumat (məs: mənfi qiymət) olsa, Model avtomatik ValidationException atacaq.
                setattr(shop, key, value)
        
        # 3. Yenilənmiş obyekti bazada yadda saxlayırıq
        self.repo.update(shop_id, shop)
        logger.info(f"Updated Shop ID: {shop_id}")

    def delete_shop(self, shop_id):
        # Repository silmə zamanı tapmasa, özü NotFoundException atır
        self.repo.delete(shop_id)
        logger.info(f"Deleted Shop ID: {shop_id}")