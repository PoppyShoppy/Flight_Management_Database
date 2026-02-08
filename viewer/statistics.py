import sqlite3
from db import DBConnection


class StatisticsViewer:
    ###Handles statistics and reporting views for the flight management system.###
    
    def __init__(self):
        pass

    def get_connection(self):
        conn = DBConnection.get_connection()
        return conn

    def flights_per_destination(self):
        ###Show number of flights to each destination.###
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            
            # Get all destinations
            cur.execute("SELECT destination_id, airport_iata_code, city FROM destinations ORDER BY city")
            destinations = cur.fetchall()
            
            print("\n" + "=" * 80)
            print("FLIGHTS PER DESTINATION SUMMARY")
            print("=" * 80)
            print("Destination ID | IATA Code | City                    | Total Flights")
            print("-" * 80)
            
            for dest in destinations:
                dest_id = dest[0]
                iata = dest[1]
                city = dest[2]
                
                # Count flights to this destination
                cur.execute("SELECT COUNT(*) FROM flights WHERE flightDestination = ?", (dest_id,))
                flight_count = cur.fetchone()[0]
                
                # Print with formatting
                print(str(dest_id).ljust(15) + str(iata).ljust(10) + str(city).ljust(24) + str(flight_count))
            
            print()
                
        except Exception as e:
            print("Error: " + str(e))
        finally:
            conn.close()

    def flights_per_pilot(self):
        ###Show number of flights assigned to each pilot.###
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            
            # Get all pilots
            cur.execute("SELECT pilot_id, employee_id, first_name, last_name FROM pilots")
            pilots = cur.fetchall()
            
            print("\n" + "=" * 100)
            print("PILOT FLIGHT ASSIGNMENT SUMMARY")
            print("=" * 100)
            print("Pilot ID | Employee ID | First Name         | Last Name          | Flights Assigned")
            print("-" * 100)
            
            for pilot in pilots:
                pilot_id = pilot[0]
                emp_id = pilot[1]
                first_name = pilot[2]
                last_name = pilot[3]
                
                # Count flights for this pilot
                cur.execute("SELECT COUNT(*) FROM flight_crew WHERE pilot_id = ?", (pilot_id,))
                flight_count = cur.fetchone()[0]
                
                # Print with formatting
                print(str(pilot_id).ljust(9) + str(emp_id).ljust(12) + str(first_name).ljust(19) + str(last_name).ljust(19) + str(flight_count))
            
            print()
                
        except Exception as e:
            print("Error: " + str(e))
        finally:
            conn.close()

    def flight_status_summary(self):
        ###Show overall flight status distribution.###
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            
            # Get total number of flights
            cur.execute("SELECT COUNT(*) FROM flights")
            total_flights = cur.fetchone()[0]
            
            # Get all statuses
            cur.execute("SELECT DISTINCT Status FROM flights ORDER BY Status")
            statuses = cur.fetchall()
            
            print("\n" + "=" * 60)
            print("FLIGHT STATUS DISTRIBUTION")
            print("=" * 60)
            print("Flight Status     | Count | Percentage (%)")
            print("-" * 60)
            
            for status_row in statuses:
                status = status_row[0]
                
                # Count flights with this status
                cur.execute("SELECT COUNT(*) FROM flights WHERE Status = ?", (status,))
                count = cur.fetchone()[0]
                
                # Calculate percentage
                percentage = (count * 100) / total_flights
                percentage = round(percentage, 2)
                
                # Print with formatting
                print(str(status).ljust(18) + str(count).ljust(7) + str(percentage))
            
            print("\nTotal Flights in System: " + str(total_flights) + "\n")
                
        except Exception as e:
            print("Error: " + str(e))
        finally:
            conn.close()

    def crew_assignments_per_flight(self):
        ###Show crew assignment details for each flight.###
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            
            # Get all flights
            cur.execute("SELECT FlightID, flight_number, Status FROM flights ORDER BY FlightID")
            flights = cur.fetchall()
            
            print("\n" + "=" * 80)
            print("CREW ASSIGNMENT SUMMARY")
            print("=" * 80)
            print("Flight ID | Flight Number | Status      | Crew Count")
            print("-" * 80)
            
            for flight in flights:
                flight_id = flight[0]
                flight_number = flight[1]
                status = flight[2]
                
                # Count crew members for this flight
                cur.execute("SELECT COUNT(*) FROM flight_crew WHERE flight_id = ?", (flight_id,))
                crew_count = cur.fetchone()[0]
                
                # Print with formatting
                print(str(flight_id).ljust(10) + str(flight_number).ljust(14) + str(status).ljust(12) + str(crew_count))
            
            print()
                
        except Exception as e:
            print("Error: " + str(e))
        finally:
            conn.close()

    def pilot_role_distribution(self):
        ###Show distribution of pilot ranks in the system.###
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            
            # Get total number of pilots
            cur.execute("SELECT COUNT(*) FROM pilots")
            total_pilots = cur.fetchone()[0]
            
            # Get all distinct pilot ranks
            cur.execute("SELECT DISTINCT pilot_rank FROM pilots ORDER BY pilot_rank")
            ranks = cur.fetchall()
            
            print("\n" + "=" * 60)
            print("PILOT RANK DISTRIBUTION")
            print("=" * 60)
            print("Pilot Rank        | Count | Percentage (%)")
            print("-" * 60)
            
            for rank_row in ranks:
                rank = rank_row[0]
                
                # Count pilots with this rank
                cur.execute("SELECT COUNT(*) FROM pilots WHERE pilot_rank = ?", (rank,))
                count = cur.fetchone()[0]
                
                # Calculate percentage
                percentage = (count * 100) / total_pilots
                percentage = round(percentage, 2)
                
                # Print with formatting
                print(str(rank).ljust(18) + str(count).ljust(7) + str(percentage))
            
            print("\nTotal Pilots in System: " + str(total_pilots) + "\n")
                
        except Exception as e:
            print("Error: " + str(e))
        finally:
            conn.close()

    def destination_coverage(self):
        ###Show coverage statistics for all destinations.###
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            
            # Count total destinations
            cur.execute("SELECT COUNT(*) FROM destinations")
            total_destinations = cur.fetchone()[0]
            
            # Count destinations with flights
            cur.execute("""
                SELECT COUNT(DISTINCT flightDestination) FROM flights
            """)
            active_destinations = cur.fetchone()[0]
            
            # Calculate inactive destinations
            inactive_destinations = total_destinations - active_destinations
            
            print("\n" + "=" * 60)
            print("DESTINATION COVERAGE REPORT")
            print("=" * 60)
            print("Total Destinations: " + str(total_destinations))
            print("Active (with flights): " + str(active_destinations))
            print("Inactive: " + str(inactive_destinations))
            print()
                
        except Exception as e:
            print("Error: " + str(e))
        finally:
            conn.close()

    def view_statistics_menu(self):
        ###Display statistics menu and handle user selection.###
        while True:
            print("\n" + "=" * 60)
            print("STATISTICS AND REPORTING MENU")
            print("=" * 60)
            print("1. Flights per Destination")
            print("2. Flights per Pilot")
            print("3. Flight Status Distribution")
            print("4. Crew Assignments per Flight")
            print("5. Pilot Rank Distribution")
            print("6. Destination Coverage Report")
            print("7. Return to Main Menu")
            print("=" * 60)
            
            try:
                choice = int(input("Select an option (1-7): "))
                
                if choice == 1:
                    self.flights_per_destination()
                elif choice == 2:
                    self.flights_per_pilot()
                elif choice == 3:
                    self.flight_status_summary()
                elif choice == 4:
                    self.crew_assignments_per_flight()
                elif choice == 5:
                    self.pilot_role_distribution()
                elif choice == 6:
                    self.destination_coverage()
                elif choice == 7:
                    print("Returning to Main Menu...\n")
                    break
                else:
                    print("Invalid choice. Please select 1-7.")
                    
            except ValueError:
                print("Please enter a valid number.")
            except Exception as e:
                print("Error: " + str(e))
