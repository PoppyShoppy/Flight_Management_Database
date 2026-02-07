import sqlite3
from SCHEMA import SCHEMA_SQL
# Define DBOperation class to manage all data into the database.
# Give a name of your choice to the database


class DBOperations:
  sql_create_table_firsttime = SCHEMA_SQL

  sql_create_table = "create table TableName"
  sql_insert = "INSERT INTO flights (flight_number, flight_duration, Status, flightOrigin, flightDestination) VALUES (?, ?, ?, ?, ?)"
  sql_insert_destination = "INSERT INTO destinations (airport_iata_code, airport_name, city, country) VALUES (?, ?, ?, ?)"
  sql_insert_pilot = "INSERT INTO pilots (employee_id, first_name, last_name, contact_number, license_number, pilot_rank) VALUES (?, ?, ?, ?, ?, ?)"
  sql_insert_flight_crew = "INSERT INTO flight_crew (flight_id, pilot_id, role, is_flying_pilot) VALUES (?, ?, ?, ?)"
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
    try:
      self.conn = sqlite3.connect("DBName.db")
      self.cur = self.conn.cursor()
      self.cur.executescript(self.sql_create_table_firsttime)
      self.conn.commit()
      print("Database and tables initiated successfullly.")
    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  def get_connection(self):
    self.conn = sqlite3.connect("DBName.db")
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

  def find_destination_by_city_or_iata(self, city_or_iata):
    """Look up destination_id by city name or IATA code"""
    conn = sqlite3.connect("DBName.db")
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
    conn = sqlite3.connect("DBName.db")
    cur = conn.cursor()
    query = """
    SELECT airport_name, city FROM destinations 
    WHERE destination_id = ?
    """
    cur.execute(query, (destination_id,))
    result = cur.fetchone()
    conn.close()
    return result if result else None

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

  def insert_data(self):
    try:
      self.get_connection()

      flight = FlightInfo()
      #flight.set_flight_id(int(input("Enter FlightID: ")))  
      
      flight.set_flight_number(input("Enter Flight Number: e.g. BB123 for Bonobo Airlines flight 123: "))

      ### ENTER FLIGHT ORIGIN SECTION
      origin = input("Enter Flight Origin (City or IATA code): ")
      origin_id = self.find_destination_by_city_or_iata(origin)

      if origin_id is None:
        print("Origin not found in destinations table.")
        return 
      
      result = self.airport_name_and_city_by_id(origin_id)
      airport_info = f"{result[0]}, {result[1]}" if result else "Unknown"
      response=input("Did you mean: " + airport_info + "? Type Yes or No: ")

      if response.lower() != "yes":
        print("Please try again with a different city or IATA code. or check the destinations table for valid entries.")
        return
      
      flight.set_flight_origin(origin_id)
      
      ### ENTER FLIGHT DESTINATION SECTION
      destination = input("Enter Flight Destination (City or IATA code): ")
      destination_id = self.find_destination_by_city_or_iata(destination)

      if destination_id is None:
        print("Destination not found in destinations table.")
        return  
      
      result = self.airport_name_and_city_by_id(destination_id) 
      airport_info = f"{result[0]}, {result[1]}" if result else "Unknown" 
      response=input("Did you mean: " + airport_info + "? Type Yes or No: ")

      if response.lower() != "yes": 
       print("Please try again with a different city or IATA code. or check the destinations table for valid entries.")
       return
      
      flight.set_flight_destination(destination_id)

      flight.set_flight_status(input("Enter Flight Status: i.e. On Time, Delayed, Cancelled: "))

      self.cur.execute(self.sql_insert, (flight.flight_number, flight.flight_duration, flight.status, flight.flight_origin, flight.flight_destination))
      
      self.conn.commit()
      print("Inserted data successfully")
    except Exception as e:
      print(e)
    finally:
      self.conn.close()

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
        exit(0)
      else:
        print("Invalid Choice")

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


class FlightInfo:

  def __init__(self):
    self.flightID = 0
    self.flightOrigin = ''
    self.flightDestination = ''
    self.status = ''

  def set_flight_id(self, flightID):
    self.flightID = flightID

  def set_flight_number(self, flight_number):
    self.flight_number = flight_number
  def set_flight_duration(self, flight_duration):
    self.flight_duration = flight_duration

  def set_flight_status(self, status):
    self.status = status

  def set_flight_origin(self, flightOrigin):
    self.flight_origin = flightOrigin

  def set_flight_destination(self, flightDestination):
    self.flight_destination = flightDestination

  def get_flight_id(self):
    return self.flightID
  
  def get_flight_number(self):
    return self.flight_number 
  

  def get_flight_origin(self):
    return self.flightOrigin

  def get_flight_destination(self):
    return self.flightDestination

  def get_status(self):
    return self.status

  def __str__(self):
    return (str(self.flight_number) + "\n" + str(self.status) + "\n" +
            str(getattr(self, 'flight_origin', '')) + "\n" + str(getattr(self, 'flight_destination', '')))


# The main function will parse arguments.
# These argument will be definded by the users on the console.
# The user will select a choice from the menu to interact with the database.

while True:
  print("\n Menu:")
  print("**********")
  print(" 1. Create table FlightInfo")
  print(" 2. Insert data into FlightInfo")
  print(" 3. Select all data from FlightInfo")
  print(" 4. Search a flight")
  print(" 5. Update data some records")
  print(" 6. Delete data some records")
  print(" 7. Exit\n")

  __choose_menu = int(input("Enter your choice: "))
  db_ops = DBOperations()
  if __choose_menu == 1:
    db_ops.create_table()
  elif __choose_menu == 2:
    db_ops.insert_data()
  elif __choose_menu == 3:
    db_ops.select_all()
  elif __choose_menu == 4:
    db_ops.search_data()
  elif __choose_menu == 5:
    db_ops.update_data()
  elif __choose_menu == 6:
    db_ops.delete_data()
  elif __choose_menu == 7:
    exit(0)
  else:
    print("Invalid Choice")
