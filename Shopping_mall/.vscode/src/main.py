from services.mall import Mall
from repositories.repository import Repository

def main():
    repo = Repository()
    mall = Mall(repo)

    while True:
        print("\nShopping Mall Management CLI")
        print("1. Add Shop")
        print("2. Add Rental")
        print("3. Add Maintenance")
        print("4. List Shops")
        print("5. List Rentals")
        print("6. List Maintenance")
        print("0. Exit")

        choice = input("Enter choice: ")
        if choice == '1':
            shop_type = input("Shop type (standard/specialty): ")
            name = input("Name: ")
            location = input("Location: ")
            size_sqft = int(input("Size (sqft): "))
            specialty = input("Specialty (if applicable): ") if shop_type == 'specialty' else None
            mall.add_shop(shop_type, name, location, size_sqft, specialty)
        elif choice == '2':
            shop_id = int(input("Shop ID: "))
            tenant = input("Tenant: ")
            start = input("Start date (YYYY-MM-DD): ")
            end = input("End date (YYYY-MM-DD): ")
            rent = float(input("Monthly rent: "))
            mall.add_rental(shop_id, tenant, start, end, rent)
        elif choice == '3':  # Add Maintenance
            shop_id = int(input("Enter Shop ID: "))
            desc = input("Description: ")
            date_str = input("Request date (YYYY-MM-DD): ")
            # YENİ ƏLAVƏ OLUNAN SƏTİR:
            status_input = input("Status (Pending/In Progress/Completed) [default: Pending]: ").strip()
            if not status_input:
                status_input = "Pending"  # boş buraxıbsa → Pending

            mall.add_maintenance(shop_id, desc, date_str, status=status_input)  # status ötürürük
        elif choice == '4':
            for shop in mall.get_all_shops():
                print(shop.to_dict())
        elif choice == '5':
            for rental in mall.get_all_rentals():
                print(rental.to_dict())
        elif choice == '6':
            for maint in mall.get_all_maintenance():
                print(maint.to_dict())
        
        elif choice == '0':
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()