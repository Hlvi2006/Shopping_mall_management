from .base_repository import BaseRepository
from src.models.shop import Shop

class ShopRepository(BaseRepository):
    def __init__(self):
        super().__init__(key_name="shops", model_cls=Shop, id_field="shop_id")