import sqlite3


class FlightCrewInputLayer:

    def __init__(self, db_operations):
        self.repo = db_operations

    def display_available_flights(self):
        """Display available flights for user to choose from"""
        try:
            conn = sqlite3.connect(self.repo.db_name)
            cur = conn.cursor()
            cur.execute("""
                SELECT f.flight_id, f.flight_number, d1.airport_iata_code, d2.airport_iata_code, f.Status 
                FROM flights f 
                JOIN destinations d1 ON f.flightOrigin = d1.destination_id 
                JOIN destinations d2 ON f.flightDestination = d2.destination_id 
                LIMIT 15
            """)
            results = cur.fetchall()
            conn.close()
            
            if results:
                print("\nAvailable flights:")
                print("-" * 80)
                for row in results:
                    print(f"Flight ID: {row[0]:<3} | Number: {row[1]:<8} | Route: {row[2]:<5} -> {row[3]:<5} | Status: {row[4]:<12}")
                print("-" * 80)
                return True
            else:
                print("No flights found in the database.")
                return False
        except Exception as e:
            print(f"Error displaying flights: {e}")
            return False

    def display_available_pilots(self):
        """Display available pilots for user to choose from"""
        try:
            conn = sqlite3.connect(self.repo.db_name)
            cur = conn.cursor()
            cur.execute("SELECT pilot_id, employee_id, first_name, last_name, pilot_rank FROM pilots LIMIT 15")
            results = cur.fetchall()
            conn.close()
            
            if results:
                print("\nAvailable pilots:")
                print("-" * 100)
                for row in results:
                    print(f"Pilot ID: {row[0]:<3} | Employee ID: {row[1]:<10} | Name: {row[2]:<15} {row[3]:<15} | Rank: {row[4]:<12}")
                print("-" * 100)
                return True
            else:
                print("No pilots found in the database.")
                return False
        except Exception as e:
            print(f"Error displaying pilots: {e}")
            return False

    def validate_flight_exists(self, flight_id):
        """Check if flight exists in database"""
        try:
            conn = sqlite3.connect(self.repo.db_name)
            cur = conn.cursor()
            cur.execute("SELECT flight_number FROM flights WHERE flight_id = ?", (flight_id,))
            result = cur.fetchone()
            conn.close()
            return result is not None
        except Exception as e:
            print(f"Error validating flight: {e}")
            return False

    def validate_pilot_exists(self, pilot_id):
        """Check if pilot exists in database"""
        try:
            conn = sqlite3.connect(self.repo.db_name)
            cur = conn.cursor()
            cur.execute("SELECT employee_id FROM pilots WHERE pilot_id = ?", (pilot_id,))
            result = cur.fetchone()
            conn.close()
            return result is not None
        except Exception as e:
            print(f"Error validating pilot: {e}")
            return False

    def create_input_flight_crew_data(self):
        """Collect flight crew information from user input"""
        try:
            # Display available flights
            if not self.display_available_flights():
                return
            
            # Get flight ID
            try:
                flight_id = int(input("Enter Flight ID: ").strip())
            except ValueError:
                print("Invalid flight ID. Please enter a number.")
                return
            
            if not self.validate_flight_exists(flight_id):
                print(f"Flight ID {flight_id} not found in database.")
                return
            
            # Display available pilots
            if not self.display_available_pilots():
                return
            
            # Get pilot ID
            try:
                pilot_id = int(input("Enter Pilot ID: ").strip())
            except ValueError:
                print("Invalid pilot ID. Please enter a number.")
                return
            
            if not self.validate_pilot_exists(pilot_id):
                print(f"Pilot ID {pilot_id} not found in database.")
                return
            
            # Get role
            print("Role options:")
            print("1. Captain")
            print("2. First Officer")
            role_choice = input("Select role (1-2): ").strip()
            
            role_mapping = {
                "1": "Captain",
                "2": "First Officer"
            }
            
            role = role_mapping.get(role_choice)
            if not role:
                print("Invalid role selection.")
                return
            
            # Get flying pilot status
            is_flying = input("Is flying pilot? (yes/no): ").lower() in ("y", "yes")
            
            # Confirm before inserting
            print(f"\nConfirm flight crew details:")
            print(f"  Flight ID: {flight_id}")
            print(f"  Pilot ID: {pilot_id}")
            print(f"  Role: {role}")
            print(f"  Flying Pilot: {'Yes' if is_flying else 'No'}")
            
            confirm = input("Is this correct? (yes/no): ").lower()
            if confirm != "yes" and confirm != "y":
                print("Insertion cancelled.")
                return
            
            # Insert the flight crew
            self.repo.insert_flight_crew_data(flight_id, pilot_id, role, is_flying)
            print("\nOperation Complete. Returning to main menu...")
            
        except Exception as e:
            print(f"Error: {e}")
