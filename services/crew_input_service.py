from tabulate import tabulate


class CrewInputService:

    def __init__(self, db_operations):
        self.repo = db_operations

    def display_available_flights(self):
        ###Display available flights for user to choose from###
        try:
            results = self.repo.list_flights()
            if results:
                print("\nAvailable flights:")
                print(tabulate(results, headers=["Flight ID", "Number", "Origin", "Destination", "Status"], tablefmt="grid"))
                return True
            else:
                print("No flights found in the database.")
                return False
        except Exception as e:
            print("Error displaying flights: " + str(e))
            return False

    def display_available_pilots(self):
        ###Display available pilots for user to choose from###
        try:
            results = self.repo.list_pilots()
            if results:
                print("\nAvailable pilots:")
                print(tabulate(results, headers=["Pilot ID", "Employee ID", "First Name", "Last Name", "Rank"], tablefmt="grid"))
                return True
            else:
                print("No pilots found in the database.")
                return False
        except Exception as e:
            print("Error displaying pilots: " + str(e))
            return False

    def validate_flight_exists(self, flight_id):
        ###Check if flight exists in database###
        try:
            return self.repo.validate_flight_exists(flight_id)
        except Exception as e:
            print("Error validating flight: " + str(e))
            return False

    def validate_pilot_exists(self, pilot_id):
        ###Check if pilot exists in database###
        try:
            return self.repo.validate_pilot_exists(pilot_id)
        except Exception as e:
            print("Error validating pilot: " + str(e))
            return False

    def create_input_flight_crew_data(self):
        ###Collect flight crew information from user input###
        try:
            # Display available flights
            if not self.display_available_flights():
                return

            # Get flight ID
            while True:
                try:
                    flight_id = int(input("Enter Flight ID: ").strip())
                except ValueError:
                    print("Invalid flight ID. Please enter a number.")
                    continue
                if not self.validate_flight_exists(flight_id):
                    print("Flight ID " + str(flight_id) + " not found in database.")
                    continue
                break
            
            # Display available pilots
            if not self.display_available_pilots():
                return

            # Get pilot ID
            while True:
                try:
                    pilot_id = int(input("Enter Pilot ID: ").strip())
                except ValueError:
                    print("Invalid pilot ID. Please enter a number.")
                    continue
                if not self.validate_pilot_exists(pilot_id):
                    print("Pilot ID " + str(pilot_id) + " not found in database.")
                    continue
                break
            
            # Get role
            while True:
                print("Role options:")
                print("1. Captain")
                print("2. First Officer")
                try:
                    role_choice = input("Select role (1-2): ").strip()
                    role_mapping = {
                        "1": "Captain",
                        "2": "First Officer"
                    }
                    role = role_mapping.get(role_choice)
                    if not role:
                        print("Invalid role selection. Please enter 1 or 2.")
                        continue
                    break
                except Exception as e:
                    print("Error: " + str(e))
            
            # Get flying pilot status
            while True:
                is_flying_input = input("Is flying pilot? (yes/no): ").strip().lower()
                if is_flying_input in ("y", "yes"):
                    is_flying = True
                    break
                if is_flying_input in ("n", "no"):
                    is_flying = False
                    break
                print("Please enter yes or no.")
            
            # Confirm before inserting
            print("\nConfirm flight crew details:")
            print("  Flight ID: " + str(flight_id))
            print("  Pilot ID: " + str(pilot_id))
            print("  Role: " + str(role))
            print("  Flying Pilot: " + ("Yes" if is_flying else "No"))
            
            while True:
                confirm = input("Is this correct? (yes/no): ").strip().lower()
                if confirm in ("yes", "y"):
                    break
                if confirm in ("no", "n"):
                    print("Insertion cancelled.")
                    return
                print("Please enter yes or no.")
            
            # Insert the flight crew
            inserted_id = self.repo.insert_flight_crew_data(flight_id, pilot_id, role, is_flying)
            print("\nInserted flight_crew id: " + str(inserted_id))
            print("Operation Complete. Returning to main menu...")
            
        except Exception as e:
            print("Error: " + str(e))
