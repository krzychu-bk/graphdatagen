import random
from faker import Faker
from faker_airtravel import AirTravelProvider

fake = Faker()
fake.add_provider(AirTravelProvider)

def rm_att_quotes(json_like_str):
    atts = []
    for key, value in json_like_str.items():
        if isinstance(value, str):
            atts.append(f"{key}: \"{value}\"")
        else:
            atts.append(f"{key}: {value}")
    return "{"+", ".join(atts) + "}"

def gencyphernodes(data):
    creates = []
    for node in data:
        query = "CREATE(n:Airport" + node + ")"
        creates.append(query)
    return creates

airport_data = []
for _ in range(50):
    airport_data.append(rm_att_quotes(fake.airport_object()))


with open("airport_queries.txt", "w") as f:
        for query in gencyphernodes(airport_data):
            f.write(query + "\n\n")
