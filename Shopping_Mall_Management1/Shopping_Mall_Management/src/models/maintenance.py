from .base_model import BaseModel

class Maintenance(BaseModel):
    def __init__(self, main_id, shop_id, description, date, cost):
        self.__main_id = str(main_id)
        self.__shop_id = str(shop_id)
        self.__description = description
        self.__date = date
        self.__cost = float(cost)

    # --- Properties ---

    @property
    def main_id(self):
        return self.__main_id

    @property
    def shop_id(self):
        return self.__shop_id

    @property
    def description(self):
        return self.__description
    
    @description.setter
    def description(self, value):
        if not value: raise ValueError("Description cannot be empty")
        self.__description = value

    @property
    def date(self):
        return self.__date

    @property
    def cost(self):
        return self.__cost
    
    @cost.setter
    def cost(self, value):
        if float(value) < 0: raise ValueError("Cost cannot be negative")
        self.__cost = float(value)

    # --- Implementation ---

    def to_dict(self):
        return {
            "main_id": self.main_id,
            "shop_id": self.shop_id,
            "description": self.description,
            "date": self.date,
            "cost": self.cost
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            main_id=data["main_id"],
            shop_id=data["shop_id"],
            description=data["description"],
            date=data["date"],
            cost=data["cost"]
        )

    def __str__(self):
        return f"[ID: {self.main_id}] Shop: {self.shop_id} | Cost: {self.cost} | {self.description}"