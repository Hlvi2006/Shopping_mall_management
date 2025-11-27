from models.entity import Entity

class Shop(Entity):
    """Base class for shops, encapsulating shop details."""
    def __init__(self, shop_id, name, location, size_sqft):
        self._shop_id = shop_id
        self._name = name
        self._location = location
        self._size_sqft = size_sqft

    @property
    def shop_id(self):
        return self._shop_id

    @property
    def name(self):
        return self._name

    @property
    def location(self):
        return self._location

    @property
    def size_sqft(self):
        return self._size_sqft

    def calculate_rent(self, base_rate=10):
        """Polymorphic method for rent calculation."""
        return self._size_sqft * base_rate

    def to_dict(self):
        return {
            'shop_id': self._shop_id,
            'name': self._name,
            'location': self._location,
            'size_sqft': self._size_sqft,
            'type': 'Shop'
        }

class SpecialtyShop(Shop): #why?
    """Inherited class demonstrating polymorphism and Liskov substitution."""
    def __init__(self, shop_id, name, location, size_sqft, specialty):
        super().__init__(shop_id, name, location, size_sqft)
        self._specialty = specialty

    @property
    def specialty(self):
        return self._specialty

    def calculate_rent(self, base_rate=10):
        """Overridden for specialty premium."""
        return super().calculate_rent(base_rate) * 1.2  # 20% premium

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict['specialty'] = self._specialty
        base_dict['type'] = 'SpecialtyShop'
        return base_dict