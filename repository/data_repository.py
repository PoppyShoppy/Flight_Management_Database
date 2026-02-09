import sqlite3
from db import DBConnection

class DBOperations:

  ###### JUST RIGHT CLICK on the sql variable and click "Go to definition" to see where it's used. ######
  # I tried to keep just one method per CRRUD operation but for some operations like INSERT, I needed to take in multiple arguments unique to the table.

  # ==================== INSERT STATEMENTS ===========================================================================
  sql_insert_flights = "INSERT INTO flights (flight_number, scheduled_departure, Status, flightOrigin, flightDestination) VALUES (?, ?, ?, ?, ?)"
  sql_insert_destination = "INSERT INTO destinations (airport_iata_code, airport_name, city, country) VALUES (?, ?, ?, ?)"
  sql_insert_pilot = "INSERT INTO pilots (employee_id, first_name, last_name, contact_number, license_number, pilot_rank) VALUES (?, ?, ?, ?, ?, ?)"
  sql_insert_flight_crew = "INSERT INTO flight_crew (flight_id, pilot_id, role, is_flying_pilot) VALUES (?, ?, ?, ?)"
  
  # ==================== SELECT STATEMENTS ========================================================================================================================
  # Note: Aliases d1/d2/f used to avoid confusion when referencing same table twice
  sql_select_all_flights = "SELECT f.flight_number, d1.airport_iata_code AS Origin, d2.airport_iata_code AS Destination, f.Status FROM flights f " \
  "JOIN destinations d1 ON f.flightOrigin = d1.destination_id JOIN destinations d2 ON f.flightDestination = d2.destination_id;"
  
  sql_select_all_destinations = "SELECT destination_id, airport_iata_code, airport_name, city, country FROM destinations"
  sql_select_all_pilots = "SELECT pilot_id, employee_id, first_name, last_name, pilot_rank FROM pilots"
  sql_select_all_flight_crew = "SELECT flight_crew_id, flight_id, pilot_id, role, is_flying_pilot FROM flight_crew"
  
  # Helper SELECT queries for lookups and validation ===========================================================================================================================
  sql_list_destinations = "SELECT destination_id, airport_iata_code, airport_name, city, country FROM destinations"
  sql_find_destination_by_city_or_iata = "SELECT destination_id FROM destinations WHERE city LIKE ? OR airport_iata_code = ?"
  sql_get_airport_info = "SELECT airport_name, city FROM destinations WHERE destination_id = ?"
  sql_list_pilots = "SELECT pilot_id, employee_id, first_name, last_name, pilot_rank FROM pilots"
  sql_list_flights = "SELECT flights.FlightID, flights.flight_number, d1.airport_iata_code AS origin, d2.airport_iata_code AS destination, flights.Status FROM flights " \
  "JOIN destinations d1 ON flights.flightOrigin = d1.destination_id JOIN destinations d2 ON flights.flightDestination = d2.destination_id"
  
  sql_validate_flight_exists = "SELECT 1 FROM flights WHERE FlightID = ?"
  sql_validate_pilot_exists = "SELECT 1 FROM pilots WHERE pilot_id = ?"
  
  # Search queries ==================================================================================================================================================================
  sql_search_flight_by_id = "SELECT FlightID, flight_number, Status, flightOrigin, flightDestination FROM flights WHERE FlightID = ?"
  sql_search_destinations = "SELECT destination_id, airport_iata_code, airport_name, city, country FROM destinations WHERE city LIKE ? OR airport_iata_code LIKE ?"
  sql_search_pilots = "SELECT pilot_id, employee_id, first_name, last_name, contact_number, license_number, pilot_rank FROM pilots WHERE first_name LIKE ? OR last_name LIKE ? OR employee_id LIKE ?"
  sql_search_flight_crew = "SELECT flight_crew_id, flight_id, pilot_id, role, is_flying_pilot FROM flight_crew WHERE flight_id = ?"
  
  # UPDATE queries ==================================================================================================================================================================
  sql_update_flight_number = "UPDATE flights SET flight_number = ? WHERE FlightID = ?"
  sql_update_flight_status = "UPDATE flights SET Status = ? WHERE FlightID = ?"
  sql_update_flight_origin = "UPDATE flights SET flightOrigin = ? WHERE FlightID = ?"
  sql_update_flight_destination = "UPDATE flights SET flightDestination = ? WHERE FlightID = ?"
  sql_update_destination_iata = "UPDATE destinations SET airport_iata_code = ? WHERE destination_id = ?"
  sql_update_destination_name = "UPDATE destinations SET airport_name = ? WHERE destination_id = ?"
  sql_update_destination_city = "UPDATE destinations SET city = ? WHERE destination_id = ?"
  sql_update_destination_country = "UPDATE destinations SET country = ? WHERE destination_id = ?"
  sql_update_pilot_employee_id = "UPDATE pilots SET employee_id = ? WHERE pilot_id = ?"
  sql_update_pilot_first_name = "UPDATE pilots SET first_name = ? WHERE pilot_id = ?"
  sql_update_pilot_last_name = "UPDATE pilots SET last_name = ? WHERE pilot_id = ?"
  sql_update_pilot_contact = "UPDATE pilots SET contact_number = ? WHERE pilot_id = ?"
  sql_update_pilot_license = "UPDATE pilots SET license_number = ? WHERE pilot_id = ?"
  sql_update_pilot_rank = "UPDATE pilots SET pilot_rank = ? WHERE pilot_id = ?"
  sql_update_crew_role = "UPDATE flight_crew SET role = ? WHERE flight_crew_id = ?"
  sql_update_crew_flying_pilot = "UPDATE flight_crew SET is_flying_pilot = ? WHERE flight_crew_id = ?"
  
  # DELETE queries
  sql_delete_flight = "DELETE FROM flights WHERE FlightID = ?"
  sql_delete_destination = "DELETE FROM destinations WHERE destination_id = ?"
  sql_delete_pilot = "DELETE FROM pilots WHERE pilot_id = ?"
  sql_delete_flight_crew = "DELETE FROM flight_crew WHERE flight_crew_id = ?"
  
  # Existence check queries
  sql_check_flight_exists = "SELECT * FROM flights WHERE FlightID = ?"
  sql_check_destination_exists = "SELECT * FROM destinations WHERE destination_id = ?"
  sql_check_pilot_exists = "SELECT * FROM pilots WHERE pilot_id = ?"
  sql_check_crew_exists = "SELECT * FROM flight_crew WHERE flight_crew_id = ?"
  
  # CREATE TABLE STATEMENTS, thinking of deleting because they are only used once at execution and already covered by the init_db file it did help me quickly look up table structure though. 
  sql_create_destinations = """CREATE TABLE IF NOT EXISTS destinations (
    destination_id INTEGER PRIMARY KEY AUTOINCREMENT,
    airport_iata_code VARCHAR(3) UNIQUE NOT NULL,
    airport_name VARCHAR(100),
    city VARCHAR(50),
    country VARCHAR(50)
  )"""
  sql_create_pilots = """CREATE TABLE IF NOT EXISTS pilots (
    pilot_id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id VARCHAR(20) UNIQUE NOT NULL,
    first_name VARCHAR(30),
    last_name VARCHAR(30),
    contact_number VARCHAR(20),
    license_number VARCHAR(15),
    pilot_rank VARCHAR(20)
  )"""
  sql_create_flights = """CREATE TABLE IF NOT EXISTS flights (
    FlightID INTEGER PRIMARY KEY AUTOINCREMENT,
    flight_number VARCHAR(10) NOT NULL,
    scheduled_departure DATETIME NOT NULL,
    Status VARCHAR(15),
    flightOrigin INTEGER,
    flightDestination INTEGER,
    FOREIGN KEY (flightOrigin) REFERENCES destinations(destination_id),
    FOREIGN KEY (flightDestination) REFERENCES destinations(destination_id)
  )"""
  sql_create_flight_crew = """CREATE TABLE IF NOT EXISTS flight_crew (
    flight_crew_id INTEGER PRIMARY KEY AUTOINCREMENT,
    flight_id INTEGER NOT NULL,
    pilot_id INTEGER NOT NULL,
    role VARCHAR(20) NOT NULL,
    is_flying_pilot BOOLEAN DEFAULT 0,
    FOREIGN KEY (flight_id) REFERENCES flights(FlightID),
    FOREIGN KEY (pilot_id) REFERENCES pilots(pilot_id),
    UNIQUE(flight_id, pilot_id)
  )"""
  
  sql_search = "select * from TableName where FlightID = ?"
  sql_alter_data = ""
  sql_update_data = ""
  sql_delete_data = ""
  sql_drop_table = ""

  def __init__(self):
    self.db_name = DBConnection.DB_NAME

  def get_connection(self):
      conn = DBConnection.get_connection()
      cur = conn.cursor()
      # keeping this in just in case
      self.conn = conn
      self.cur = cur
      return conn, cur

  # ==================== GENERIC HELPER METHODS ====================
  
  def _execute_query(self, query, params):
    """Generic method to execute a query and commit."""
    try:
      conn = DBConnection.get_connection()
      cur = conn.cursor()
      cur.execute(query, params)
      conn.commit()
      return True
    finally:
      try:
        conn.close()
      except Exception:
        pass

  def _fetch_query(self, query, params):
    """Generic method to execute a query and fetch results."""
    try:
      conn = DBConnection.get_connection()
      cur = conn.cursor()
      cur.execute(query, params)
      return cur.fetchall()
    finally:
      try:
        conn.close()
      except Exception:
        pass

  def _fetch_one(self, query, params):
    """Generic method to execute a query and fetch one result."""
    try:
      conn = DBConnection.get_connection()
      cur = conn.cursor()
      cur.execute(query, params)
      return cur.fetchone() is not None
    finally:
      try:
        conn.close()
      except Exception:
        pass

  def create_table(self):
    """Create all necessary tables for the flight management system."""
    try:
      self.get_connection()
      
      # Create destinations table
      self.cur.execute(self.sql_create_destinations)
      
      # Create pilots table
      self.cur.execute(self.sql_create_pilots)
      
      # Create flights table
      self.cur.execute(self.sql_create_flights)
      
      # Create flight_crew table
      self.cur.execute(self.sql_create_flight_crew)
      
      self.conn.commit()
      print("All tables created successfully!")
      
    except Exception as e:
      print("Error creating tables: " + str(e))
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
          flight.get_scheduled_departure(),
          flight.get_status(),
          flight.get_flight_origin(),
          flight.get_flight_destination()
        )
      )     
      self.conn.commit()
      return self.cur.lastrowid
    except Exception:
      raise
    finally:
      self.conn.close()

  def insert_destination_data(self, iata, name, city, country):
    ###Insert destination with provided data###
    try:
      self.get_connection()
      self.cur.execute(self.sql_insert_destination, (iata, name, city, country))
      self.conn.commit()
      return self.cur.lastrowid
    except Exception:
      raise
    finally:
      self.conn.close()

  def insert_pilot_data(self, emp_id, first, last, contact, license, rank):
    ###Insert pilot with provided data###
    try:
      self.get_connection()
      self.cur.execute(self.sql_insert_pilot, (emp_id, first, last, contact, license, rank))
      self.conn.commit()
      return self.cur.lastrowid
    except Exception:
      raise
    finally:
      self.conn.close()

  def insert_flight_crew_data(self, flight_id, pilot_id, role, is_flying):
    ###Insert flight crew with provided data###
    try:
      self.get_connection()
      self.cur.execute(self.sql_insert_flight_crew, (flight_id, pilot_id, role, int(is_flying)))
      self.conn.commit()
      return self.cur.lastrowid
    except Exception:
      raise
    finally:
      self.conn.close()

  ##############################################################################################################################################
  ##############################################################################################################################################
  ##############################################################################################################################################
  # --- Read-only / helper methods used by input layers --- ####################################################################################
  def list_destinations(self):
    ###Return list of destinations.###
    try:
      conn = DBConnection.get_connection()
      cur = conn.cursor()
      cur.execute(self.sql_list_destinations)
      results = cur.fetchall()
      return results
    finally:
      try:
        conn.close()
      except Exception:
        pass

  def find_destination_id_by_city_or_iata(self, city_or_iata):
    ###Return destination_id matching city LIKE or exact IATA also case-insensitive###
    try:
      conn = DBConnection.get_connection()
      cur = conn.cursor()
      cur.execute(self.sql_find_destination_by_city_or_iata, (f"%{city_or_iata}%", city_or_iata.upper()))
      row = cur.fetchone()
      return row[0] if row else None
    finally:
      try:
        conn.close()
      except Exception:
        pass

  def get_airport_info_by_id(self, destination_id):
    ###Return (airport_name, city) or None.###
    try:
      conn = DBConnection.get_connection()
      cur = conn.cursor()
      cur.execute(self.sql_get_airport_info, (destination_id,))
      row = cur.fetchone()
      return (row[0], row[1]) if row else None
    finally:
      try:
        conn.close()
      except Exception:
        pass

  def list_pilots(self):
    ###Return list of pilots ###
    try:
      conn = DBConnection.get_connection()
      cur = conn.cursor()
      cur.execute(self.sql_list_pilots)
      return cur.fetchall()
    finally:
      try:
        conn.close()
      except Exception:
        pass

  def list_flights(self):
    ###Return a list of flights with origin/destination IATA codes for display.###
    try:
      conn = DBConnection.get_connection()
      cur = conn.cursor()
      cur.execute(self.sql_list_flights)
      return cur.fetchall()
    finally:
      try:
        conn.close()
      except Exception:
        pass

  def validate_flight_exists(self, flight_id):
    try:
      conn = DBConnection.get_connection()
      cur = conn.cursor()
      cur.execute(self.sql_validate_flight_exists, (flight_id,))
      return cur.fetchone() is not None
    finally:
      try:
        conn.close()
      except Exception:
        pass

  def validate_pilot_exists(self, pilot_id):
    try:
      conn = DBConnection.get_connection()
      cur = conn.cursor()
      cur.execute(self.sql_validate_pilot_exists, (pilot_id,))
      return cur.fetchone() is not None
    finally:
      try:
        conn.close()
      except Exception:
        pass

  def search_flight_by_id(self, flight_id):
    """Search for a single flight by ID."""
    try:
      conn = DBConnection.get_connection()
      cur = conn.cursor()
      cur.execute(self.sql_search_flight_by_id, (flight_id,))
      return cur.fetchall()
    finally:
      try:
        conn.close()
      except Exception:
        pass

  def search_destinations(self, search_term):
    """Search destinations by city or IATA code."""
    try:
      conn = DBConnection.get_connection()
      cur = conn.cursor()
      cur.execute(self.sql_search_destinations, (f"%{search_term}%", f"%{search_term}%"))
      return cur.fetchall()
    finally:
      try:
        conn.close()
      except Exception:
        pass

  def search_pilots(self, search_term):
    """Search pilots by name or employee ID."""
    try:
      conn = DBConnection.get_connection()
      cur = conn.cursor()
      cur.execute(self.sql_search_pilots, (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
      return cur.fetchall()
    finally:
      try:
        conn.close()
      except Exception:
        pass

  def search_flight_crew(self, flight_id):
    """Search flight crew by flight ID."""
    try:
      conn = DBConnection.get_connection()
      cur = conn.cursor()
      cur.execute(self.sql_search_flight_crew, (flight_id,))
      return cur.fetchall()
    finally:
      try:
        conn.close()
      except Exception:
        pass

  # ==================== UPDATE METHODS ====================
  
  def update_flight_number(self, flight_id, new_value):
    """Update flight number."""
    return self._execute_query(self.sql_update_flight_number, (new_value, flight_id))

  def update_flight_status(self, flight_id, new_value):
    """Update flight status."""
    return self._execute_query(self.sql_update_flight_status, (new_value, flight_id))

  def update_flight_origin(self, flight_id, new_value):
    """Update flight origin."""
    return self._execute_query(self.sql_update_flight_origin, (new_value, flight_id))

  def update_flight_destination(self, flight_id, new_value):
    """Update flight destination."""
    return self._execute_query(self.sql_update_flight_destination, (new_value, flight_id))

  def update_destination_iata(self, dest_id, new_value):
    """Update destination IATA code."""
    return self._execute_query(self.sql_update_destination_iata, (new_value, dest_id))

  def update_destination_name(self, dest_id, new_value):
    """Update destination airport name."""
    return self._execute_query(self.sql_update_destination_name, (new_value, dest_id))

  def update_destination_city(self, dest_id, new_value):
    """Update destination city."""
    return self._execute_query(self.sql_update_destination_city, (new_value, dest_id))

  def update_destination_country(self, dest_id, new_value):
    """Update destination country."""
    return self._execute_query(self.sql_update_destination_country, (new_value, dest_id))

  def update_pilot_employee_id(self, pilot_id, new_value):
    """Update pilot employee ID."""
    return self._execute_query(self.sql_update_pilot_employee_id, (new_value, pilot_id))

  def update_pilot_first_name(self, pilot_id, new_value):
    """Update pilot first name."""
    return self._execute_query(self.sql_update_pilot_first_name, (new_value, pilot_id))

  def update_pilot_last_name(self, pilot_id, new_value):
    """Update pilot last name."""
    return self._execute_query(self.sql_update_pilot_last_name, (new_value, pilot_id))

  def update_pilot_contact(self, pilot_id, new_value):
    """Update pilot contact number."""
    return self._execute_query(self.sql_update_pilot_contact, (new_value, pilot_id))

  def update_pilot_license(self, pilot_id, new_value):
    """Update pilot license number."""
    return self._execute_query(self.sql_update_pilot_license, (new_value, pilot_id))

  def update_pilot_rank(self, pilot_id, new_value):
    """Update pilot rank."""
    return self._execute_query(self.sql_update_pilot_rank, (new_value, pilot_id))

  def update_crew_role(self, crew_id, new_value):
    """Update flight crew role."""
    return self._execute_query(self.sql_update_crew_role, (new_value, crew_id))

  def update_crew_flying_pilot(self, crew_id, new_value):
    """Update flight crew flying pilot status."""
    return self._execute_query(self.sql_update_crew_flying_pilot, (new_value, crew_id))

  # ==================== DELETE METHODS ====================
  
  def delete_flight(self, flight_id):
    """Delete a flight by ID."""
    return self._execute_query(self.sql_delete_flight, (flight_id,))

  def delete_destination(self, dest_id):
    """Delete a destination by ID."""
    return self._execute_query(self.sql_delete_destination, (dest_id,))

  def delete_pilot(self, pilot_id):
    """Delete a pilot by ID."""
    return self._execute_query(self.sql_delete_pilot, (pilot_id,))

  def delete_flight_crew(self, crew_id):
    """Delete a flight crew record by ID."""
    return self._execute_query(self.sql_delete_flight_crew, (crew_id,))

  # ==================== EXISTENCE CHECK METHODS ====================
  
  def flight_exists(self, flight_id):
    """Check if a flight exists."""
    return self._fetch_one(self.sql_check_flight_exists, (flight_id,))

  def destination_exists(self, dest_id):
    """Check if a destination exists."""
    return self._fetch_one(self.sql_check_destination_exists, (dest_id,))

  def pilot_exists(self, pilot_id):
    """Check if a pilot exists."""
    return self._fetch_one(self.sql_check_pilot_exists, (pilot_id,))

  def crew_exists(self, crew_id):
    """Check if a flight crew record exists."""
    return self._fetch_one(self.sql_check_crew_exists, (crew_id,))




