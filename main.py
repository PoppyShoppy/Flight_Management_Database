from db import DBConnection
from db.db_init import DatabaseInitialiser
from repository import DBOperations
from viewer import DataViewer, StatisticsViewer
from services import FlightInputService, DestinationInputService, PilotInputService, CrewInputService
    
DatabaseInitialiser.initialise()

db_ops = DBOperations()
db_viewer = DataViewer()
stats_viewer = StatisticsViewer()

# The main function will parse arguments.
# These argument will be definded by the users on the console.
# The user will select a choice from the menu to interact with the database.

while True:
  print("\n Menu:")
  print("**********")
  print(" 1. Create table FlightInfo")
  print(" 2. Insert data into Database")
  print(" 3. Select and view all data from Database")
  print(" 4. Search records in Database")
  print(" 5. Update data some records")
  print(" 6. Delete data some records")
  print(" 7. View Statistics and Reports")
  print(" 8. Exit\n")

  try:
    __choose_menu = int(input("Enter your choice: "))
  except ValueError:
    print("Please enter a valid number between 1 and 8.")
    continue
  if __choose_menu == 1:
    db_ops.create_table()
  elif __choose_menu == 2:
    try:
      insert_choice = int(input("\nWhat would you like to insert?\n1. Flight\n2. Destination\n3. Pilot\n4. Flight Crew\n5. Back to Menu\nEnter your choice: "))
      if insert_choice == 1:
        flight_input = FlightInputService(db_ops)
        flight_input.create_input_flight_data()
      elif insert_choice == 2:
        dest_input = DestinationInputService(db_ops)
        dest_input.create_input_destination_data()
      elif insert_choice == 3:
        pilot_input = PilotInputService(db_ops)
        pilot_input.create_input_pilot_data()
      elif insert_choice == 4:
        crew_input = CrewInputService(db_ops)
        crew_input.create_input_flight_crew_data()
      elif insert_choice == 5:
        pass
      else:
        print("Invalid Choice")
    except ValueError:
      print("Please enter a valid number")

  elif __choose_menu == 3:
    db_viewer.select_all()
  elif __choose_menu == 4:
    db_viewer.search_data()
  elif __choose_menu == 5:
    db_viewer.update_data()
  elif __choose_menu == 6:
    db_viewer.delete_data()
  elif __choose_menu == 7:
    stats_viewer.view_statistics_menu()
  elif __choose_menu == 8:
    exit(0)
  else:
    print("Invalid Choice")
