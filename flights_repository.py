import sqlite3
from db_connection import DBConnection

class DBOperations:
  sql_create_table = "create table TableName"
  sql_insert_flights = "INSERT INTO flights (flight_number, Status, flightOrigin, flightDestination) VALUES (?, ?, ?, ?)"
  sql_insert_destination = "INSERT INTO destinations (airport_iata_code, airport_name, city, country) VALUES (?, ?, ?, ?)"
  sql_insert_pilot = "INSERT INTO pilots (employee_id, first_name, last_name, contact_number, license_number, pilot_rank) VALUES (?, ?, ?, ?, ?, ?)"
  sql_insert_flight_crew = "INSERT INTO flight_crew (flight_id, pilot_id, role, is_flying_pilot) VALUES (?, ?, ?, ?)"
  
  #because I am referencing the content of the destination table twice in a single query (for flight origin and destination), I had to use dot notation/aliases d1/d2/f to specify that the correct columns are pulled in the select statement to avoid confusion  
  sql_select_all_flights = "SELECT f.flight_number, d1.airport_iata_code AS Origin, d2.airport_iata_code AS Destination, f.Status FROM flights f JOIN destinations d1 ON f.flightOrigin = d1.destination_id JOIN destinations d2 ON f.flightDestination = d2.destination_id;"
  sql_select_all_destinations = "select * from destinations" 
  sql_select_all_pilots = "select * from pilots"
  sql_select_all_flight_crew = "select * from flight_crew" 
  sql_search = "select * from TableName where FlightID = ?"
  sql_alter_data = ""
  sql_update_data = ""
  sql_delete_data = ""
  sql_drop_table = ""

  def __init__(self):
    self.db_name = DBConnection.DB_NAME

  def get_connection(self):
      self.conn = DBConnection.get_connection()
      self.cur = self.conn.cursor()

  def create_table(self):
    try:
      self.get_connection()
      self.cur.execute(self.sql_create_table)
      self.conn.commit()
      print("Table created successfully")
    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  def insert_destination(self):
    try:
      self.get_connection()
      iata = input("Enter airport IATA code (e.g. JFK): ").upper()
      name = input("Enter airport name: ")
      city = input("Enter city: ")
      country = input("Enter country: ")
      self.cur.execute(self.sql_insert_destination, (iata, name, city, country))
      self.conn.commit()
      print("Inserted destination id:", self.cur.lastrowid)
    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  def insert_pilot(self):
    try:
      self.get_connection()
      emp = input("Enter employee id: e.g. EMP001")
      first = input("Enter first name: ")
      last = input("Enter last name: ")
      contact = input("Enter contact number: ")
      license = input("Enter license number: ")
      rank = input("Enter pilot rank (e.g. Captain): ")
      self.cur.execute(self.sql_insert_pilot, (emp, first, last, contact, license, rank))
      self.conn.commit()
      print("Inserted pilot id:", self.cur.lastrowid)
    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  def insert_flight_crew(self):
    try:
      self.get_connection()
      flight_id = int(input("Enter FlightID: "))
      # validate flight exists
      self.cur.execute("SELECT 1 FROM flights WHERE FlightID = ?", (flight_id,))
      if not self.cur.fetchone():
        print("Flight not found")
        return
      pilot_id = int(input("Enter PilotID: "))
      self.cur.execute("SELECT 1 FROM pilots WHERE pilot_id = ?", (pilot_id,))
      if not self.cur.fetchone():
        print("Pilot not found")
        return
      role = input("Enter role (Captain/First Officer): ")
      is_flying = input("Is flying pilot? (yes/no): ").lower() in ("y", "yes")
      self.cur.execute(self.sql_insert_flight_crew, (flight_id, pilot_id, role, int(is_flying)))
      self.conn.commit()
      print("Inserted flight_crew id:", self.cur.lastrowid)
    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  def insert_flight_data(self, flight):
    try:
      self.get_connection()

      self.cur.execute(
        self.sql_insert_flights, 
        (
          flight.get_flight_number(),
          flight.get_status(),
          flight.get_flight_origin(),
          flight.get_flight_destination()
        )
      )     
      self.conn.commit()
      print("\n" + "Data inserted successfully with FlightID:", self.cur.lastrowid)
    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  def insert_destination_data(self, iata, name, city, country):
    """Insert destination with provided data"""
    try:
      self.get_connection()
      self.cur.execute(self.sql_insert_destination, (iata, name, city, country))
      self.conn.commit()
      print("Inserted destination id:", self.cur.lastrowid)
    except Exception as e:
      print(f"Error inserting destination: {e}")
    finally:
      self.conn.close()

  def insert_pilot_data(self, emp_id, first, last, contact, license, rank):
    """Insert pilot with provided data"""
    try:
      self.get_connection()
      self.cur.execute(self.sql_insert_pilot, (emp_id, first, last, contact, license, rank))
      self.conn.commit()
      print("Inserted pilot id:", self.cur.lastrowid)
    except Exception as e:
      print(f"Error inserting pilot: {e}")
    finally:
      self.conn.close()

  def insert_flight_crew_data(self, flight_id, pilot_id, role, is_flying):
    """Insert flight crew with provided data"""
    try:
      self.get_connection()
      self.cur.execute(self.sql_insert_flight_crew, (flight_id, pilot_id, role, int(is_flying)))
      self.conn.commit()
      print("Inserted flight_crew id:", self.cur.lastrowid)
    except Exception as e:
      print(f"Error inserting flight crew: {e}")
    finally:
      self.conn.close()
  
  
  def insert_data(self):
    """Menu for inserting different types of data"""
    try:
      insert_choice = int(input("\nWhat would you like to insert?\n1. Flight\n2. Destination\n3. Pilot\n4. Flight Crew\n5. Back to Menu\nEnter your choice: "))
      if insert_choice == 1:
        from flight_input_layer import FlightInputLayer
        flight_input = FlightInputLayer(self)
        flight_input.create_input_flight_data()
      elif insert_choice == 2:
        from destination_input_layer import DestinationInputLayer
        dest_input = DestinationInputLayer(self)
        dest_input.create_input_destination_data()
      elif insert_choice == 3:
        from pilot_input_layer import PilotInputLayer
        pilot_input = PilotInputLayer(self)
        pilot_input.create_input_pilot_data()
      elif insert_choice == 4:
        from flight_crew_input_layer import FlightCrewInputLayer
        crew_input = FlightCrewInputLayer(self)
        crew_input.create_input_flight_crew_data()
      elif insert_choice == 5:
        return
      else:
        print("Invalid Choice")
    except ValueError:
      print("Please enter a valid number")
    except Exception as e:
      print(f"Error: {e}")

  
  def select_all(self):
    try:
      select_all_choice=int(input("\nWhat table do you want to select from?" "\n1. Flights" "\n2. Destinations" "\n3. Pilots" "\n4. Flight_crew" "\n5. Exit Menu" "\nEnter your choice: "))
      if select_all_choice == 1:
        self.sql_select_all = self.sql_select_all_flights
      elif select_all_choice == 2:
        self.sql_select_all = self.sql_select_all_destinations
      elif select_all_choice == 3:
        self.sql_select_all = self.sql_select_all_pilots
      elif select_all_choice == 4:
        self.sql_select_all = self.sql_select_all_flight_crew
      elif select_all_choice == 5:
        return
      else:
        print("Invalid Choice")
        return

      self.get_connection()
      self.conn.row_factory = sqlite3.Row
      self.cur = self.conn.cursor()
      self.cur.execute(self.sql_select_all)
      result = self.cur.fetchall()
      
      if not result: 
        print("No records found.")
        return 
            
      print("\n" + "-"*50)
      print(f"\n{' | '.join(result[0].keys())}")
      for row in result:
        print('    |    '.join(str(val) for val in row))
      # think how you could develop this method to show the records

    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  def search_data(self):
    try:
      self.get_connection()
      flightID = int(input("Enter FlightNo: "))
      self.cur.execute(self.sql_search, tuple(str(flightID)))
      result = self.cur.fetchone()
      if type(result) == type(tuple()):
        for index, detail in enumerate(result):
          if index == 0:
            print("Flight ID: " + str(detail))
          elif index == 1:
            print("Flight Origin: " + detail)
          elif index == 2:
            print("Flight Destination: " + detail)
          else:
            print("Status: " + str(detail))
      else:
        print("No Record")

    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  def update_data(self):
    try:
      self.get_connection()

      # Update statement

      if result.rowcount != 0:
        print(str(result.rowcount) + "Row(s) affected.")
      else:
        print("Cannot find this record in the database")

    except Exception as e:
      print(e)
    finally:
      self.conn.close()


# Define Delete_data method to delete data from the table. The user will need to input the flight id to delete the corrosponding record.

  def delete_data(self):
    try:
      self.get_connection()

      if result.rowcount != 0:
        print(str(result.rowcount) + "Row(s) affected.")
      else:
        print("Cannot find this record in the database")

    except Exception as e:
      print(e)
    finally:
      self.conn.close()



# The main function will parse arguments.
# These argument will be definded by the users on the console.
# The user will select a choice from the menu to interact with the database.
