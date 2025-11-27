from models.entity import Entity
from datetime import date

class Rental(Entity):
    """Encapsulates rental agreements."""
    def __init__(self, rental_id, shop_id, tenant_name, start_date, end_date, monthly_rent):
        self._rental_id = rental_id
        self._shop_id = shop_id
        self._tenant_name = tenant_name
        self._start_date = start_date
        self._end_date = end_date
        self._monthly_rent = monthly_rent

    # Getters (encapsulation)
    @property
    def rental_id(self):
        return self._rental_id

    @property
    def shop_id(self):
        return self._shop_id

    @property
    def tenant_name(self):
        return self._tenant_name

    @property
    def start_date(self):
        return self._start_date

    @property
    def end_date(self):
        return self._end_date

    @property
    def monthly_rent(self):
        return self._monthly_rent

    def is_active(self):
        return date.today() <= self._end_date

    def to_dict(self):
        return {
            'rental_id': self._rental_id,
            'shop_id': self._shop_id,
            'tenant_name': self._tenant_name,
            'start_date': self._start_date.isoformat(),
            'end_date': self._end_date.isoformat(),
            'monthly_rent': self._monthly_rent
        }