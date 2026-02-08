import sqlite3
from tabulate import tabulate
from db import DBConnection


class DataViewer:
    ### This class handles all the view and display operations, this was originally inside the data_repository but it got too big to manage. ###
    
    # SQL queries for select operations (used by select_all and helper display methods)
    sql_select_all_flights = (
        "SELECT f.FlightID, f.flight_number, f.Status, d1.airport_iata_code AS Origin, "
        "d2.airport_iata_code AS Destination "
        "FROM flights f "
        "JOIN destinations d1 ON f.flightOrigin = d1.destination_id "
        "JOIN destinations d2 ON f.flightDestination = d2.destination_id"
    )
    sql_select_all_destinations = "SELECT destination_id, airport_iata_code, airport_name, city, country FROM destinations"
    sql_select_all_pilots = "SELECT pilot_id, employee_id, first_name, last_name, contact_number, license_number, pilot_rank FROM pilots"
    sql_select_all_flight_crew = "SELECT flight_crew_id, flight_id, pilot_id, role, is_flying_pilot FROM flight_crew"

    def __init__(self):
        pass

    def get_connection(self):
        conn = DBConnection.get_connection()
        return conn

    # Helper methods to show lists programmatically (used by update/delete convenience)
    def show_all_flights(self):
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute(self.sql_select_all_flights)
            result = cur.fetchall()
            if result:
                rows = [[r[0], r[1], r[2], r[3], r[4]] for r in result]
                print("\n" + tabulate(rows, headers=["Flight ID", "Number", "Status", "Origin", "Destination"], tablefmt="grid"))
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
                    rows = [[row[0], row[1], row[2], row[3], row[4]] for row in result]
                    print("\n" + tabulate(rows, headers=["Flight ID", "Number", "Status", "Origin", "Destination"], tablefmt="grid"))
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
            conn = self.get_connection()
            cur = conn.cursor()
            
            search_choice = int(input("\nSearch in which table?\n1. Flights\n2. Destinations\n3. Pilots\n4. Flight Crew\n5. Cancel\nEnter your choice: "))
            
            if search_choice == 1:
                # Search Flights
                try:
                    flight_id = int(input("Enter Flight ID to search: "))
                except ValueError:
                    print("Please enter a valid number for Flight ID.")
                    return
                    
                cur.execute("SELECT FlightID, flight_number, Status, flightOrigin, flightDestination FROM flights WHERE FlightID = ?", (flight_id,))
                result = cur.fetchall()
                if result:
                    rows = [[row[0], row[1], row[2], row[3], row[4]] for row in result]
                    print("\n" + tabulate(rows, headers=["Flight ID", "Number", "Status", "Origin", "Destination"], tablefmt="grid"))
                else:
                    print("No flight found with that ID.")
            
            elif search_choice == 2:
                # Search Destinations
                search_term = input("Enter city or IATA code to search: ").strip().upper()
                cur.execute(
                    "SELECT destination_id, airport_iata_code, airport_name, city, country FROM destinations WHERE city LIKE ? OR airport_iata_code LIKE ?",
                    (f"%{search_term}%", f"%{search_term}%")
                )
                result = cur.fetchall()
                if result:
                    rows = [[row[0], row[1], row[2], row[3], row[4]] for row in result]
                    print("\n" + tabulate(rows, headers=["ID", "IATA", "Airport", "City", "Country"], tablefmt="grid"))
                else:
                    print("No destinations found matching that search.")
            
            elif search_choice == 3:
                # Search Pilots
                search_term = input("Enter pilot name or employee ID to search: ").strip().upper()
                cur.execute(
                    "SELECT pilot_id, employee_id, first_name, last_name, contact_number, license_number, pilot_rank FROM pilots WHERE first_name LIKE ? OR last_name LIKE ? OR employee_id LIKE ?",
                    (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%")
                )
                result = cur.fetchall()
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
                    
                cur.execute("SELECT flight_crew_id, flight_id, pilot_id, role, is_flying_pilot FROM flight_crew WHERE flight_id = ?", (flight_id,))
                result = cur.fetchall()
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
        finally:
            conn.close()

    def update_data(self):
        ###Update records in selected table.###
        try:
            conn = self.get_connection()
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            
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

                cur.execute("SELECT * FROM flights WHERE FlightID = ?", (flight_id,))
                if not cur.fetchone():
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
                    cur.execute("UPDATE flights SET flight_number = ? WHERE FlightID = ?", (new_value, flight_id))
                elif field_choice == 2:
                    print("1. On Time\n2. Delayed\n3. Cancelled")
                    status_choice = int(input("Enter status: "))
                    statuses = {1: "On Time", 2: "Delayed", 3: "Cancelled"}
                    new_value = statuses.get(status_choice)
                    if not new_value:
                        print("Invalid status.")
                        return
                    cur.execute("UPDATE flights SET Status = ? WHERE FlightID = ?", (new_value, flight_id))
                elif field_choice == 3:
                    new_value = int(input("Enter new origin destination_id: "))
                    cur.execute("UPDATE flights SET flightOrigin = ? WHERE FlightID = ?", (new_value, flight_id))
                elif field_choice == 4:
                    new_value = int(input("Enter new destination destination_id: "))
                    cur.execute("UPDATE flights SET flightDestination = ? WHERE FlightID = ?", (new_value, flight_id))
                else:
                    print("Invalid choice.")
                    return
                
                conn.commit()
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

                cur.execute("SELECT * FROM destinations WHERE destination_id = ?", (dest_id,))
                if not cur.fetchone():
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
                    cur.execute("UPDATE destinations SET airport_iata_code = ? WHERE destination_id = ?", (new_value, dest_id))
                elif field_choice == 2:
                    new_value = input("Enter new airport name: ")
                    cur.execute("UPDATE destinations SET airport_name = ? WHERE destination_id = ?", (new_value, dest_id))
                elif field_choice == 3:
                    new_value = input("Enter new city: ")
                    cur.execute("UPDATE destinations SET city = ? WHERE destination_id = ?", (new_value, dest_id))
                elif field_choice == 4:
                    new_value = input("Enter new country: ")
                    cur.execute("UPDATE destinations SET country = ? WHERE destination_id = ?", (new_value, dest_id))
                else:
                    print("Invalid choice.")
                    return
                
                conn.commit()
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

                cur.execute("SELECT * FROM pilots WHERE pilot_id = ?", (pilot_id,))
                if not cur.fetchone():
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
                    cur.execute("UPDATE pilots SET employee_id = ? WHERE pilot_id = ?", (new_value, pilot_id))
                elif field_choice == 2:
                    new_value = input("Enter new first name: ")
                    cur.execute("UPDATE pilots SET first_name = ? WHERE pilot_id = ?", (new_value, pilot_id))
                elif field_choice == 3:
                    new_value = input("Enter new last name: ")
                    cur.execute("UPDATE pilots SET last_name = ? WHERE pilot_id = ?", (new_value, pilot_id))
                elif field_choice == 4:
                    new_value = input("Enter new contact number: ")
                    cur.execute("UPDATE pilots SET contact_number = ? WHERE pilot_id = ?", (new_value, pilot_id))
                elif field_choice == 5:
                    new_value = input("Enter new license number: ")
                    cur.execute("UPDATE pilots SET license_number = ? WHERE pilot_id = ?", (new_value, pilot_id))
                elif field_choice == 6:
                    new_value = input("Enter new pilot rank: ")
                    cur.execute("UPDATE pilots SET pilot_rank = ? WHERE pilot_id = ?", (new_value, pilot_id))
                else:
                    print("Invalid choice.")
                    return
                
                conn.commit()
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

                cur.execute("SELECT * FROM flight_crew WHERE flight_crew_id = ?", (crew_id,))
                if not cur.fetchone():
                    print("Flight Crew record not found.")
                    return
                
                print("\nWhat would you like to update?")
                print("1. Role")
                print("2. Is Flying Pilot")
                field_choice = int(input("Enter your choice: "))
                
                if field_choice == 1:
                    new_value = input("Enter new role (Captain/First Officer): ")
                    cur.execute("UPDATE flight_crew SET role = ? WHERE flight_crew_id = ?", (new_value, crew_id))
                elif field_choice == 2:
                    is_flying = input("Is flying pilot? (yes/no): ").lower() in ("y", "yes")
                    cur.execute("UPDATE flight_crew SET is_flying_pilot = ? WHERE flight_crew_id = ?", (int(is_flying), crew_id))
                else:
                    print("Invalid choice.")
                    return
                
                conn.commit()
                print("Flight Crew record updated successfully.")
            
            elif update_choice == 5:
                return
            else:
                print("Invalid choice.")

        except ValueError:
            print("Please enter a valid number.")
        except Exception as e:
            print("Error: " + str(e))
        finally:
            conn.close()

    def delete_data(self):
        ###Delete records from selected table.###
        try:
            conn = self.get_connection()
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            
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

                cur.execute("SELECT * FROM flights WHERE FlightID = ?", (flight_id,))
                if not cur.fetchone():
                    print("Flight not found.")
                    return

                confirm = input("Are you sure you want to delete flight " + str(flight_id) + "? (yes/no): ").lower()
                if confirm in ("yes", "y"):
                    cur.execute("DELETE FROM flights WHERE FlightID = ?", (flight_id,))
                    conn.commit()
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

                cur.execute("SELECT * FROM destinations WHERE destination_id = ?", (dest_id,))
                if not cur.fetchone():
                    print("Destination not found.")
                    return

                confirm = input("Are you sure you want to delete destination " + str(dest_id) + "? (yes/no): ").lower()
                if confirm in ("yes", "y"):
                    cur.execute("DELETE FROM destinations WHERE destination_id = ?", (dest_id,))
                    conn.commit()
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

                cur.execute("SELECT * FROM pilots WHERE pilot_id = ?", (pilot_id,))
                if not cur.fetchone():
                    print("Pilot not found.")
                    return

                confirm = input("Are you sure you want to delete pilot " + str(pilot_id) + "? (yes/no): ").lower()
                if confirm in ("yes", "y"):
                    cur.execute("DELETE FROM pilots WHERE pilot_id = ?", (pilot_id,))
                    conn.commit()
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

                cur.execute("SELECT * FROM flight_crew WHERE flight_crew_id = ?", (crew_id,))
                if not cur.fetchone():
                    print("Flight Crew record not found.")
                    return

                confirm = input("Are you sure you want to delete crew record " + str(crew_id) + "? (yes/no): ").lower()
                if confirm in ("yes", "y"):
                    cur.execute("DELETE FROM flight_crew WHERE flight_crew_id = ?", (crew_id,))
                    conn.commit()
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
        finally:
            conn.close()
