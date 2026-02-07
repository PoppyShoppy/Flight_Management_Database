import sqlite3
from SCHEMA import SCHEMA_SQL 
from db_connection import DBConnection

class DatabaseInitialiser: 
   #Create database and tables if they dont exist, also inserts example rows so you can use it straight out the box
   @staticmethod #using static method so i can call this method without creating an instance of the class, as I only want to run this once to set up the database and tables, and I dont need to store any state in the class.
   def initialise():
    try:
      conn = sqlite3.connect(DBConnection.DB_NAME)
      cur = conn.cursor()
      cur.executescript(SCHEMA_SQL)
      conn.commit()
      print("\n" + "Database and tables initiated successfullly.")
    except Exception as e:
      print(e)
    finally:
      conn.close()