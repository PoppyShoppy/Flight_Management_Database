from tabulate import tabulate


class DestinationInputService:

    def __init__(self, db_operations):
        self.repo = db_operations

    def get_existing_destinations(self):
        ###Display existing destinations to help user input###
        try:
            results = self.repo.list_destinations()
            if results:
                print("\nExisting destinations:")
                print(tabulate(results, headers=["ID", "IATA", "Airport", "City", "Country"], tablefmt="grid"))
        except Exception as e:
            print("Could not display existing destinations: " + str(e))

    def create_input_destination_data(self):
        ###Collect destination information from user input###
        try:
            self.get_existing_destinations()
            
            iata = input("Enter airport IATA code (e.g., JFK): ").upper().strip()
            if not iata or len(iata) != 3:
                print("IATA code must be exactly 3 characters.")
                return
            
            airport_name = input("Enter airport name (e.g., London Gatwick Airport): ").strip()
            if not airport_name:
                print("Airport name cannot be empty.")
                return
            
            city = input("Enter city (e.g., New York): ").strip()
            if not city:
                print("City cannot be empty.")
                return
            
            country = input("Enter country (e.g., United States): ").strip()
            if not country:
                print("Country cannot be empty.")
                return
            
            # Confirm before inserting
            print("\nConfirm destination details:")
            print("  IATA Code: " + str(iata))
            print("  Airport Name: " + str(airport_name))
            print("  City: " + str(city))
            print("  Country: " + str(country))
            
            confirm = input("Is this correct? (yes/no): ").lower()
            if confirm != "yes" and confirm != "y":
                print("Insertion cancelled.")
                return
            
            # Insert the destination
            inserted_id = self.repo.insert_destination_data(iata, airport_name, city, country)
            print("\nInserted destination id: " + str(inserted_id))
            print("Operation Complete. Returning to main menu...")
            
        except Exception as e:
            print("Error: " + str(e))
