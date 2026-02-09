import re

class DestinationInfo:

  def __init__(self):
    self.destination_id = 0
    self.airport_iata_code = ''
    self.airport_name = ''
    self.city = ''
    self.country = ''

  ############## SETTERS ##################

  def set_destination_id(self, destination_id):
    try:
      val = int(destination_id)
      if val > 0:
        self.destination_id = val
      else:
        raise ValueError
    except (ValueError, TypeError):
      raise ValueError("Invalid destination ID. It should be a positive integer number.")

  def set_airport_iata_code(self, code):
    if not code:
      raise ValueError("IATA code cannot be empty")
    code = code.strip().upper()
    # check for 3 character IATA or 4 character ICAO codes if needed
    if len(code) not in (3, 4) or not re.match(r'^[A-Z0-9]{3,4}$', code):
      raise ValueError("Invalid IATA/ICAO code format")
    self.airport_iata_code = code

  def set_airport_name(self, name):
    if not name or not name.strip():
      raise ValueError("Airport name cannot be empty")
    self.airport_name = name.strip()

  def set_city(self, city):
    if not city or not city.strip():
      raise ValueError("City cannot be empty")
    self.city = city.strip()

  def set_country(self, country):
    if not country or not country.strip():
      raise ValueError("Country cannot be empty")
    self.country = country.strip()

  ############## GETTERS ##################

  def get_destination_id(self):
    return self.destination_id

  def get_airport_iata_code(self):
    return self.airport_iata_code

  def get_airport_name(self):
    return self.airport_name

  def get_city(self):
    return self.city

  def get_country(self):
    return self.country

  def __str__(self):
    return f"{self.airport_iata_code} - {self.airport_name}, {self.city}, {self.country}"
