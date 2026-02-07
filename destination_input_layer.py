import sqlite3


class DestinationInputLayer:

    def __init__(self, db_operations):
        self.repo = db_operations

    def get_existing_destinations(self):
        """Display existing destinations to help user input"""
        try:
            conn = sqlite3.connect(self.repo.db_name)
            cur = conn.cursor()
            cur.execute("SELECT destination_id, airport_iata_code, airport_name, city, country FROM destinations LIMIT 10")
            results = cur.fetchall()
            conn.close()
            
            if results:
                print("\nSample existing destinations:")
                print("-" * 80)
                for row in results:
                    print(f"ID: {row[0]:<3} | IATA: {row[1]:<6} | Airport: {row[2]:<25} | City: {row[3]:<15} | Country: {row[4]}")
                print("-" * 80)
        except Exception as e:
            print(f"Could not display existing destinations: {e}")

    def create_input_destination_data(self):
        """Collect destination information from user input"""
        try:
            self.get_existing_destinations()
            
            iata = input("Enter airport IATA code (e.g., JFK): ").upper().strip()
            if not iata or len(iata) != 3:
                print("IATA code must be exactly 3 characters.")
                return
            
            airport_name = input("Enter airport name (e.g., John F. Kennedy International): ").strip()
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
            print(f"\nConfirm destination details:")
            print(f"  IATA Code: {iata}")
            print(f"  Airport Name: {airport_name}")
            print(f"  City: {city}")
            print(f"  Country: {country}")
            
            confirm = input("Is this correct? (yes/no): ").lower()
            if confirm != "yes" and confirm != "y":
                print("Insertion cancelled.")
                return
            
            # Insert the destination
            self.repo.insert_destination_data(iata, airport_name, city, country)
            print("\nOperation Complete. Returning to main menu...")
            
        except Exception as e:
            print(f"Error: {e}")
