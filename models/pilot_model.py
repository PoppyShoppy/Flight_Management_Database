class PilotInfo:

  def __init__(self):
    self.pilot_id = 0
    self.employee_id = ''
    self.first_name = ''
    self.last_name = ''
    self.contact_number = ''
    self.license_number = ''
    self.pilot_rank = ''

  ############## SETTERS ##################

  def set_pilot_id(self, pilot_id):
    try:
      val = int(pilot_id)
      if val > 0:
        self.pilot_id = val
      else:
        raise ValueError
    except (ValueError, TypeError):
      raise ValueError("Invalid pilot ID. It should be a positive integer number.")

  def set_employee_id(self, emp_id):
    if not emp_id or not str(emp_id).strip():
      raise ValueError("Employee ID cannot be empty")
    self.employee_id = str(emp_id).strip()

  def set_first_name(self, first):
    if not first or not first.strip():
      raise ValueError("First name cannot be empty")
    self.first_name = first.strip()

  def set_last_name(self, last):
    if not last or not last.strip():
      raise ValueError("Last name cannot be empty")
    self.last_name = last.strip()

  def set_contact_number(self, contact):
    if not contact or not str(contact).strip():
      raise ValueError("Contact number cannot be empty")
    self.contact_number = str(contact).strip()

  def set_license_number(self, license_no):
    if not license_no or not str(license_no).strip():
      raise ValueError("License number cannot be empty")
    self.license_number = str(license_no).strip()

  def set_pilot_rank(self, rank):
    if not rank or not rank.strip():
      raise ValueError("Pilot rank cannot be empty")
    self.pilot_rank = rank.strip()

  ############## GETTERS ##################

  def get_pilot_id(self):
    return self.pilot_id

  def get_employee_id(self):
    return self.employee_id

  def get_first_name(self):
    return self.first_name

  def get_last_name(self):
    return self.last_name

  def get_contact_number(self):
    return self.contact_number

  def get_license_number(self):
    return self.license_number

  def get_pilot_rank(self):
    return self.pilot_rank

  def __str__(self):
    return f"{self.employee_id} - {self.first_name} {self.last_name} ({self.pilot_rank})"
