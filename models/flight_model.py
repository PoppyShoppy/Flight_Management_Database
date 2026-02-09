import re
from datetime import datetime

class FlightInfo:

  def __init__(self):
  
    self.flightID = 0
    self.flight_number = ''
    self.flightOrigin = 0
    self.flightDestination = 0
    self.status = ''
    self.scheduled_departure = None

############## SETTERS ##################

  def set_flight_id(self, flightID):
    try:
      #Checks if input is a number. 
      # flightID is automatically generated in the database but in case an event occurs when flightID
      #  is entered this check is there.
      if isinstance(flightID, str): #checks if flightID is a string and converts it to an integer if it is.
          input_val = int(flightID)
      else:
          input_val = flightID
      if input_val > 0: #making sure that flightID is a positive integer number.
        self.flightID = input_val
      else: 
        raise ValueError #a value error is raised if the flightID is not a positive integer number.
    except(ValueError, TypeError): #type error is also there in case the input cannot be converted to an int. 
      raise ValueError("Invalid flight ID. It should be a positive integer number.")

  #flight number is not checked for uniqueness because if another flight to the same destination and schedule is added, 
  # it can have the same flight number.
  def set_flight_number(self, flight_number):
    #reg expression pattern where first two character can be any letter and last three character are digits.
    pattern = r'^[A-Z]{2}\d{3}$' 

    # I am using the .strip() and .upper() methods to remove leading trailing whitespace and make it uppercase 
    # in order to handle lazy typists. 
    flight_number = flight_number.strip().upper() 

    # Using the re.match() function to check if the flight number matches the pattern. 
    if re.match(pattern, flight_number):
        self.flight_number = flight_number
    else:
        raise ValueError("Invalid flight number format. It should be two uppercase letters followed by three digits (e.g., BB123).")
    
    # ensuring that flight status can only be set to allowed values and not "Flying High"
  def set_flight_status(self, status):
      allowed_statuses = ["On Time", "Delayed", "Cancelled"]
      if status not in allowed_statuses:
          raise ValueError(f"Invalid flight status. Allowed values are: {', '.join(allowed_statuses)}.")
      else:
        self.status = status

  def set_flight_origin(self, flightOrigin):
    if isinstance(flightOrigin, str):
        input_val = int(flightOrigin)
    else:
        input_val = flightOrigin

    if input_val > 0:
        self.flightOrigin = input_val
    else: 
        raise ValueError("Invalid flight origin. It should be a positive integer number representing the destination_id in the destinations table.")          

  def set_flight_destination(self, flight_Destination):
    if isinstance(flight_Destination, str):
        input_val = int(flight_Destination)
    else:
        input_val = flight_Destination
        
    if input_val == self.flightOrigin:
        raise ValueError("Flight destination cannot be the same as flight origin.")
    elif input_val <= 0:
        raise ValueError("Invalid flight destination. It should be a positive integer number greater than one representing the destination_id in the destinations table.")
    else:
        self.flightDestination = input_val

  def set_scheduled_departure(self, departure_str):
    try:
        # Simple datetime parser for format YYYY-MM-DD HH:MM
        if isinstance(departure_str, str):
            # Try to parse the datetime string
            dt = datetime.strptime(departure_str.strip(), "%Y-%m-%d %H:%M")
            self.scheduled_departure = dt.strftime("%Y-%m-%d %H:%M")
        else:
            raise ValueError("Scheduled departure must be a string in format YYYY-MM-DD HH:MM")
    except ValueError as e:
        raise ValueError("Invalid date/time format. Please use YYYY-MM-DD HH:MM (e.g., 2026-02-15 14:30)")

############## GETTERS ##################

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

  def get_scheduled_departure(self):
    return self.scheduled_departure

  def __str__(self):
    return ("\n" + str(self.flight_number) + ", " + str(self.status) + ", " +
            str(getattr(self, 'flightOrigin', '')) + ", " + str(getattr(self, 'flightDestination', '')))

