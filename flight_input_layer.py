import sqlite3 
from flights_Data_Model import FlightInfo

class FlightInputLayer:

    def __init__(self, db_operations):
        self.repo = db_operations

    def find_destination_by_city_or_iata(self, city_or_iata):
        """Look up destination_id by city name or IATA code"""
        conn = sqlite3.connect(self.repo.db_name)
        cur = conn.cursor()
        query = """
        SELECT destination_id FROM destinations 
        WHERE city LIKE ? OR airport_iata_code = ?
        """
        cur.execute(query, (f"%{city_or_iata}%", city_or_iata.upper()))
        result = cur.fetchone()
        conn.close()
        return result[0] if result else None
    
    def airport_name_and_city_by_id(self, destination_id):
        """Look up airport name and city by destination_id"""
        conn = sqlite3.connect(self.repo.db_name)
        cur = conn.cursor()
        query = """
        SELECT airport_name, city FROM destinations 
        WHERE destination_id = ?
        """
        cur.execute(query, (destination_id,))
        result = cur.fetchone()
        conn.close()
        return result if result else None
    
    def validate_destination_input(self, usr_input):
        dest_id = self.find_destination_by_city_or_iata(usr_input)
        print(dest_id)
        if dest_id is None:
            print("Destination not found in destinations table.")
            return None
        
        result = self.airport_name_and_city_by_id(dest_id)   #This check is done to make sure the user has entered a their expected and a valid city or IATA code that exists in the destinations table.
        airport_info = f"{result[0]}, {result[1]}" if result else "Unknown"
        
        if airport_info == "Unknown":
            print("Origin not found in destinations table.")
            return None 
        
        response=input("Did you mean: " + airport_info + "? Type Yes or No: ")
        if response.lower() != "yes":
                print("Please try again with a different city or IATA code. or check the destinations table for valid entries.")
                return None
        return dest_id
    
    def status_menu_options(self):
        print("Flight Status Options:")
        print("1. On Time")
        print("2. Delayed")
        print("3. Cancelled")
        status_choice = input("Enter the number corresponding to the flight status: ")
        status_mapping = {
            "1": "On Time",
            "2": "Delayed",
            "3": "Cancelled"
        }
        return status_mapping.get(status_choice, None)

    def create_input_flight_data(self):
        flight = FlightInfo()
       
        flight.set_flight_number(input("Enter Flight Number: e.g. BB123 for Bonobo Airlines flight 123: "))

        flight.set_flight_origin(int(self.validate_destination_input(input("Enter Flight Origin (City or IATA code): "))))
        
        flight.set_flight_destination(int(self.validate_destination_input(input("Enter Flight Destination (City or IATA code): "))))
        
        flight.set_flight_status(self.status_menu_options())

        self.repo.insert_flight_data(flight)
        print("\n" + "Operation Complete. Returning to main menu...")
