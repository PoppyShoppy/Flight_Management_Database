PRAGMA database_list;
DROP TABLE IF EXISTS flight_crew;
DROP TABLE IF EXISTS flights;
DROP TABLE IF EXISTS pilots;
DROP TABLE IF EXISTS destinations;

-- Destinations (airports) table
CREATE TABLE IF NOT EXISTS destinations (
    destination_id INTEGER PRIMARY KEY AUTOINCREMENT, -- unique identifier for each destination, using int for simplicity, auto-incrementing and efficient indexing, storage and performance benefits, and easy to reference in other tables as foreign keys
    airport_iata_code VARCHAR(3) UNIQUE NOT NULL,  -- e.g., 'JFK', 'LAX', candidate key for airports, unique and standardized, allows for efficient lookups and joins, and is widely used in the aviation industry
    airport_name VARCHAR(100), -- e.g., 'John F Kennedy International', provides descriptive information about the airport, useful for display and reporting purposes
    city VARCHAR(50), 
    country VARCHAR(50)
);

-- Pilots table
CREATE TABLE IF NOT EXISTS pilots (
    pilot_id INTEGER PRIMARY KEY AUTOINCREMENT, -- unique identifier for each pilot, using int for simplicity, auto-incrementing and efficient indexing, storage and performance benefits, and easy to reference in other tables as foreign keys
    employee_id VARCHAR(20) UNIQUE NOT NULL,
    first_name VARCHAR(30), -- Most names fit within 30 characters; extremely rare that a name would need more
    last_name VARCHAR(30), -- similar rationale as above 
    contact_number VARCHAR(20), 
    license_number VARCHAR(15),
    pilot_rank VARCHAR(20)    
);

-- Flights table
CREATE TABLE IF NOT EXISTS flights (
    FlightID INTEGER PRIMARY KEY AUTOINCREMENT, -- identifies a specific flight instance
    flight_number VARCHAR(10) NOT NULL,  -- e.g., 'AA123'
    scheduled_departure DATETIME NOT NULL,          -- the date and time of the flight, important for scheduling and historical records
    Status VARCHAR(15),                  -- e.g., 'Scheduled', 'Delayed', 'Cancelled', 'Completed', 'Boarding'
    -- Foreign keys
    flightOrigin INTEGER,               -- Where the flight starts
    flightDestination INTEGER,          -- Where the flight ends
    
    FOREIGN KEY (flightOrigin) REFERENCES destinations(destination_id),
    FOREIGN KEY (flightDestination) REFERENCES destinations(destination_id)
);

-- Flight Crew table
-- Advantages: Scalable to any number of pilots, Clear role assignment, Easy to query by role, Maintains referential integrity. 
CREATE TABLE IF NOT EXISTS flight_crew (
    flight_crew_id INTEGER PRIMARY KEY AUTOINCREMENT,
    flight_id INTEGER NOT NULL,
    pilot_id INTEGER NOT NULL,
    role VARCHAR(20) NOT NULL,  -- 'Captain', 'First Officer', not making this a fk allows for flexiblity of new roles
    is_flying_pilot BOOLEAN DEFAULT 0, -- indicate if this pilot is the flying pilot/captain.
    FOREIGN KEY (flight_id) REFERENCES flights(FlightID), -- 
    FOREIGN KEY (pilot_id) REFERENCES pilots(pilot_id),
    UNIQUE(flight_id, pilot_id)  -- Prevents same pilot twice on the same flight
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

-- Insert flights (Added '2024-05-20' as the date for all initial records)
INSERT INTO flights (flight_number, flight_date, Status, flightOrigin, flightDestination) VALUES
('AA100', '2024-05-20', 'Completed', 1, 2),
('BA201', '2024-05-20', 'Completed', 2, 1),
('AF302', '2024-05-20', 'Scheduled', 3, 5),
('KL403', '2024-05-20', 'Scheduled', 4, 3),
('LH504', '2024-05-20', 'Boarding', 5, 4),
('AZ605', '2024-05-20', 'Delayed', 8, 9),
('EI706', '2024-05-20', 'Scheduled', 7, 2),
('IB807', '2024-05-20', 'Scheduled', 9, 10),
('VY908', '2024-05-20', 'Scheduled', 10, 9),
('SR009', '2024-05-20', 'Scheduled', 11, 12),
('OS110', '2024-05-20', 'Scheduled', 12, 11),
('DL211', '2024-05-20', 'Scheduled', 1, 13),
('UA312', '2024-05-20', 'Scheduled', 14, 15),
('AM413', '2024-05-20', 'Scheduled', 15, 13),
('AC514', '2024-05-20', 'Scheduled', 2, 1);

-- Assign pilots to flights
INSERT INTO flight_crew (flight_id, pilot_id, role, is_flying_pilot) VALUES
(1, 1, 'Captain', 1),
(1, 2, 'First Officer', 0),
(2, 3, 'Captain', 1),
(2, 4, 'First Officer', 0),
(3, 5, 'Captain', 1),
(3, 6, 'First Officer', 0);
