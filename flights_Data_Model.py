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
    return self.flight_origin

  def get_flight_destination(self):
    return self.flight_destination

  def get_status(self):
    return self.status

  def __str__(self):
    return (str(self.flight_number) + "\n" + str(self.status) + "\n" +
            str(getattr(self, 'flight_origin', '')) + "\n" + str(getattr(self, 'flight_destination', '')))

