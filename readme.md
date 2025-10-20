
Flight Price Tracker is a FastAPI + MongoDB project that tracks ticket prices over time and provides endpoints for flights, prices, and hybrid search.

Features:

* Stores flight details and price history in MongoDB.
* Generates dynamic price history for each flight, starting 6 months before departure.
* API endpoints:

  * List all flights
  * Get time-series price history for a route
  * Filter prices by year and month
  * Hybrid search with weighted scoring (text match, recency, stability)
* Swagger UI for interactive API testing.

Folder Structure:
flight_price_tracker/
├── main.py          # FastAPI app
├── models.py        # Pydantic models
├── database.py      # MongoDB connection and collections
├── seed.py          # Seed script to populate MongoDB
├── seed_data.json   # Sample flight data
├── README.md        # Project documentation

Requirements:

* Python 3.10+
* MongoDB running locally
* Python packages: fastapi, uvicorn, pymongo, pydantic
  Install packages:
  pip install fastapi uvicorn pymongo pydantic

API Endpoints:

1. Seed database
   POST /api/seed
   Response: {"message": "Database seeded successfully!"}

2. List all flights
   GET /api/flights
   Response example:
   [{"flight_id":"F1","route":"LHE->BKK","airline":"Thai Airways","departure_date":"2026-01-01T00:00:00"}, {"flight_id":"F2","route":"LHE->JED","airline":"Saudia","departure_date":"2026-02-10T00:00:00"}]

3. Get price history
   GET /api/prices?route=<ROUTE>&year=<YEAR>&month=<MONTH>
   Example: GET /api/prices?route=LHE->BKK&year=2025&month=11
   Response:
   {"route":"LHE->BKK","airline":"Thai Airways","price_history":[{"date":"2025-07-05T00:00:00","price":670},{"date":"2025-07-20T00:00:00","price":680}]}

4. Hybrid search
   GET /api/search?q=<QUERY>&weight_text=<float>&weight_recency=<float>&weight_stability=<float>
   Example: GET /api/search?q=LHE
   Response: [{"flight_id":"F1","route":"LHE->BKK","airline":"Thai Airways","score":0.83},{"flight_id":"F2","route":"LHE->JED","airline":"Saudia","score":0.81}]

Testing in Browser:

* Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) (interactive testing of all endpoints)
* Direct GET URLs:
  [http://127.0.0.1:8000/api/flights](http://127.0.0.1:8000/api/flights)
  [http://127.0.0.1:8000/api/prices?route=LHE->BKK](http://127.0.0.1:8000/api/prices?route=LHE->BKK)
  [http://127.0.0.1:8000/api/search?q=LHE](http://127.0.0.1:8000/api/search?q=LHE)

Notes:

* Prices are randomly generated each time you seed, simulating realistic changes.
* Prices start 6 months before flight departure.
* Collections in MongoDB:

  * flightRecord → flight info
  * price_history → price time-series
