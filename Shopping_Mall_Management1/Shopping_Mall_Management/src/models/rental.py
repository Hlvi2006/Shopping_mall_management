import datetime
from .base_model import BaseModel

class Rental(BaseModel):
    def __init__(self, rental_id, shop_id, tenant, start_date, end_date, monthly_price, total_cost=None):
        self.__rental_id = str(rental_id)
        self.__shop_id = str(shop_id)
        self.__tenant = tenant
        self.__start_date = start_date
        self.__end_date = end_date
        self.__monthly_price = float(monthly_price)
        
        # Calculate or assign total cost
        if total_cost is not None:
            self.__total_cost = float(total_cost)
        else:
            self.__total_cost = self.calculate_total()

    # --- Properties ---

    @property
    def rental_id(self):
        return self.__rental_id

    @property
    def shop_id(self):
        return self.__shop_id

    @property
    def tenant(self):
        return self.__tenant
    
    @tenant.setter
    def tenant(self, value):
        if not value: raise ValueError("Tenant cannot be empty")
        self.__tenant = value

    @property
    def start_date(self):
        return self.__start_date
    
    @property
    def end_date(self):
        return self.__end_date
    
    @property
    def monthly_price(self):
        return self.__monthly_price
    
    @monthly_price.setter
    def monthly_price(self, value):
        if float(value) < 0: raise ValueError("Price cannot be negative")
        self.__monthly_price = float(value)

    @property
    def total_cost(self):
        return self.__total_cost

    # --- Methods ---

    def calculate_total(self):
        try:
            start = datetime.datetime.strptime(self.__start_date, "%Y-%m-%d")
            end = datetime.datetime.strptime(self.__end_date, "%Y-%m-%d")
            months = (end.year - start.year) * 12 + (end.month - start.month)
            return max(1, months) * self.__monthly_price
        except (ValueError, TypeError):
            return 0.0

    def to_dict(self):
        return {
            "rental_id": self.rental_id,
            "shop_id": self.shop_id,
            "tenant": self.tenant,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "monthly_price": self.monthly_price,
            "total_cost": self.total_cost
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            rental_id=data["rental_id"],
            shop_id=data["shop_id"],
            tenant=data["tenant"],
            start_date=data["start_date"],
            end_date=data["end_date"],
            monthly_price=data["monthly_price"],
            total_cost=data.get("total_cost")
        )
    
    def __str__(self):
        return f"[Rental ID: {self.rental_id}] Shop: {self.shop_id} | Tenant: {self.tenant} | Cost: {self.total_cost}"