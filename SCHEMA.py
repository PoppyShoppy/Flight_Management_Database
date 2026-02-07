SCHEMA_SQL = """DROP TABLE IF EXISTS flight_crew;
DROP TABLE IF EXISTS flights;
DROP TABLE IF EXISTS pilots;
DROP TABLE IF EXISTS destinations;

CREATE TABLE IF NOT EXISTS destinations (
    destination_id INTEGER PRIMARY KEY AUTOINCREMENT,
    airport_iata_code VARCHAR(3) UNIQUE NOT NULL,
    airport_name VARCHAR(100),
    city VARCHAR(50),
    country VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS pilots (
    pilot_id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id VARCHAR(20) UNIQUE NOT NULL,
    first_name VARCHAR(30),
    last_name VARCHAR(30),
    contact_number VARCHAR(20),
    license_number VARCHAR(15),
    pilot_rank VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS flights (
    FlightID INTEGER PRIMARY KEY AUTOINCREMENT,
    flight_number VARCHAR(10) NOT NULL,
    Status VARCHAR(15),
    flightOrigin INTEGER,
    flightDestination INTEGER,
    FOREIGN KEY (flightOrigin) REFERENCES destinations(destination_id),
    FOREIGN KEY (flightDestination) REFERENCES destinations(destination_id)
);

CREATE TABLE IF NOT EXISTS flight_crew (
    flight_crew_id INTEGER PRIMARY KEY AUTOINCREMENT,
    flight_id INTEGER NOT NULL,
    pilot_id INTEGER NOT NULL,
    role VARCHAR(20) NOT NULL,
    is_flying_pilot BOOLEAN DEFAULT 0,
    FOREIGN KEY (flight_id) REFERENCES flights(flight_id),
    FOREIGN KEY (pilot_id) REFERENCES pilots(pilot_id),
    UNIQUE(flight_id, pilot_id)
);

-- Insert airports (15 destinations)
INSERT INTO destinations (airport_iata_code, airport_name, city, country) VALUES 
('JFK', 'John F Kennedy International', 'New York', 'USA'),
('LHR', 'London Heathrow Airport', 'London', 'UK'),
('CDG', 'Paris Charles de Gaulle', 'Paris', 'France'),
('AMS', 'Amsterdam Airport Schiphol', 'Amsterdam', 'Netherlands'),
('FRA', 'Frankfurt am Main', 'Frankfurt', 'Germany'),
('ORY', 'Paris Orly Airport', 'Paris', 'France'),
('DUB', 'Dublin Airport', 'Dublin', 'Ireland'),
('FCO', 'Rome Fiumicino Leonardo da Vinci', 'Rome', 'Italy'),
('MAD', 'Adolfo Suárez Madrid-Barajas', 'Madrid', 'Spain'),
('BCN', 'Barcelona-El Prat', 'Barcelona', 'Spain'),
('ZRH', 'Zurich Airport', 'Zurich', 'Switzerland'),
('VIE', 'Vienna International Airport', 'Vienna', 'Austria'),
('LAX', 'Los Angeles International', 'Los Angeles', 'USA'),
('ORD', 'Chicago O''Hare International', 'Chicago', 'USA'),
('SFO', 'San Francisco International', 'San Francisco', 'USA');

-- Insert pilots (15 pilots)
INSERT INTO pilots (employee_id, first_name, last_name, contact_number, license_number, pilot_rank) VALUES
('EMP001', 'John', 'Smith', '555-0101', 'LIC001001', 'Captain'),
('EMP002', 'Sarah', 'Jones', '555-0102', 'LIC001002', 'First Officer'),
('EMP003', 'Mike', 'Brown', '555-0103', 'LIC001003', 'Captain'),
('EMP004', 'Emily', 'Davis', '555-0104', 'LIC001004', 'First Officer'),
('EMP005', 'Robert', 'Wilson', '555-0105', 'LIC001005', 'Captain'),
('EMP006', 'Jennifer', 'Martinez', '555-0106', 'LIC001006', 'First Officer'),
('EMP007', 'David', 'Anderson', '555-0107', 'LIC001007', 'Captain'),
('EMP008', 'Lisa', 'Taylor', '555-0108', 'LIC001008', 'First Officer'),
('EMP009', 'James', 'Thomas', '555-0109', 'LIC001009', 'Captain'),
('EMP010', 'Maria', 'Jackson', '555-0110', 'LIC001010', 'First Officer'),
('EMP011', 'Christopher', 'White', '555-0111', 'LIC001011', 'Captain'),
('EMP012', 'Amanda', 'Harris', '555-0112', 'LIC001012', 'First Officer'),
('EMP013', 'Richard', 'Martin', '555-0113', 'LIC001013', 'Captain'),
('EMP014', 'Patricia', 'Thompson', '555-0114', 'LIC001014', 'First Officer'),
('EMP015', 'Daniel', 'Garcia', '555-0115', 'LIC001015', 'Captain');

INSERT INTO flights (flight_number, Status, flightOrigin, flightDestination) VALUES
('AA100', 'Completed', 1, 2),
('BA201', 'Completed', 2, 1),
('AF302', 'Scheduled', 3, 5),
('KL403', 'Scheduled', 4, 3),
('LH504', 'Boarding', 5, 4),
('AZ605', 'Delayed', 8, 9),
('EI706', 'Scheduled', 7, 2),
('IB807', 'Scheduled', 9, 10),
('VY908', 'Scheduled', 10, 9),
('SR009', 'Scheduled', 11, 12),
('OS110', 'Scheduled', 12, 11),
('DL211', 'Scheduled', 1, 13),
('UA312', 'Scheduled', 14, 15),
('AM413', 'Scheduled', 15, 13),
('AC514', 'Scheduled', 2, 1);

-- Assign pilots to flights (2 pilots per flight)
INSERT INTO flight_crew (flight_id, pilot_id, role, is_flying_pilot) VALUES
(1, 1, 'Captain', 1),
(1, 2, 'First Officer', 0),
(2, 3, 'Captain', 1),
(2, 4, 'First Officer', 0),
(3, 5, 'Captain', 1),
(3, 6, 'First Officer', 0),
(4, 7, 'Captain', 1),
(4, 8, 'First Officer', 0),
(5, 9, 'Captain', 1),
(5, 10, 'First Officer', 0),
(6, 11, 'Captain', 1),
(6, 12, 'First Officer', 0),
(7, 13, 'Captain', 1),
(7, 14, 'First Officer', 0),
(8, 15, 'Captain', 1),
(8, 1, 'First Officer', 0),
(9, 2, 'Captain', 1),
(9, 3, 'First Officer', 0),
(10, 4, 'Captain', 1),
(10, 5, 'First Officer', 0),
(11, 6, 'Captain', 1),
(11, 7, 'First Officer', 0),
(12, 8, 'Captain', 1),
(12, 9, 'First Officer', 0),
(13, 10, 'Captain', 1),
(13, 11, 'First Officer', 0),
(14, 12, 'Captain', 1),
(14, 13, 'First Officer', 0),
(15, 14, 'Captain', 1),
(15, 15, 'First Officer', 0);
"""