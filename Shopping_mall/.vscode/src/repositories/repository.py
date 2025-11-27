import sqlite3
from models.shop import Shop, SpecialtyShop
from models.rental import Rental
from models.maintenance import Maintenance

class SingletonMeta(type):
    """Singleton pattern for DB connection."""
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class DatabaseConnection(metaclass=SingletonMeta):
    def __init__(self, db_name='mall.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

class Repository:
    """Abstraction for data handling (dependency inversion)."""
    def __init__(self):
        self.db = DatabaseConnection()
        self._init_db()

    def _init_db(self):
        self.db.cursor.execute('''
            CREATE TABLE IF NOT EXISTS shops (
                shop_id INTEGER PRIMARY KEY,
                name TEXT,
                location TEXT,
                size_sqft INTEGER,
                type TEXT,
                specialty TEXT
            )
        ''')
        self.db.cursor.execute('''
            CREATE TABLE IF NOT EXISTS rentals (
                rental_id INTEGER PRIMARY KEY,
                shop_id INTEGER,
                tenant_name TEXT,
                start_date TEXT,
                end_date TEXT,
                monthly_rent REAL,
                FOREIGN KEY(shop_id) REFERENCES shops(shop_id)
            )
        ''')
        self.db.cursor.execute('''
            CREATE TABLE IF NOT EXISTS maintenance (
                maint_id INTEGER PRIMARY KEY,
                shop_id INTEGER,
                description TEXT,
                request_date TEXT,
                status TEXT,
                FOREIGN KEY(shop_id) REFERENCES shops(shop_id)
            )
        ''')
        self.db.conn.commit()

    def get_next_id(self, table): # id avtomatik doldurmuruq deye!!!
        self.db.cursor.execute(f'SELECT MAX(rowid) FROM {table}')
        max_id = self.db.cursor.fetchone()[0]
        return (max_id or 0) + 1

    def create_shop(self, shop):
        specialty = shop.specialty if hasattr(shop, 'specialty') else None
        self.db.cursor.execute('''
            INSERT INTO shops (shop_id, name, location, size_sqft, type, specialty)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (shop.shop_id, shop.name, shop.location, shop.size_sqft, shop.to_dict()['type'], specialty))
        self.db.conn.commit()

    def create_rental(self, rental):
        self.db.cursor.execute('''
            INSERT INTO rentals (rental_id, shop_id, tenant_name, start_date, end_date, monthly_rent)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (rental.rental_id, rental.shop_id, rental.tenant_name,
              rental.start_date.isoformat(), rental.end_date.isoformat(), rental.monthly_rent))
        self.db.conn.commit()

    def create_maintenance(self, maint):
        self.db.cursor.execute('''
            INSERT INTO maintenance (maint_id, shop_id, description, request_date, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (maint.maint_id, maint.shop_id, maint.description,
              maint.request_date.isoformat(), maint.status))
        self.db.conn.commit()

    def read_all_shops(self):
        self.db.cursor.execute('SELECT * FROM shops')
        shops = []
        for row in self.db.cursor.fetchall():
            shop_id, name, location, size_sqft, shop_type, specialty = row
            if shop_type == 'SpecialtyShop':
                shops.append(SpecialtyShop(shop_id, name, location, size_sqft, specialty))
            else:
                shops.append(Shop(shop_id, name, location, size_sqft))
        return shops

    def read_all_rentals(self):
        from models.rental import Rental
        from datetime import date
        self.db.cursor.execute('SELECT rental_id, shop_id, tenant_name, start_date, end_date, monthly_rent FROM rentals')
        rentals = []
        for row in self.db.cursor.fetchall():
            rental_id, shop_id, tenant_name, start_str, end_str, monthly_rent = row
            # Convert strings back to date objects!
            start_date = date.fromisoformat(start_str)
            end_date = date.fromisoformat(end_str)
            rentals.append(Rental(rental_id, shop_id, tenant_name, start_date, end_date, monthly_rent))
        return rentals

    def read_all_maintenance(self):
        from models.maintenance import Maintenance
        from datetime import date
        self.db.cursor.execute('SELECT maint_id, shop_id, description, request_date, status FROM maintenance')
        maint_list = []
        for row in self.db.cursor.fetchall():
            maint_id, shop_id, description, req_date_str, status = row
            request_date = date.fromisoformat(req_date_str)
            maint = Maintenance(maint_id, shop_id, description, request_date)
            maint.status = status  # use the setter
            maint_list.append(maint)
        return maint_list

    