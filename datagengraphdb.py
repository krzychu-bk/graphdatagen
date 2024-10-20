import random
import datetime
from faker import Faker

# Initialize the Faker instance
fake = Faker()

# Function to generate fake airports
def generate_fake_airports(num_airports=10):
    airports = []
    for _ in range(num_airports):
        airport = {
            "code": fake.unique.lexify(text='???').upper(),  # Generate a random 3-letter code
            "name": f"{fake.city()} International Airport",
            "city": fake.city(),
            "country": fake.country(),
            "transfer_time": random.randint(20, 120)
        }
        airports.append(airport)
    return airports

# Function to generate random flights between the fake airports
def generate_random_flights(airports, num_flights=10):
    flights = []
    for _ in range(num_flights):
        # Randomly pick two different airports
        departure_airport = random.choice(airports)
        arrival_airport = random.choice(airports)
        while arrival_airport == departure_airport:
            arrival_airport = random.choice(airports)

        # Generate random flight details
        flight_number = f"{random.choice(['AA', 'BA', 'DL', 'AF', 'EK', 'JL'])}{random.randint(100, 999)}"
        departure_time = datetime.datetime.now() + datetime.timedelta(minutes=random.randint(30, 300))
        arrival_time = departure_time + datetime.timedelta(minutes=random.randint(60, 600))
        duration = (arrival_time - departure_time).seconds // 60
        price = random.randint(200,2000)
        flight = {
            "flight_number": flight_number,
            "departure_airport": departure_airport["code"],
            "arrival_airport": arrival_airport["code"],
            "departure_time": departure_time.strftime("%Y-%m-%dT%H:%M:%S"),
            "arrival_time": arrival_time.strftime("%Y-%m-%dT%H:%M:%S"),
            "duration": duration,
            "price": price,
        }
        flights.append(flight)
    return flights

# Generate fake airports and flights
airports = generate_fake_airports(50)  # Generate n fake airports
flights = generate_random_flights(airports, 200)  # Generate m random flights

# Generate Cypher queries to insert the data into Neo4j
def generate_cypher_queries(airports, flights):
    # Create queries for airports
    airport_queries = []
    i = 0
    for airport in airports:
        airport_query = f"""
        MERGE (a{i}:Airport {{code: '{airport['code']}'}})
        ON CREATE SET a.name = '{airport['name']}', a.city = '{airport['city']}', a.country = '{airport['country']}', a.transfer_time = {airport['transfer_time']}'
        """
        airport_queries.append(airport_query.strip())
        i = i + 1  
    # Create queries for flights
    flight_queries = []
    for flight in flights:
        flight_query = f"""
        MATCH (origin:Airport {{code: '{flight['departure_airport']}'}})
        MATCH (destination:Airport {{code: '{flight['arrival_airport']}'}})
        CREATE (origin)-[:FLIGHT {{
            flight_number: '{flight['flight_number']}',
            departure_time: datetime('{flight['departure_time']}'),
            arrival_time: datetime('{flight['arrival_time']}'),
            duration: {flight['duration']},
            price: {flight['price']}
        }}]->(destination)
        """
        flight_queries.append(flight_query.strip())

    return airport_queries, flight_queries

# Save the Cypher queries to text files
def save_queries_to_files(airport_queries, flight_queries):
    # Save airport queries to a file
    with open("airport_queries.txt", "w") as f:
        for query in airport_queries:
            f.write(query + "\n\n")
    
    # Save flight queries to a file
    with open("flight_queries.txt", "w") as f:
        for query in flight_queries:
            f.write(query + "\n\n")

# Generate the Cypher queries
airport_queries, flight_queries = generate_cypher_queries(airports, flights)

# Save the queries to text files
save_queries_to_files(airport_queries, flight_queries)

print("Cypher queries have been saved to 'airport_queries.txt' and 'flight_queries.txt'.")
