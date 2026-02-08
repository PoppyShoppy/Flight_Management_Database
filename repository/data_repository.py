import sqlite3
from db import DBConnection

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
      conn = DBConnection.get_connection()
      cur = conn.cursor()
      # keeping this in just in case
      self.conn = conn
      self.cur = cur
      return conn, cur

  def create_table(self):
    """Create all necessary tables for the flight management system."""
    try:
      self.get_connection()
      
      # Create destinations table
      self.cur.execute("""
        CREATE TABLE IF NOT EXISTS destinations (
          destination_id INTEGER PRIMARY KEY AUTOINCREMENT,
          airport_iata_code TEXT UNIQUE NOT NULL,
          airport_name TEXT NOT NULL,
          city TEXT NOT NULL,
          country TEXT NOT NULL
        )
      """)
      
      # Create pilots table
      self.cur.execute("""
        CREATE TABLE IF NOT EXISTS pilots (
          pilot_id INTEGER PRIMARY KEY AUTOINCREMENT,
          employee_id TEXT UNIQUE NOT NULL,
          first_name TEXT NOT NULL,
          last_name TEXT NOT NULL,
          contact_number TEXT,
          license_number TEXT UNIQUE NOT NULL,
          pilot_rank TEXT NOT NULL
        )
      """)
      
      # Create flights table
      self.cur.execute("""
        CREATE TABLE IF NOT EXISTS flights (
          flight_id INTEGER PRIMARY KEY AUTOINCREMENT,
          flight_number TEXT UNIQUE NOT NULL,
          Status TEXT NOT NULL,
          flightOrigin INTEGER NOT NULL,
          flightDestination INTEGER NOT NULL,
          FOREIGN KEY (flightOrigin) REFERENCES destinations(destination_id),
          FOREIGN KEY (flightDestination) REFERENCES destinations(destination_id)
        )
      """)
      
      # Create flight_crew table
      self.cur.execute("""
        CREATE TABLE IF NOT EXISTS flight_crew (
          flight_crew_id INTEGER PRIMARY KEY AUTOINCREMENT,
          flight_id INTEGER NOT NULL,
          pilot_id INTEGER NOT NULL,
          role TEXT NOT NULL,
          is_flying_pilot BOOLEAN NOT NULL DEFAULT 0,
          FOREIGN KEY (flight_id) REFERENCES flights(flight_id),
          FOREIGN KEY (pilot_id) REFERENCES pilots(pilot_id)
        )
      """)
      
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

  # --- Read-only / helper methods used by input layers ---
  def list_destinations(self):
    ###Return list of destinations (rows) limited to `limit`.###
    try:
      conn = DBConnection.get_connection()
      cur = conn.cursor()
      cur.execute("SELECT destination_id, airport_iata_code, airport_name, city, country FROM destinations")
      results = cur.fetchall()
      return results
    finally:
      try:
        conn.close()
      except Exception:
        pass

  def find_destination_by_city_or_iata(self, city_or_iata):
    ###Return destination_id matching city LIKE or exact IATA (case-insensitive), or None.###
    try:
      conn = DBConnection.get_connection()
      cur = conn.cursor()
      query = """
      SELECT destination_id FROM destinations
      WHERE city LIKE ? OR airport_iata_code = ?
      """
      cur.execute(query, (f"%{city_or_iata}%", city_or_iata.upper()))
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
      cur.execute("SELECT airport_name, city FROM destinations WHERE destination_id = ?", (destination_id,))
      row = cur.fetchone()
      return (row[0], row[1]) if row else None
    finally:
      try:
        conn.close()
      except Exception:
        pass

  def list_pilots(self, limit=10):
    ###Return list of pilots limited to `limit`.###
    try:
      conn = DBConnection.get_connection()
      cur = conn.cursor()
      cur.execute("SELECT pilot_id, employee_id, first_name, last_name, pilot_rank FROM pilots LIMIT ?", (limit,))
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
      cur.execute(
        """
        SELECT flights.FlightID, flights.flight_number, d1.airport_iata_code AS origin, d2.airport_iata_code AS destination, flights.Status
        FROM flights
        JOIN destinations d1 ON flights.flightOrigin = d1.destination_id
        JOIN destinations d2 ON flights.flightDestination = d2.destination_id
        """
      )
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
      cur.execute("SELECT 1 FROM flights WHERE flight_id = ?", (flight_id,))
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
      cur.execute("SELECT 1 FROM pilots WHERE pilot_id = ?", (pilot_id,))
      return cur.fetchone() is not None
    finally:
      try:
        conn.close()
      except Exception:
        pass




