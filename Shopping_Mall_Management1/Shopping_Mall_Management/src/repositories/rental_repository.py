from .base_repository import BaseRepository
from src.models.rental import Rental

class RentalRepository(BaseRepository):
    def __init__(self):
        super().__init__(key_name="rentals", model_cls=Rental, id_field="rental_id")