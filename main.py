from fastapi import FastAPI, HTTPException
from datetime import datetime
from bson import ObjectId
from database import flights_col, prices_col
from models import FlightResponse, PriceHistoryResponse, SearchResult
import math
import subprocess

app = FastAPI(title="Flight Price Tracker")

@app.post("/api/seed")
def seed_data():
    subprocess.run(["python", "seed.py"])
    return {"message": "Database seeded successfully!"}

@app.get("/api/flights", response_model=list[FlightResponse])
def get_flights():
    flights = list(flights_col.find({}, {"_id": 1, "route": 1, "airline": 1, "departure_date": 1}))
    return [
        FlightResponse(
            flight_id=str(f["_id"]),
            route=f["route"],
            airline=f["airline"],
            departure_date=f["departure_date"]
        ) for f in flights
    ]

@app.get("/api/prices", response_model=PriceHistoryResponse)
def get_prices(route: str):
    price_docs = list(prices_col.find({"route": route}, {"_id": 0, "date": 1, "price": 1, "airline": 1}))
    if not price_docs:  
        raise HTTPException(status_code=404, detail="Route not found")
    airline = price_docs[0]["airline"]
    price_history = [{"date": p["date"], "price": p["price"]} for p in price_docs]
    return PriceHistoryResponse(route=route, airline=airline, price_history=price_history)

@app.get("/api/search", response_model=list[SearchResult])
def hybrid_search(q: str, weight_text: float = 0.6, weight_recency: float = 0.3, weight_stability: float = 0.1):
    text_matches = list(flights_col.find({"$text": {"$search": q}}, {"score": {"$meta": "textScore"}}))
    if not text_matches:
        raise HTTPException(status_code=404, detail="No flights matched your query")

    results = []
    now = datetime.now()

    for f in text_matches:
        fid = str(f["_id"])
        flight_id = f["_id"]

        prices = list(prices_col.find({"flight_id": flight_id}).sort("date", 1))
        if not prices:
            continue

        last_date = prices[-1]["date"]
        recency = 1 / (1 + (now - last_date).days)

        price_values = [p["price"] for p in prices]
        if len(price_values) > 1:
            avg_price = sum(price_values) / len(price_values)
            variance = sum((p - avg_price) ** 2 for p in price_values) / len(price_values)
            stability = 1 / (1 + math.sqrt(variance))
        else:
            stability = 0.5

        score = (
            weight_text * f["score"] +
            weight_recency * recency +
            weight_stability * stability
        )

        results.append({
            "flight_id": fid,
            "route": f["route"],
            "airline": f["airline"],
            "score": round(score, 3)
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results
