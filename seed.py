import json
import random
from datetime import datetime, timedelta
from database import flights_col, prices_col

with open("seed_data.json", "r") as f:
    flights = json.load(f)

flights_col.delete_many({})
prices_col.delete_many({})

for flight in flights:
    result = flights_col.insert_one(flight)
    flight_id = result.inserted_id

    dep_date = datetime.fromisoformat(flight["departure_date"])
    interval = flight["interval_days"]
    current_date = dep_date - timedelta(days=180)
    price = random.randint(500, 900)

    while current_date < dep_date:
        price += random.randint(-20, 30)
        prices_col.insert_one({
            "flight_id": flight_id,
            "route": flight["route"],
            "airline": flight["airline"],
            "date": current_date,
            "price": price
        })
        current_date += timedelta(days=interval)


flights_col.create_index([("route", "text"), ("airline", "text")])

print(" flightDB.flightRecord seeded successfully with sample flight and price data!")
