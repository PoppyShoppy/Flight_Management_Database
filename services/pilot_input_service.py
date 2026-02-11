from tabulate import tabulate


class PilotInputService:

    def __init__(self, db_operations):
        self.repo = db_operations

    def get_existing_pilots(self):
        ###Display existing pilots to help user input###
        try:
            results = self.repo.list_pilots()
            if results:
                print("\nExisting pilots:")
                print(tabulate(results, headers=["ID", "Employee ID", "First Name", "Last Name", "Rank"], tablefmt="grid"))
        except Exception as e:
            print("Could not display existing pilots: " + str(e))

    def create_input_pilot_data(self):
        ###Collect pilot information from user input###
        try:
            self.get_existing_pilots()

            while True:
                employee_id = input("Enter employee ID (e.g., EMP001): ").upper().strip()
                if not employee_id:
                    print("Employee ID cannot be empty.")
                    continue
                break

            while True:
                first_name = input("Enter first name: ").strip()
                if not first_name:
                    print("First name cannot be empty.")
                    continue
                break

            while True:
                last_name = input("Enter last name: ").strip()
                if not last_name:
                    print("Last name cannot be empty.")
                    continue
                break

            while True:
                contact_number = input("Enter contact number (e.g., +44-555555555): ").strip()
                if not contact_number:
                    print("Contact number cannot be empty.")
                    continue
                break

            while True:
                license_number = input("Enter license number (e.g., LIC123456): ").upper().strip()
                if not license_number:
                    print("License number cannot be empty.")
                    continue
                break
            
            while True:
                # Rank menu: map numeric choice to pilot rank.
                print("Pilot rank options:")
                print("1. Captain")
                print("2. First Officer")
                print("3. Second Officer")
                try:
                    rank_choice = input("Select pilot rank (1-3): ").strip()
                    rank_mapping = {
                        "1": "Captain",
                        "2": "First Officer",
                        "3": "Second Officer"
                    }
                    pilot_rank = rank_mapping.get(rank_choice)
                    if not pilot_rank:
                        print("Invalid rank selection. Please enter 1, 2, or 3.")
                        continue
                    break
                except Exception as e:
                    print("Error: " + str(e))
            
            # Confirm before inserting
            print("\nConfirm pilot details:")
            print("  Employee ID: " + str(employee_id))
            print("  Name: " + str(first_name) + " " + str(last_name))
            print("  Contact: " + str(contact_number))
            print("  License: " + str(license_number))
            print("  Rank: " + str(pilot_rank))
            
            while True:
                confirm = input("Is this correct? (yes/no): ").strip().lower()
                if confirm in ("yes", "y"):
                    break
                if confirm in ("no", "n"):
                    print("Insertion cancelled.")
                    return
                print("Please enter yes or no.")
            
            # Insert the pilot
            inserted_id = self.repo.insert_pilot_data(employee_id, first_name, last_name, contact_number, license_number, pilot_rank)
            print("\nInserted pilot id: " + str(inserted_id))
            print("Operation Complete. Returning to main menu...")
            
        except Exception as e:
            print("Error: " + str(e))
