from faker import Faker
import random
from datetime import timedelta

FLEET_DATA = [
    ('AA', 'Boeing 737-800', 172, 'AA'),
    ('AA', 'Airbus A321neo', 196, 'AN'),
    ('AA', 'Boeing 777-300ER', 304, 'AA'),
    ('DL', 'Airbus A321-200', 191, 'DN'),
    ('DL', 'Boeing 757-200', 199, 'DL'),
    ('DL', 'Airbus A350-900', 306, 'DZ'),
    ('UA', 'Boeing 737 MAX 9', 179, 'U'),
    ('UA', 'Boeing 787-9', 252, 'UA'),
    ('UA', 'Airbus A319-100', 126, 'UA'),
    ('WN', 'Boeing 737-700', 143, 'SW'),
    ('WN', 'Boeing 737 MAX 8', 175, 'WN'),
    ('AS', 'Boeing 737-900ER', 178, 'AS'),
    ('B6', 'Airbus A220-300', 140, 'JB')]

DOMESTIC_AIRPORT_CODE = [
    'ATL', 'LAX', 'ORD', 'DFW', 'DEN', 'JFK', 'SFO', 'LAS', 'SEA', 'MCO']

# (Origin, Destination)
FLIGHT_TIME_STATISTIC = {
    # ATL Departures
    ('ATL', 'LAX'): {'mean': 295, 'std': 22},
    ('ATL', 'ORD'): {'mean': 125, 'std': 15},
    ('ATL', 'DFW'): {'mean': 135, 'std': 14},
    ('ATL', 'DEN'): {'mean': 205, 'std': 18},
    ('ATL', 'JFK'): {'mean': 130, 'std': 16},
    ('ATL', 'SFO'): {'mean': 315, 'std': 24},
    ('ATL', 'LAS'): {'mean': 280, 'std': 20},
    ('ATL', 'SEA'): {'mean': 335, 'std': 25},
    ('ATL', 'MCO'): {'mean': 95, 'std': 12},

    # LAX Departures
    ('LAX', 'ATL'): {'mean': 265, 'std': 20},
    ('LAX', 'ORD'): {'mean': 245, 'std': 22},
    ('LAX', 'DFW'): {'mean': 185, 'std': 16},
    ('LAX', 'DEN'): {'mean': 150, 'std': 15},
    ('LAX', 'JFK'): {'mean': 325, 'std': 28},
    ('LAX', 'SFO'): {'mean': 85, 'std': 10},
    ('LAX', 'LAS'): {'mean': 70, 'std': 10},
    ('LAX', 'SEA'): {'mean': 175, 'std': 15},
    ('LAX', 'MCO'): {'mean': 305, 'std': 25},

    # ORD Departures
    ('ORD', 'ATL'): {'mean': 115, 'std': 15},
    ('ORD', 'LAX'): {'mean': 265, 'std': 25},
    ('ORD', 'DFW'): {'mean': 145, 'std': 16},
    ('ORD', 'DEN'): {'mean': 160, 'std': 18},
    ('ORD', 'JFK'): {'mean': 135, 'std': 20},
    ('ORD', 'SFO'): {'mean': 285, 'std': 26},
    ('ORD', 'LAS'): {'mean': 245, 'std': 22},
    ('ORD', 'SEA'): {'mean': 270, 'std': 24},
    ('ORD', 'MCO'): {'mean': 165, 'std': 18},

    # DFW Departures
    ('DFW', 'ATL'): {'mean': 120, 'std': 12},
    ('DFW', 'LAX'): {'mean': 200, 'std': 18},
    ('DFW', 'ORD'): {'mean': 135, 'std': 15},
    ('DFW', 'DEN'): {'mean': 125, 'std': 14},
    ('DFW', 'JFK'): {'mean': 215, 'std': 20},
    ('DFW', 'SFO'): {'mean': 235, 'std': 22},
    ('DFW', 'LAS'): {'mean': 175, 'std': 16},
    ('DFW', 'SEA'): {'mean': 260, 'std': 20},
    ('DFW', 'MCO'): {'mean': 155, 'std': 15},

    # DEN Departures
    ('DEN', 'ATL'): {'mean': 185, 'std': 16},
    ('DEN', 'LAX'): {'mean': 155, 'std': 15},
    ('DEN', 'ORD'): {'mean': 145, 'std': 18},
    ('DEN', 'DFW'): {'mean': 115, 'std': 12},
    ('DEN', 'JFK'): {'mean': 235, 'std': 22},
    ('DEN', 'SFO'): {'mean': 165, 'std': 18},
    ('DEN', 'LAS'): {'mean': 110, 'std': 12},
    ('DEN', 'SEA'): {'mean': 170, 'std': 16},
    ('DEN', 'MCO'): {'mean': 215, 'std': 19},

    # JFK Departures
    ('JFK', 'ATL'): {'mean': 145, 'std': 18},
    ('JFK', 'LAX'): {'mean': 365, 'std': 30},
    ('JFK', 'ORD'): {'mean': 150, 'std': 22},
    ('JFK', 'DFW'): {'mean': 245, 'std': 25},
    ('JFK', 'DEN'): {'mean': 275, 'std': 24},
    ('JFK', 'SFO'): {'mean': 385, 'std': 32},
    ('JFK', 'LAS'): {'mean': 355, 'std': 28},
    ('JFK', 'SEA'): {'mean': 375, 'std': 30},
    ('JFK', 'MCO'): {'mean': 175, 'std': 18},

    # SFO Departures
    ('SFO', 'ATL'): {'mean': 285, 'std': 22},
    ('SFO', 'LAX'): {'mean': 90, 'std': 15},
    ('SFO', 'ORD'): {'mean': 250, 'std': 24},
    ('SFO', 'DFW'): {'mean': 215, 'std': 20},
    ('SFO', 'DEN'): {'mean': 155, 'std': 16},
    ('SFO', 'JFK'): {'mean': 335, 'std': 28},
    ('SFO', 'LAS'): {'mean': 95, 'std': 12},
    ('SFO', 'SEA'): {'mean': 125, 'std': 15},
    ('SFO', 'MCO'): {'mean': 325, 'std': 26},

    # LAS Departures
    ('LAS', 'ATL'): {'mean': 250, 'std': 20},
    ('LAS', 'LAX'): {'mean': 75, 'std': 10},
    ('LAS', 'ORD'): {'mean': 220, 'std': 20},
    ('LAS', 'DFW'): {'mean': 160, 'std': 15},
    ('LAS', 'DEN'): {'mean': 115, 'std': 12},
    ('LAS', 'JFK'): {'mean': 310, 'std': 26},
    ('LAS', 'SFO'): {'mean': 100, 'std': 12},
    ('LAS', 'SEA'): {'mean': 160, 'std': 15},
    ('LAS', 'MCO'): {'mean': 280, 'std': 22},

    # SEA Departures
    ('SEA', 'ATL'): {'mean': 295, 'std': 24},
    ('SEA', 'LAX'): {'mean': 165, 'std': 16},
    ('SEA', 'ORD'): {'mean': 240, 'std': 22},
    ('SEA', 'DFW'): {'mean': 235, 'std': 20},
    ('SEA', 'DEN'): {'mean': 160, 'std': 16},
    ('SEA', 'JFK'): {'mean': 325, 'std': 28},
    ('SEA', 'SFO'): {'mean': 130, 'std': 15},
    ('SEA', 'LAS'): {'mean': 150, 'std': 15},
    ('SEA', 'MCO'): {'mean': 335, 'std': 26},

    # MCO Departures
    ('MCO', 'ATL'): {'mean': 100, 'std': 12},
    ('MCO', 'LAX'): {'mean': 335, 'std': 28},
    ('MCO', 'ORD'): {'mean': 175, 'std': 20},
    ('MCO', 'DFW'): {'mean': 170, 'std': 16},
    ('MCO', 'DEN'): {'mean': 255, 'std': 22},
    ('MCO', 'JFK'): {'mean': 160, 'std': 18},
    ('MCO', 'SFO'): {'mean': 365, 'std': 30},
    ('MCO', 'LAS'): {'mean': 315, 'std': 25},
    ('MCO', 'SEA'): {'mean': 385, 'std': 32},
}

def generate_plane_row(faker):
    fleet = random.choice(FLEET_DATA)
    registration = f'N{faker.bothify(text='%##')}{fleet[3]}'
    fleet_type = fleet[1]
    capacity = fleet[2]
    
    return [registration, fleet_type, capacity]

def generate_passenger_row(faker):
    first_name = faker.first_name()
    last_name = faker.last_name()
    email = faker.email()
    phone = faker.phone_number()
    
    return [first_name, last_name, email, phone]

def generate_flight_row(faker, airline_code, departure_start_date='now'):
    flight_number = f'{airline_code}{faker.bothify(text='@!!!')}'

    departure_airport = random.choice(DOMESTIC_AIRPORT_CODE)
    arrival_airport = random.choice([
        code for code in DOMESTIC_AIRPORT_CODE if code != departure_airport])

    scheduled_departure = faker.date_time_between(start_date=departure_start_date, end_date='+1d')

    mean_flight_time = FLIGHT_TIME_STATISTIC[(departure_airport, arrival_airport)]['mean']
    std_flight_time = FLIGHT_TIME_STATISTIC[(departure_airport, arrival_airport)]['std']

    estimated_flight_time = random.gauss(mean_flight_time, std_flight_time)
    assert estimated_flight_time > 0, 'Estimated flight time must be positive'

    scheduled_arrival = scheduled_departure + timedelta(minutes=estimated_flight_time)

    return [flight_number, departure_airport, arrival_airport, scheduled_departure, scheduled_arrival]

if __name__ == '__main__':
    faker = Faker()
    for _ in range(10):
        row = generate_plane_row(faker)
        print(f'registration: {row[0]}, fleet_type: {row[1]}, capacity: {row[2]}')
    
    for _ in range(10):
        row = generate_passenger_row(faker)
        print(f'first_name: {row[0]}, last_name: {row[1]}, email: {row[2]}, phone: {row[3]}')
    
    for i in range(10):
        row = generate_flight_row(faker, 'AA', f'+{i}d')
        print(f'flight_number: {row[0]}, departure_airport: {row[1]}, arrival_airport: {row[2]}, scheduled_departure: {row[3]}, scheduled_arrival: {row[4]}')