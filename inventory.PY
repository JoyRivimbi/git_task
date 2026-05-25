from tabulate import tabulate

#========The beginning of the class==========
class Shoe:
    """
    Represents a shoe product in the Nike inventory.
    """
    def __init__(self, country, code, product, cost, quantity):
        self.country = country.strip()
        self.code = code.strip()
        self.product = product.strip()
        self.cost = float(cost)
        self.quantity = int(quantity)

    def get_cost(self):
        return self.cost

    def get_quantity(self):
        return self.quantity

    def __str__(self):
        return f"{self.product} ({self.code}) | Country: {self.country}"


#=============Shoe list===========
shoe_list = []


#==========Helper Functions==============
def save_to_file():
    """
    Helper function to safely save the current shoe_list state back to inventory.txt.
    """
    try:
        lines = ["Country,Code,Product,Cost,Quantity\n"]
        for s in shoe_list:
            lines.append(f"{s.country},{s.code},{s.product},{s.cost},{s.quantity}\n")
        
        with open("inventory.txt", "w") as file:
            file.writelines(lines)
        return True
    except Exception as e:
        print(f"\n[ERROR] Failed to save data to file: {e}")
        return False


#==========Core Functions Outside Class==============
def read_shoes_data():
    """
    Opens inventory.txt and reads data to populate shoe objects.
    """
    try:
        with open("inventory.txt", "r") as file:
            next(file)  # Skip the header line
            for line in file:
                if not line.strip():
                    continue
                data = line.strip().split(",")
                if len(data) == 5:
                    shoe_list.append(Shoe(data[0], data[1], data[2], data[3], data[4]))
        print("\n[SUCCESS] Inventory data loaded successfully.")
    except FileNotFoundError:
        print("\n[ERROR] inventory.txt not found. A new one will be generated upon capturing items.")
    except Exception as e:
        print(f"\n[ERROR] An unexpected error occurred while reading data: {e}")


def capture_shoes():
    """
    Captures a shoe profile from the user and writes it permanently to storage.
    """
    print("\n--- Register New Product ---")
    code = input("Enter Code: ").strip()
    
    # Prevent duplicate product keys
    if any(shoe.code == code for shoe in shoe_list):
        print("\n[ERROR] A product with this code already exists.")
        return

    country = input("Enter Country: ")
    product = input("Enter Product: ")
    
    try:
        cost = float(input("Enter Cost: "))
        quantity = int(input("Enter Quantity: "))
        
        new_shoe = Shoe(country, code, product, cost, quantity)
        shoe_list.append(new_shoe)
        
        if save_to_file():
            print(f"\n[SUCCESS] {product} has been registered and saved to database.")
    except ValueError:
        print("\n[ERROR] Invalid input. Cost and Quantity must be numeric values.")


def view_all():
    """
    Iterates over the shoe list and prints details in a neat grid format.
    """
    if not shoe_list:
        print("\nThe inventory is currently empty.")
        return

    table_data = [[s.country, s.code, s.product, f"R{s.cost:,.2f}", s.quantity] for s in shoe_list]
    print("\n--- NIKE WAREHOUSE INVENTORY ---")
    print(tabulate(table_data, headers=["Country", "Code", "Product", "Cost", "Quantity"], tablefmt="grid"))


def re_stock():
    """
    Finds the shoe with the lowest stock capacity and prompts user to increase it.
    """
    if not shoe_list:
        print("\n[!] No inventory available to restock.")
        return

    low_shoe = min(shoe_list, key=lambda x: x.get_quantity())
    print(f"\nLowest stock item: {low_shoe.product} ({low_shoe.quantity} units remaining)")
    
    choice = input("Would you like to restock this item? (y/n): ").lower()
    if choice == 'y':
        try:
            add_qty = int(input("Enter units to add: "))
            if add_qty < 0:
                print("[ERROR] Cannot add negative quantities.")
                return
                
            low_shoe.quantity += add_qty
            if save_to_file():
                print("[SUCCESS] Stock level updated and safely persistent on disk.")
        except ValueError:
            print("[ERROR] Please enter a valid whole integer.")


def search_shoe():
    """
    Searches for a shoe object by its explicit item code.
    """
    search_code = input("\nEnter the shoe code to search: ").strip()
    for shoe in shoe_list:
        if shoe.code == search_code:
            print(f"\nMatch Found: {shoe}")
            return shoe
    print("\n[!] No shoe found with that code.")


def value_per_item():
    """
    Calculates and prints total asset value breakdown per product.
    """
    if not shoe_list:
        print("\nNo items to evaluate.")
        return
        
    print("\n--- STOCK VALUATION REPORT ---")
    for shoe in shoe_list:
        total_value = shoe.cost * shoe.quantity
        print(f"Product: {shoe.product:20} | Unit Cost: R{shoe.cost:10,.2f} | Total Value: R{total_value:12,.2f}")


def highest_qty():
    """
    Determines highest stock volume to run promotional clearance campaigns.
    """
    if not shoe_list:
        print("\nNo items available.")
        return

    high_shoe = max(shoe_list, key=lambda x: x.get_quantity())
    print(f"\n--- CLEARANCE SALE ---")
    print(f"The {high_shoe.product} ({high_shoe.code}) is overstocked with {high_shoe.quantity} units.")
    print("MARKDOWN APPLIED FOR SALE DIRECTIVES!")


#==========Main Menu Loop=============
def main():
    read_shoes_data()

    while True:
        print("\n" + "="*35)
        print("    NIKE STOCK MANAGER")
        print("="*35)
        print("1. View All Inventory")
        print("2. Search by Code")
        print("3. Restock Lowest Quantity")
        print("4. Find Highest Quantity (Sale)")
        print("5. View Total Stock Values")
        print("6. Capture New Product")
        print("7. Exit")
        
        choice = input("\nSelect an option (1-7): ").strip()

        if choice == '1':
            view_all()
        elif choice == '2':
            search_shoe()
        elif choice == '3':
            re_stock()
        elif choice == '4':
            highest_qty()
        elif choice == '5':
            value_per_item()
        elif choice == '6':
            capture_shoes()
        elif choice == '7':
            print("\nExiting system. Goodbye!")
            break
        else:
            print("\n[!] Invalid selection. Please choose a number from 1 to 7.")

if __name__ == "__main__":
    main()