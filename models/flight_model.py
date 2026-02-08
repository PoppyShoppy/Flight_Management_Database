import re
class FlightInfo:

  def __init__(self):
  
    self.flightID = 0
    self.flight_number = ''
    self.flightOrigin = ''
    self.flightDestination = ''
    self.status = ''

############## SETTERS ##################

  def set_flight_id(self, flightID):
    try:
      #checks if input is a number. FlightId is automatically generated in the database but in case an event occurs when flightID is entered this check is there.
      if isinstance(flightID, str):
          input_val = int(flightID)
      else:
          input_val = flightID
      if input_val > 0:
        self.flightID = input_val
      else: 
        raise ValueError
    except(ValueError, TypeError):
      raise ValueError("Invalid flight ID. It should be a positive integer number.")

  def set_flight_number(self, flight_number):

    pattern = r'^[A-Z]{2}\d{3}$'

    flight_number = flight_number.strip().upper()

    if re.match(pattern, flight_number):
        self.flight_number = flight_number
    else:
        raise ValueError("Invalid flight number format. It should be two uppercase letters followed by three digits (e.g., BB123).")
    
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

  def __str__(self):
    return ("\n" + str(self.flight_number) + ", " + str(self.status) + ", " +
            str(getattr(self, 'flightOrigin', '')) + ", " + str(getattr(self, 'flightDestination', '')))

