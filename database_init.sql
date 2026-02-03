-- Destinations (airports) table
CREATE TABLE destinations (
    destination_id VARCHAR(10) PRIMARY KEY,
    airport_iata_code VARCHAR(3) UNIQUE NOT NULL,  -- e.g., 'JFK', 'LAX'
    airport_name VARCHAR(100),
    city VARCHAR(50), -- can city and country become 
    country VARCHAR(50)
);

-- Pilots table
CREATE TABLE pilots (
    pilot_id INT PRIMARY KEY,
    employee_id VARCHAR(20) UNIQUE NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    contact_number VARCHAR(50), 
    license_number VARCHAR(20),
    pilot_rank VARCHAR(20),
    
);

-- Flights table
CREATE TABLE flights (
    flight_id INT PRIMARY KEY, --euniquely identifies a specific flight instance on a specific date/time
    flight_number VARCHAR(10) NOT NULL,  -- e.g., 'AA123'
    departure_time DATETIME,
    arrival_time DATETIME,

    -- Foreign keys
    origin_id INT,  -- Where the flight starts --foreign key but not sure where i would reference this
    destination_id INT,  -- Where the flight ends
    
    FOREIGN KEY (origin_id) REFERENCES destinations(destination_id),
    FOREIGN KEY (destination_id) REFERENCES destinations(destination_id)
);






-- Insert airports
INSERT INTO airports VALUES 
(1, 'JFK', 'John F Kennedy International', 'New York', 'USA'),
(2, 'LHR', 'Heathrow Airport', 'London', 'UK');

-- Insert pilots
INSERT INTO pilots VALUES
(101, 'EMP001', 'John', 'Smith', '555-0101', 'LIC001', 'Captain'),
(102, 'EMP002', 'Sarah', 'Jones', '555-0102', 'LIC002', 'First Officer'),
(103, 'EMP003', 'Mike', 'Brown', '555-0103', 'LIC003', 'Training Captain');

-- Insert a flight
INSERT INTO flights VALUES
(1001, 'AA100', '2024-03-15 08:00:00', '2024-03-15 20:00:00', 1, 2);

-- Assign pilots to the flight (2 pilots for normal flight)
INSERT INTO flight_assignments VALUES
(1, 1001, 101, 'Captain'),
(2, 1001, 102, 'First Officer');

-- For a training flight with 3 pilots:
INSERT INTO flight_assignments VALUES
(3, 1001, 103, 'Training Captain');