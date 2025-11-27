from models.entity import Entity
from datetime import date

class Maintenance(Entity):
    """Encapsulates maintenance requests."""
    def __init__(self, maint_id, shop_id, description, request_date, status='Pending'):
        self._maint_id = maint_id
        self._shop_id = shop_id
        self._description = description
        self._request_date = request_date
        self._status = status

    # Getters
    @property
    def maint_id(self):
        return self._maint_id

    @property
    def shop_id(self):
        return self._shop_id

    @property
    def description(self):
        return self._description

    @property
    def request_date(self):
        return self._request_date

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if value not in ['Pending', 'In Progress', 'Completed']:
            raise ValueError("Invalid status")
        self._status = value

    def to_dict(self):
        return {
            'maint_id': self._maint_id,
            'shop_id': self._shop_id,
            'description': self._description,
            'request_date': self._request_date.isoformat(),
            'status': self._status
        }