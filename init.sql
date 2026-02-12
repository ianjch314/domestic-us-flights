CREATE TABLE planes (
    registration VARCHAR(20) PRIMARY KEY,
    fleet_type VARCHAR(255) NOT NULL,
    capacity INT NOT NULL
);

CREATE TABLE passengers (
    passenger_id SERIAL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(32) NOT NULL
);

CREATE TABLE flights (
    flight_id SERIAL PRIMARY KEY,
    flight_number VARCHAR(255) NOT NULL,
    plane_registration VARCHAR(20) NOT NULL,
    departure_airport VARCHAR(255) NOT NULL,
    arrival_airport VARCHAR(255) NOT NULL,
    scheduled_departure TIMESTAMP NOT NULL,
    scheduled_arrival TIMESTAMP NOT NULL,

    FOREIGN KEY (plane_registration)
    REFERENCES planes (registration),

    UNIQUE (flight_number, scheduled_departure)
);

CREATE TABLE tickets (
    ticket_id SERIAL PRIMARY KEY,
    passenger_id INT NOT NULL,
    flight_number VARCHAR(255) NOT NULL,
    scheduled_departure TIMESTAMP NOT NULL,
    seat_number VARCHAR(255) NOT NULL,

    FOREIGN KEY (passenger_id)
    REFERENCES passengers (passenger_id),

    FOREIGN KEY (flight_number, scheduled_departure)
    REFERENCES flights (flight_number, scheduled_departure)
);