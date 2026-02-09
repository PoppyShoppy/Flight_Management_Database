from models import FlightInfo
from tabulate import tabulate

class FlightInputService:

    def __init__(self, db_operations):  # This is a dependency injection which allows this code to pass database operations onto flights repository without having to create a object of the repository class here. 
        self.repo = db_operations

    def find_destination_id_by_city_or_iata(self, city_or_iata):
        ###Look up destination_id by city name or IATA code via repository.###
        return self.repo.find_destination_id_by_city_or_iata(city_or_iata)
    
    def airport_name_and_city_by_id(self, destination_id):
        ###Look up airport name and city by destination_id via repository.###
        return self.repo.get_airport_info_by_id(destination_id)
    
    def validate_destination_input(self): # Checking user input for destination/origin - loops until valid input
        while True:
            usr_input = input("Enter Flight Origin (City or IATA code): ")
            dest_id = self.find_destination_id_by_city_or_iata(usr_input) # Need this function because its unreasonable to assume that user can find the city by entering destination_id
            if dest_id is None:
                print("Destination not found in destinations table.")
                continue
            
            result = self.airport_name_and_city_by_id(dest_id)   # This check is done to make sure the user has entered a their expected and a valid city or IATA code that exists in the destinations table.
            airport_info = f"{result[0]}, {result[1]}" if result else "Unknown"
            
            if airport_info == "Unknown":
                print("Origin not found in destinations table.")
                continue
            
            response=input("Did you mean: " + airport_info + "? Type Yes or No: ")
            if response.lower() == "yes":
                return dest_id
            else:
                print("Please try again with a different city or IATA code. or check the destinations table for valid entries.")
    
    def status_menu_options(self):
        print("Flight Status Options:")
        print("1. On Time")
        print("2. Delayed")
        print("3. Cancelled")
        while True:
            try:
                status_choice = input("Enter the number corresponding to the flight status: ").strip()
                status_mapping = {
                    "1": "On Time",
                    "2": "Delayed",
                    "3": "Cancelled"
                }
                status = status_mapping.get(status_choice)
                if status is None:
                    print("Invalid status choice. Please enter 1, 2, or 3.")
                    continue
                return status
            except Exception as e:
                print("Error: " + str(e))
                continue

    # Asks for user input for flight data, some validation steps are taken where the user is asked to confirm the city as the destination id is stored in a digit. Flight status is also confirmed using numbered input by the user.
    def create_input_flight_data(self):
        flight = FlightInfo()

        # Loop for valid flight number input
        while True:
            try:
                flight_number_input = input("Enter Flight Number: e.g. BB123 for Bonobo Airlines flight 123: ")
                flight.set_flight_number(flight_number_input)
                break
            except ValueError as e:
                print("Error: " + str(e))

        flight.set_flight_origin(self.validate_destination_input())
        flight.set_flight_destination(self.validate_destination_input())

        # Get the scheduled departure time
        while True:
            try:
                departure_input = input("Enter Scheduled Departure (Format: YYYY-MM-DD HH:MM, e.g., 2026-02-15 14:30): ")
                flight.set_scheduled_departure(departure_input)
                break
            except ValueError as e:
                print("Error: " + str(e))

        flight.set_flight_status(self.status_menu_options())

        # Confirm with user before inserting into database
        print("\nConfirm flight details:")
        print("  Flight Number: " + str(flight.flight_number))
        print("  Scheduled Departure: " + str(flight.scheduled_departure))
        print("  Origin ID: " + str(flight.flightOrigin) + " i.e. " + str(self.airport_name_and_city_by_id(flight.flightOrigin)))
        print("  Destination ID: " + str(flight.flightDestination) + " i.e. " + str(self.airport_name_and_city_by_id(flight.flightDestination)))
        print("  Status: " + str(flight.status))

        while True:
            confirm = input("Is this correct? (yes/no): ").strip().lower()
            if confirm in ("yes", "y"):
                break
            if confirm in ("no", "n"):
                print("Insertion cancelled.")
                return
            print("Please enter yes or no.")

        inserted_id = self.repo.insert_flight_data(flight)
        print(flight.__str__())
        print("\nData inserted successfully with FlightID: " + str(inserted_id))
        print("Operation Complete. Returning to main menu...")
