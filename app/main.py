from faker import Faker
import random

FLEET_DATA = [
    ('American Airlines', 'Boeing 737-800', 172, 'AA'),
    ('American Airlines', 'Airbus A321neo', 196, 'AN'),
    ('American Airlines', 'Boeing 777-300ER', 304, 'AA'),
    ('Delta Air Lines', 'Airbus A321-200', 191, 'DN'),
    ('Delta Air Lines', 'Boeing 757-200', 199, 'DL'),
    ('Delta Air Lines', 'Airbus A350-900', 306, 'DZ'),
    ('United Airlines', 'Boeing 737 MAX 9', 179, 'U'),
    ('United Airlines', 'Boeing 787-9', 252, 'UA'),
    ('United Airlines', 'Airbus A319-100', 126, 'UA'),
    ('Southwest Airlines', 'Boeing 737-700', 143, 'SW'),
    ('Southwest Airlines', 'Boeing 737 MAX 8', 175, 'WN'),
    ('Alaska Airlines', 'Boeing 737-900ER', 178, 'AS'),
    ('JetBlue', 'Airbus A220-300', 140, 'JB')]

def generate_plane_row(faker):
    fleet = random.choice(FLEET_DATA)
    registration = f'N{faker.bothify(text="%##")}{fleet[3]}'
    
    return [registration, fleet[1], fleet[2]]

def generate_passenger_row(faker):
    first_name = faker.first_name()
    last_name = faker.last_name()
    email = faker.email()
    phone_number = faker.phone_number()
    
    return [first_name, last_name, email, phone_number]

if __name__ == '__main__':
    faker = Faker()
    for _ in range(10):
        row = generate_plane_row(faker)
        print(f'registration: {row[0]}, type: {row[1]}, capacity: {row[2]}')
    
    for _ in range(10):
        row = generate_passenger_row(faker)
        print(f'first_name: {row[0]}, last_name: {row[1]}, email: {row[2]}, phone: {row[3]}')