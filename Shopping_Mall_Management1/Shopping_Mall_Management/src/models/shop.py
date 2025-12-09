from .base_model import BaseModel

class Shop(BaseModel):
    def __init__(self, shop_id, name, owner, category, price, is_rented=False):
        # Private attributes (Encapsulation)
        self.__shop_id = str(shop_id)
        self.__name = name
        self.__owner = owner
        self.__category = category
        self.__price = float(price)
        self.__is_rented = is_rented

    # --- Properties (Getters & Setters) ---

    @property
    def shop_id(self):
        return self.__shop_id
    
    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, value):
        if not value:
            raise ValueError("Shop name cannot be empty")
        self.__name = value

    @property
    def owner(self):
        return self.__owner
    
    @owner.setter
    def owner(self, value):
        self.__owner = value

    @property
    def category(self):
        return self.__category
    
    @property
    def price(self):
        return self.__price
    
    @price.setter
    def price(self, value):
        if float(value) < 0:
            raise ValueError("Price cannot be negative")
        self.__price = float(value)

    @property
    def is_rented(self):
        return self.__is_rented
    
    @is_rented.setter
    def is_rented(self, value):
        if not isinstance(value, bool):
            raise ValueError("is_rented must be True or False")
        self.__is_rented = value

    # --- Implementation of Abstract Methods ---

    def to_dict(self):
        return {
            "shop_id": self.shop_id,
            "name": self.name,
            "owner": self.owner,
            "category": self.category,
            "price": self.price,
            "is_rented": self.is_rented
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            shop_id=data["shop_id"],
            name=data["name"],
            owner=data["owner"],
            category=data["category"],
            price=data["price"],
            is_rented=data["is_rented"]
        )
    
    def __str__(self):
        status = "RENTED" if self.is_rented else "AVAILABLE"
        return f"[ID: {self.shop_id}] {self.name} | {self.category} | {self.price}$ | {status}"