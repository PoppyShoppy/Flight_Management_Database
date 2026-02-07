import sqlite3


class PilotInputLayer:

    def __init__(self, db_operations):
        self.repo = db_operations

    def get_existing_pilots(self):
        """Display existing pilots to help user input"""
        try:
            conn = sqlite3.connect(self.repo.db_name)
            cur = conn.cursor()
            cur.execute("SELECT pilot_id, employee_id, first_name, last_name, pilot_rank FROM pilots LIMIT 10")
            results = cur.fetchall()
            conn.close()
            
            if results:
                print("\nSample existing pilots:")
                print("-" * 100)
                for row in results:
                    print(f"ID: {row[0]:<3} | Employee ID: {row[1]:<10} | Name: {row[2]:<15} {row[3]:<15} | Rank: {row[4]:<12}")
                print("-" * 100)
        except Exception as e:
            print(f"Could not display existing pilots: {e}")

    def create_input_pilot_data(self):
        """Collect pilot information from user input"""
        try:
            self.get_existing_pilots()
            
            employee_id = input("Enter employee ID (e.g., EMP001): ").upper().strip()
            if not employee_id:
                print("Employee ID cannot be empty.")
                return
            
            first_name = input("Enter first name: ").strip()
            if not first_name:
                print("First name cannot be empty.")
                return
            
            last_name = input("Enter last name: ").strip()
            if not last_name:
                print("Last name cannot be empty.")
                return
            
            contact_number = input("Enter contact number (e.g., +44-123-456-7890): ").strip()
            if not contact_number:
                print("Contact number cannot be empty.")
                return
            
            license_number = input("Enter license number (e.g., LIC123456): ").upper().strip()
            if not license_number:
                print("License number cannot be empty.")
                return
            
            print("Pilot rank options:")
            print("1. Captain")
            print("2. First Officer")
            print("3. Second Officer")
            rank_choice = input("Select pilot rank (1-3): ").strip()
            
            rank_mapping = {
                "1": "Captain",
                "2": "First Officer",
                "3": "Second Officer"
            }
            
            pilot_rank = rank_mapping.get(rank_choice)
            if not pilot_rank:
                print("Invalid rank selection.")
                return
            
            # Confirm before inserting
            print(f"\nConfirm pilot details:")
            print(f"  Employee ID: {employee_id}")
            print(f"  Name: {first_name} {last_name}")
            print(f"  Contact: {contact_number}")
            print(f"  License: {license_number}")
            print(f"  Rank: {pilot_rank}")
            
            confirm = input("Is this correct? (yes/no): ").lower()
            if confirm != "yes" and confirm != "y":
                print("Insertion cancelled.")
                return
            
            # Insert the pilot
            self.repo.insert_pilot_data(employee_id, first_name, last_name, contact_number, license_number, pilot_rank)
            print("\nOperation Complete. Returning to main menu...")
            
        except Exception as e:
            print(f"Error: {e}")
