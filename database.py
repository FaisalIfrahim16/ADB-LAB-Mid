from pymongo import MongoClient

MONGO_URL = "mongodb://localhost:27017"
DB_NAME = "flightDB"            

client = MongoClient(MONGO_URL)
db = client[DB_NAME]

flights_col = db["flightRecord"]  
prices_col = db["price_history"]  


col = list(flights_col.find(
    {},
    {
        '_id':0
    }
).limit(5))

print(col)