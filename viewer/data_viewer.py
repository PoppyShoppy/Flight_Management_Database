import sqlite3
from tabulate import tabulate
from db import DBConnection
from repository.data_repository import DBOperations


class DataViewer:
    ### This class handles all the view and display operations, this was originally inside the data_repository but it got too big to manage. ###
    
    # SQL queries for select operations (used by select_all and helper display methods)
    sql_select_all_flights = (
        "SELECT f.FlightID, f.flight_number, f.scheduled_departure, f.Status, d1.airport_iata_code AS Origin, "
        "d2.airport_iata_code AS Destination "
        "FROM flights f "
        "JOIN destinations d1 ON f.flightOrigin = d1.destination_id "
        "JOIN destinations d2 ON f.flightDestination = d2.destination_id"
    )
    sql_select_all_destinations = "SELECT destination_id, airport_iata_code, airport_name, city, country FROM destinations"
    sql_select_all_pilots = "SELECT pilot_id, employee_id, first_name, last_name, contact_number, license_number, pilot_rank FROM pilots"
    sql_select_all_flight_crew = "SELECT flight_crew_id, flight_id, pilot_id, role, is_flying_pilot FROM flight_crew"

    def __init__(self):
        self.db = DBOperations()

    def get_connection(self):
        conn = DBConnection.get_connection()
        return conn

    # ==================== GENERIC DISPLAY HELPER ====================
    
    def _display_table(self, query, headers, headers_map=None, column_count=None):
        """
        Generic method to execute a query and display results in a formatted table.
        
        Args:
            query: SQL query to execute
            headers: List of column headers for display
            headers_map: Optional function to map/transform row data
            column_count: Number of columns expected (if headers_map is None, all rows used)
        """
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute(query)
            result = cur.fetchall()
            if result:
                if headers_map:
                    rows = [headers_map(row) for row in result]
                else:
                    rows = [[row[i] for i in range(column_count)] for row in result]
                print("\n" + tabulate(rows, headers=headers, tablefmt="grid"))
            else:
                print("No records found.")
        except Exception as e:
            print("Error displaying table: " + str(e))
        finally:
            try:
                conn.close()
            except Exception:
                pass

    # Helper methods to show lists programmatically (used by update/delete convenience)
    def show_all_flights(self):
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute(self.sql_select_all_flights)
            result = cur.fetchall()
            if result:
                rows = [[r[0], r[1], r[2], r[3], r[4], r[5]] for r in result]
                print("\n" + tabulate(rows, headers=["Flight ID", "Number", "Departure", "Status", "Origin", "Destination"], tablefmt="grid"))
            else:
                print("No flights found.")
        except Exception as e:
            print("Error showing flights: " + str(e))
        finally:
            try:
                conn.close()
            except Exception:
                pass

    def show_all_destinations(self):
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute(self.sql_select_all_destinations)
            result = cur.fetchall()
            if result:
                rows = [[r[0], r[1], r[2], r[3], r[4]] for r in result]
                print("\n" + tabulate(rows, headers=["ID", "IATA", "Airport", "City", "Country"], tablefmt="grid"))
            else:
                print("No destinations found.")
        except Exception as e:
            print("Error showing destinations: " + str(e))
        finally:
            try:
                conn.close()
            except Exception:
                pass

    def show_all_pilots(self):
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute(self.sql_select_all_pilots)
            result = cur.fetchall()
            if result:
                rows = [[r[0], r[1], r[2], r[3], r[4], r[5], r[6]] for r in result]
                print("\n" + tabulate(rows, headers=["ID", "Employee", "First", "Last", "Contact", "License", "Rank"], tablefmt="grid"))
            else:
                print("No pilots found.")
        except Exception as e:
            print("Error showing pilots: " + str(e))
        finally:
            try:
                conn.close()
            except Exception:
                pass

    def show_all_flight_crew(self):
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute(self.sql_select_all_flight_crew)
            result = cur.fetchall()
            if result:
                rows = [[r[0], r[1], r[2], r[3], "Yes" if r[4] else "No"] for r in result]
                print("\n" + tabulate(rows, headers=["Crew ID", "Flight", "Pilot", "Role", "Flying"], tablefmt="grid"))
            else:
                print("No crew records found.")
        except Exception as e:
            print("Error showing flight crew: " + str(e))
        finally:
            try:
                conn.close()
            except Exception:
                pass

    def select_all(self):
        ###Display all records from selected table.###
        try:
            try:
                select_all_choice = int(input("\nWhat table do you want to select from?\n1. Flights\n2. Destinations\n3. Pilots\n4. Flight_crew\n5. Exit Menu\nEnter your choice: "))
            except ValueError:
                print("Please enter a valid number.")
                return
            
            conn = self.get_connection()
            cur = conn.cursor()
            
            if select_all_choice == 1:
                cur.execute(self.sql_select_all_flights)
                result = cur.fetchall()
                if result:
                    rows = [[row[0], row[1], row[2], row[3], row[4], row[5]] for row in result]
                    print("\n" + tabulate(rows, headers=["Flight ID", "Number", "Departure", "Status", "Origin", "Destination"], tablefmt="grid"))
                else:
                    print("No records found.")
                    
            elif select_all_choice == 2:
                cur.execute(self.sql_select_all_destinations)
                result = cur.fetchall()
                if result:
                    rows = [[row[0], row[1], row[2], row[3], row[4]] for row in result]
                    print("\n" + tabulate(rows, headers=["ID", "IATA", "Airport", "City", "Country"], tablefmt="grid"))
                else:
                    print("No records found.")
                    
            elif select_all_choice == 3:
                cur.execute(self.sql_select_all_pilots)
                result = cur.fetchall()
                if result:
                    rows = [[row[0], row[1], row[2], row[3], row[4], row[5], row[6]] for row in result]
                    print("\n" + tabulate(rows, headers=["ID", "Employee", "First Name", "Last Name", "Contact", "License", "Rank"], tablefmt="grid"))
                else:
                    print("No records found.")
                    
            elif select_all_choice == 4:
                cur.execute(self.sql_select_all_flight_crew)
                result = cur.fetchall()
                if result:
                    rows = [[row[0], row[1], row[2], row[3], "Yes" if row[4] else "No"] for row in result]
                    print("\n" + tabulate(rows, headers=["Crew ID", "Flight", "Pilot", "Role", "Flying"], tablefmt="grid"))
                else:
                    print("No records found.")
                    
            elif select_all_choice == 5:
                return
            else:
                print("Invalid Choice")
                return
            
            print()

        except Exception as e:
            print("Error: " + str(e))
        finally:
            try:
                conn.close()
            except Exception:
                pass

    def search_data(self):
        ###Search for records across all tables.###
        try:
            search_choice = int(input("\nSearch in which table?\n1. Flights\n2. Destinations\n3. Pilots\n4. Flight Crew\n5. Cancel\nEnter your choice: "))
            
            if search_choice == 1:
                # Search Flights
                try:
                    flight_id = int(input("Enter Flight ID to search: "))
                except ValueError:
                    print("Please enter a valid number for Flight ID.")
                    return
                    
                result = self.db.search_flight_by_id(flight_id)
                if result:
                    rows = [[row[0], row[1], row[2], row[3], row[4]] for row in result]
                    print("\n" + tabulate(rows, headers=["Flight ID", "Number", "Status", "Origin", "Destination"], tablefmt="grid"))
                else:
                    print("No flight found with that ID.")
            
            elif search_choice == 2:
                # Search Destinations
                search_term = input("Enter city or IATA code to search: ").strip().upper()
                result = self.db.search_destinations(search_term)
                if result:
                    rows = [[row[0], row[1], row[2], row[3], row[4]] for row in result]
                    print("\n" + tabulate(rows, headers=["ID", "IATA", "Airport", "City", "Country"], tablefmt="grid"))
                else:
                    print("No destinations found matching that search.")
            
            elif search_choice == 3:
                # Search Pilots
                search_term = input("Enter pilot name or employee ID to search: ").strip().upper()
                result = self.db.search_pilots(search_term)
                if result:
                    rows = [[row[0], row[1], row[2], row[3], row[4], row[5], row[6]] for row in result]
                    print("\n" + tabulate(rows, headers=["ID", "Employee", "First", "Last", "Contact", "License", "Rank"], tablefmt="grid"))
                else:
                    print("No pilots found matching that search.")
            
            elif search_choice == 4:
                # Search Flight Crew
                try:
                    flight_id = int(input("Enter Flight ID to find crew: "))
                except ValueError:
                    print("Please enter a valid number for Flight ID.")
                    return
                    
                result = self.db.search_flight_crew(flight_id)
                if result:
                    rows = [[row[0], row[1], row[2], row[3], "Yes" if row[4] else "No"] for row in result]
                    print("\n" + tabulate(rows, headers=["Crew ID", "Flight", "Pilot", "Role", "Flying"], tablefmt="grid"))
                else:
                    print("No crew found for that flight.")
            
            elif search_choice == 5:
                return
            else:
                print("Invalid choice.")

        except ValueError:
            print("Please enter a valid number.")
        except Exception as e:
            print("Error: " + str(e))

    def update_data(self):
        ###Update records in selected table.###
        try:
            update_choice = int(input("\nUpdate which table?\n1. Flights\n2. Destinations\n3. Pilots\n4. Flight Crew\n5. Cancel\nEnter your choice: "))
            
            if update_choice == 1:
                # Update Flight
                while True:
                    flight_id_input = input("Enter Flight ID to update (or 'x' to list flights): ").strip()
                    if flight_id_input.lower() == 'x':
                        self.show_all_flights()
                        continue
                    try:
                        flight_id = int(flight_id_input)
                        break
                    except ValueError:
                        print("Please enter a valid number or 'x'.")

                if not self.db.flight_exists(flight_id):
                    print("Flight not found.")
                    return
                
                print("\nWhat would you like to update?")
                print("1. Flight Number")
                print("2. Status")
                print("3. Origin")
                print("4. Destination")
                field_choice = int(input("Enter your choice: "))
                
                if field_choice == 1:
                    new_value = input("Enter new flight number (e.g., BB123): ").upper()
                    self.db.update_flight_number(flight_id, new_value)
                elif field_choice == 2:
                    print("1. On Time\n2. Delayed\n3. Cancelled")
                    status_choice = int(input("Enter status: "))
                    statuses = {1: "On Time", 2: "Delayed", 3: "Cancelled"}
                    new_value = statuses.get(status_choice)
                    if not new_value:
                        print("Invalid status.")
                        return
                    self.db.update_flight_status(flight_id, new_value)
                elif field_choice == 3:
                    new_value = int(input("Enter new origin destination_id: "))
                    self.db.update_flight_origin(flight_id, new_value)
                elif field_choice == 4:
                    new_value = int(input("Enter new destination destination_id: "))
                    self.db.update_flight_destination(flight_id, new_value)
                else:
                    print("Invalid choice.")
                    return
                
                print("Flight updated successfully.")
            
            elif update_choice == 2:
                # Update Destination
                while True:
                    dest_id_input = input("Enter Destination ID to update (or 'x' to list destinations): ").strip()
                    if dest_id_input.lower() == 'x':
                        self.show_all_destinations()
                        continue
                    try:
                        dest_id = int(dest_id_input)
                        break
                    except ValueError:
                        print("Please enter a valid number or 'x'.")

                if not self.db.destination_exists(dest_id):
                    print("Destination not found.")
                    return
                
                print("\nWhat would you like to update?")
                print("1. IATA Code")
                print("2. Airport Name")
                print("3. City")
                print("4. Country")
                field_choice = int(input("Enter your choice: "))
                
                if field_choice == 1:
                    new_value = input("Enter new IATA code: ").upper()
                    self.db.update_destination_iata(dest_id, new_value)
                elif field_choice == 2:
                    new_value = input("Enter new airport name: ")
                    self.db.update_destination_name(dest_id, new_value)
                elif field_choice == 3:
                    new_value = input("Enter new city: ")
                    self.db.update_destination_city(dest_id, new_value)
                elif field_choice == 4:
                    new_value = input("Enter new country: ")
                    self.db.update_destination_country(dest_id, new_value)
                else:
                    print("Invalid choice.")
                    return
                
                print("Destination updated successfully.")
            
            elif update_choice == 3:
                # Update Pilot
                while True:
                    pilot_id_input = input("Enter Pilot ID to update (or 'x' to list pilots): ").strip()
                    if pilot_id_input.lower() == 'x':
                        self.show_all_pilots()
                        continue
                    try:
                        pilot_id = int(pilot_id_input)
                        break
                    except ValueError:
                        print("Please enter a valid number or 'x'.")

                if not self.db.pilot_exists(pilot_id):
                    print("Pilot not found.")
                    return
                
                print("\nWhat would you like to update?")
                print("1. Employee ID")
                print("2. First Name")
                print("3. Last Name")
                print("4. Contact Number")
                print("5. License Number")
                print("6. Pilot Rank")
                field_choice = int(input("Enter your choice: "))
                
                if field_choice == 1:
                    new_value = input("Enter new employee ID: ")
                    self.db.update_pilot_employee_id(pilot_id, new_value)
                elif field_choice == 2:
                    new_value = input("Enter new first name: ")
                    self.db.update_pilot_first_name(pilot_id, new_value)
                elif field_choice == 3:
                    new_value = input("Enter new last name: ")
                    self.db.update_pilot_last_name(pilot_id, new_value)
                elif field_choice == 4:
                    new_value = input("Enter new contact number: ")
                    self.db.update_pilot_contact(pilot_id, new_value)
                elif field_choice == 5:
                    new_value = input("Enter new license number: ")
                    self.db.update_pilot_license(pilot_id, new_value)
                elif field_choice == 6:
                    new_value = input("Enter new pilot rank: ")
                    self.db.update_pilot_rank(pilot_id, new_value)
                else:
                    print("Invalid choice.")
                    return
                
                print("Pilot updated successfully.")
            
            elif update_choice == 4:
                # Update Flight Crew
                while True:
                    crew_id_input = input("Enter Flight Crew ID to update (or 'x' to list crew): ").strip()
                    if crew_id_input.lower() == 'x':
                        self.show_all_flight_crew()
                        continue
                    try:
                        crew_id = int(crew_id_input)
                        break
                    except ValueError:
                        print("Please enter a valid number or 'x'.")

                if not self.db.crew_exists(crew_id):
                    print("Flight Crew record not found.")
                    return
                
                print("\nWhat would you like to update?")
                print("1. Role")
                print("2. Is Flying Pilot")
                field_choice = int(input("Enter your choice: "))
                
                if field_choice == 1:
                    new_value = input("Enter new role (Captain/First Officer): ")
                    self.db.update_crew_role(crew_id, new_value)
                elif field_choice == 2:
                    is_flying = input("Is flying pilot? (yes/no): ").lower() in ("y", "yes")
                    self.db.update_crew_flying_pilot(crew_id, int(is_flying))
                else:
                    print("Invalid choice.")
                    return
                
                print("Flight Crew record updated successfully.")
            
            elif update_choice == 5:
                return
            else:
                print("Invalid choice.")

        except ValueError:
            print("Please enter a valid number.")
        except Exception as e:
            print("Error: " + str(e))

    def delete_data(self):
        ###Delete records from selected table.###
        try:
            delete_choice = int(input("\nDelete from which table?\n1. Flights\n2. Destinations\n3. Pilots\n4. Flight Crew\n5. Cancel\nEnter your choice: "))
            
            if delete_choice == 1:
                # Delete Flight
                while True:
                    flight_id_input = input("Enter Flight ID to delete (or 'x' to list flights): ").strip()
                    if flight_id_input.lower() == 'x':
                        self.show_all_flights()
                        continue
                    try:
                        flight_id = int(flight_id_input)
                        break
                    except ValueError:
                        print("Please enter a valid number or 'x'.")

                if not self.db.flight_exists(flight_id):
                    print("Flight not found.")
                    return

                confirm = input("Are you sure you want to delete flight " + str(flight_id) + "? (yes/no): ").lower()
                if confirm in ("yes", "y"):
                    self.db.delete_flight(flight_id)
                    print("Flight " + str(flight_id) + " deleted successfully.")
                else:
                    print("Deletion cancelled.")
            
            elif delete_choice == 2:
                # Delete Destination
                while True:
                    dest_id_input = input("Enter Destination ID to delete (or 'x' to list destinations): ").strip()
                    if dest_id_input.lower() == 'x':
                        self.show_all_destinations()
                        continue
                    try:
                        dest_id = int(dest_id_input)
                        break
                    except ValueError:
                        print("Please enter a valid number or 'x'.")

                if not self.db.destination_exists(dest_id):
                    print("Destination not found.")
                    return

                confirm = input("Are you sure you want to delete destination " + str(dest_id) + "? (yes/no): ").lower()
                if confirm in ("yes", "y"):
                    self.db.delete_destination(dest_id)
                    print("Destination " + str(dest_id) + " deleted successfully.")
                else:
                    print("Deletion cancelled.")
            
            elif delete_choice == 3:
                # Delete Pilot
                while True:
                    pilot_id_input = input("Enter Pilot ID to delete (or 'x' to list pilots): ").strip()
                    if pilot_id_input.lower() == 'x':
                        self.show_all_pilots()
                        continue
                    try:
                        pilot_id = int(pilot_id_input)
                        break
                    except ValueError:
                        print("Please enter a valid number or 'x'.")

                if not self.db.pilot_exists(pilot_id):
                    print("Pilot not found.")
                    return

                confirm = input("Are you sure you want to delete pilot " + str(pilot_id) + "? (yes/no): ").lower()
                if confirm in ("yes", "y"):
                    self.db.delete_pilot(pilot_id)
                    print("Pilot " + str(pilot_id) + " deleted successfully.")
                else:
                    print("Deletion cancelled.")
            
            elif delete_choice == 4:
                # Delete Flight Crew
                while True:
                    crew_id_input = input("Enter Flight Crew ID to delete (or 'x' to list crew): ").strip()
                    if crew_id_input.lower() == 'x':
                        self.show_all_flight_crew()
                        continue
                    try:
                        crew_id = int(crew_id_input)
                        break
                    except ValueError:
                        print("Please enter a valid number or 'x'.")

                if not self.db.crew_exists(crew_id):
                    print("Flight Crew record not found.")
                    return

                confirm = input("Are you sure you want to delete crew record " + str(crew_id) + "? (yes/no): ").lower()
                if confirm in ("yes", "y"):
                    self.db.delete_flight_crew(crew_id)
                    print("Flight Crew record " + str(crew_id) + " deleted successfully.")
                else:
                    print("Deletion cancelled.")
            
            elif delete_choice == 5:
                return
            else:
                print("Invalid choice.")

        except ValueError:
            print("Please enter a valid number.")
        except Exception as e:
            print("Error: " + str(e))
