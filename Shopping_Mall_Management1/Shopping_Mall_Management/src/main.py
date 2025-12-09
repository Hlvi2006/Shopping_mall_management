import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services.shop_service import ShopService
from src.services.rental_service import RentalService
from src.services.maintenance_service import MaintenanceService
from src.exceptions.custom_exceptions import BaseAppException
from src.logging_config import get_logger

logger = get_logger("System")

class MainMenu:
    def __init__(self):
        self.shop_service = ShopService()
        self.rental_service = RentalService()
        self.maint_service = MaintenanceService()

    def run(self):
        logger.info("System Started")
        while True:
            print("\n=== SHOPPING MALL MANAGEMENT SYSTEM ===")
            print("1. Manage Shops")
            print("2. Manage Rentals")
            print("3. Manage Maintenance")
            print("0. Exit")
            
            choice = input("Select: ")
            
            try:
                if choice == "1": self.shop_menu()
                elif choice == "2": self.rental_menu()
                elif choice == "3": self.maint_menu()
                elif choice == "0":
                    logger.info("System Exit")
                    print("Goodbye!")
                    break
                else:
                    print("Invalid choice!")
            except BaseAppException as e:
                print(f"⚠️ ERROR: {e}")
                logger.warning(f"App Error: {e}")
            except Exception as e:
                print(f"🔥 CRITICAL ERROR: {e}")
                logger.error(f"Critical: {e}")

    # --- SHOP MENU ---
    def shop_menu(self):
        print("\n--- SHOP MANAGEMENT ---")
        print("1. Add Shop")
        print("2. List Shops")
        print("3. Update Shop")  # <--- YENİ
        print("4. Delete Shop")
        print("0. Back")
        ch = input("Select: ")

        if ch == "1":
            sid = input("Shop ID: ")
            name = input("Name: ")
            owner = input("Owner: ")
            cat = input("Category: ")
            price = input("Rent Price: ")
            self.shop_service.create_shop(sid, name, owner, cat, price)
            print("✅ Shop created.")
        
        elif ch == "2":
            shops = self.shop_service.get_all_shops()
            for s in shops: print(s)

        elif ch == "3": # UPDATE
            sid = input("Enter Shop ID to update: ")
            print("(Leave empty to keep current value)")
            name = input("New Name: ")
            owner = input("New Owner: ")
            cat = input("New Category: ")
            price = input("New Price: ")
            
            # Yalnız dolu olanları göndəririk
            updates = {}
            if name: updates["name"] = name
            if owner: updates["owner"] = owner
            if cat: updates["category"] = cat
            if price: updates["price"] = price
            
            if updates:
                self.shop_service.update_shop(sid, **updates)
                print("✅ Shop updated.")
            else:
                print("No changes made.")

        elif ch == "4":
            sid = input("Shop ID to delete: ")
            self.shop_service.delete_shop(sid)
            print("✅ Shop deleted.")

    # --- RENTAL MENU ---
    def rental_menu(self):
        print("\n--- RENTAL MANAGEMENT ---")
        print("1. Create Rental")
        print("2. List Rentals")
        print("3. Update Rental") # <--- YENİ
        print("4. End Rental (Delete)")
        print("0. Back")
        ch = input("Select: ")

        if ch == "1":
            rid = input("Rental ID: ")
            sid = input("Shop ID: ")
            tenant = input("Tenant Name: ")
            start = input("Start Date (YYYY-MM-DD): ")
            end = input("End Date (YYYY-MM-DD): ")
            self.rental_service.create_rental(rid, sid, tenant, start, end)
            print("✅ Rental created.")

        elif ch == "2":
            rentals = self.rental_service.get_all_rentals()
            for r in rentals: print(r)

        elif ch == "3": # UPDATE
            rid = input("Enter Rental ID to update: ")
            print("(Leave empty to keep current value)")
            tenant = input("New Tenant: ")
            start = input("New Start Date: ")
            end = input("New End Date: ")
            
            updates = {}
            if tenant: updates["tenant"] = tenant
            if start: updates["start_date"] = start
            if end: updates["end_date"] = end
            
            if updates:
                self.rental_service.update_rental(rid, **updates)
                print("✅ Rental updated (Costs recalculated).")
            else:
                print("No changes made.")

        elif ch == "4":
            rid = input("Rental ID to delete: ")
            self.rental_service.delete_rental(rid)
            print("✅ Rental ended.")

    # --- MAINTENANCE MENU ---
    def maint_menu(self):
        print("\n--- MAINTENANCE MANAGEMENT ---")
        print("1. Add Record")
        print("2. List Records")
        print("3. Update Record") # <--- YENİ
        print("0. Back")
        ch = input("Select: ")

        if ch == "1":
            mid = input("Record ID: ")
            sid = input("Shop ID: ")
            desc = input("Description: ")
            date = input("Date: ")
            cost = input("Cost: ")
            self.maint_service.add_record(mid, sid, desc, date, cost)
            print("✅ Record added.")

        elif ch == "2":
            recs = self.maint_service.get_all()
            for r in recs: print(r)

        elif ch == "3": # UPDATE
            mid = input("Enter Record ID to update: ")
            desc = input("New Description: ")
            date = input("New Date: ")
            cost = input("New Cost: ")
            
            updates = {}
            if desc: updates["description"] = desc
            if date: updates["date"] = date
            if cost: updates["cost"] = cost
            
            if updates:
                self.maint_service.update_record(mid, **updates)
                print("✅ Record updated.")

if __name__ == "__main__":
    app = MainMenu()
    app.run()