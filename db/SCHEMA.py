SCHEMA_SQL = """

CREATE TABLE IF NOT EXISTS destinations (
    destination_id INTEGER PRIMARY KEY AUTOINCREMENT,
    airport_iata_code VARCHAR(3) UNIQUE NOT NULL,
    airport_name VARCHAR(255),
    city VARCHAR(50),
    country VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS pilots (
    pilot_id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id VARCHAR(20) UNIQUE NOT NULL,
    first_name VARCHAR(30) NOT NULL,
    last_name VARCHAR(30) NOT NULL,
    contact_number VARCHAR(20) UNIQUE NOT NULL,
    license_number VARCHAR(15) UNIQUE NOT NULL,
    pilot_rank VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS flights (
    FlightID INTEGER PRIMARY KEY AUTOINCREMENT,
    flight_number VARCHAR(10) NOT NULL,
    scheduled_departure DATETIME NOT NULL,
    Status VARCHAR(15),
    flightOrigin INTEGER NOT NULL,
    flightDestination INTEGER NOT NULL,
    FOREIGN KEY (flightOrigin) REFERENCES destinations(destination_id),
    FOREIGN KEY (flightDestination) REFERENCES destinations(destination_id),
    CHECK (flightOrigin <> flightDestination) -- no circular flights
);

CREATE TABLE IF NOT EXISTS flight_crew (
    flight_crew_id INTEGER PRIMARY KEY AUTOINCREMENT,
    flight_id INTEGER NOT NULL,
    pilot_id INTEGER NOT NULL,
    role VARCHAR(20) NOT NULL,
    is_flying_pilot BOOLEAN DEFAULT 0,
    FOREIGN KEY (flight_id) REFERENCES flights(FlightID),
    FOREIGN KEY (pilot_id) REFERENCES pilots(pilot_id) ON DELETE CASCADE,
    UNIQUE(flight_id, pilot_id)
);
"""