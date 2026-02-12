import os
import random
import psycopg2
from faker import Faker
from datetime import datetime, timedelta

# Database connection parameters
DB_HOST = os.environ.get("DB_HOST", "db")
DB_NAME = os.environ.get("POSTGRES_DB", "pgdb")
DB_USER = os.environ.get("POSTGRES_USER", "pguser")
DB_PASS = os.environ.get("POSTGRES_PASSWORD", "pgpass")

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        exit(1)

def generate_data():
    fake = Faker()
    conn = get_db_connection()
    cur = conn.cursor()

    print("Connected to database...")

    # --- Generate Planes ---
    print("Generating Planes...")
    plane_types = {
        "Boeing 737": 180,
        "Boeing 747": 400,
        "Airbus A320": 150,
        "Airbus A380": 500,
        "Embraer E175": 76
    }
    
    planes_data = [] # List of tuples for executemany
    registrations = []

    for _ in range(15):
        registration = fake.unique.bothify(text='N#####')
        model = random.choice(list(plane_types.keys()))
        capacity = plane_types[model]
        planes_data.append((registration, model, capacity))
        registrations.append(registration)
    
    try:
        cur.executemany(
            "INSERT INTO planes (registration, fleet_type, capacity) VALUES (%s, %s, %s) ON CONFLICT (registration) DO NOTHING",
            planes_data
        )
        conn.commit()
    except Exception as e:
        print(f"Error inserting planes: {e}")
        conn.rollback()

    # --- Generate Passengers ---
    print("Generating Passengers...")
    passengers_data = []
    
    for _ in range(100):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.unique.email()
        phone = fake.phone_number()
        passengers_data.append((first_name, last_name, email, phone))

    try:
        cur.executemany(
            "INSERT INTO passengers (first_name, last_name, email, phone) VALUES (%s, %s, %s, %s) ON CONFLICT (email) DO NOTHING",
            passengers_data
        )
        conn.commit()
    except Exception as e:
        print(f"Error inserting passengers: {e}")
        conn.rollback()

    # Get newly created passengers for referencing
    cur.execute("SELECT passenger_id FROM passengers")
    passenger_ids = [row[0] for row in cur.fetchall()]

    # --- Generate Flights ---
    print("Generating Flights...")
    
    # Needs existing planes
    cur.execute("SELECT registration FROM planes")
    existing_planes = [row[0] for row in cur.fetchall()]
    
    if not existing_planes:
        print("No planes found to assign to flights.")
        return

    airports = ["JFK", "LAX", "ORD", "DFW", "DEN", "SFO", "SEA", "LAS", "MCO", "EWR"]
    flights_data = []
    generated_flights_info = [] 

    start_date = datetime.now()

    for _ in range(25):
        flight_number = fake.unique.bothify(text='??####')
        plane_registration = random.choice(existing_planes)
        departure_airport = random.choice(airports)
        arrival_airport = random.choice([a for a in airports if a != departure_airport])
        
        # Scheduled: random time in next 30 days
        days_offset = random.randint(0, 30)
        scheduled_departure = fake.date_time_between(start_date=start_date, end_date=start_date + timedelta(days=30))
        
        duration_hours = random.randint(1, 6)
        scheduled_arrival = scheduled_departure + timedelta(hours=duration_hours)

        flights_data.append((flight_number, plane_registration, departure_airport, arrival_airport, scheduled_departure, scheduled_arrival))
        
        generated_flights_info.append({
            "flight_number": flight_number,
            "scheduled_departure": scheduled_departure,
            "plane_registration": plane_registration
        })

    try:
        cur.executemany(
            "INSERT INTO flights (flight_number, plane_registration, departure_airport, arrival_airport, scheduled_departure, scheduled_arrival) VALUES (%s, %s, %s, %s, %s, %s)",
            flights_data
        )
        conn.commit()
    except Exception as e:
        print(f"Error inserting flights: {e}")
        conn.rollback()

    # --- Generate Tickets ---
    print("Generating Tickets...")
    tickets_data = []
    
    for flight in generated_flights_info:
        cur.execute("SELECT capacity FROM planes WHERE registration = %s", (flight["plane_registration"],))
        res = cur.fetchone()
        if not res:
             continue
        capacity = res[0]
        
        # Determine number of passengers for this flight (50% to 100% full, but max available passengers)
        num_passengers = random.randint(int(capacity * 0.5), capacity)
        # Sample available passengers
        if not passenger_ids:
            break
            
        current_flight_passengers = random.sample(passenger_ids, min(num_passengers, len(passenger_ids)))

        for i, pid in enumerate(current_flight_passengers):
            # Simple seat assignment logic
            row = (i // 6) + 1
            col = ['A', 'B', 'C', 'D', 'E', 'F'][i % 6]
            seat_number = f"{row}{col}"
            
            tickets_data.append((pid, flight["flight_number"], flight["scheduled_departure"], seat_number))

    try:
        cur.executemany(
            "INSERT INTO tickets (passenger_id, flight_number, scheduled_departure, seat_number) VALUES (%s, %s, %s, %s)",
            tickets_data
        )
        conn.commit()
    except Exception as e:
         print(f"Error inserting tickets: {e}")
         conn.rollback()

    print("Data generation complete!")
    cur.close()
    conn.close()

if __name__ == "__main__":
    generate_data()
