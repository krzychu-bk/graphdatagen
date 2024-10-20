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
    i = 0
    for node in data:
        query = "CREATE(a"+str(i)+":Airport" + node + ")"
        creates.append(query)
        i = i + 1
    return creates

airport_data = []
IATAcollection = []
for _ in range(50):
    airport = fake.airport_object()
    iata = airport
    airport_data.append(rm_att_quotes(airport))
    IATAcollection.append(iata)

with open("airport_queries.txt", "w") as f:
        for query in gencyphernodes(airport_data):
            f.write(query + "\n\n")

print(IATAcollection)