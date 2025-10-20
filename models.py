from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class PricePoint(BaseModel):
    date: datetime
    price: float


class Flight(BaseModel):
    route: str
    airline: str
    departure_date: datetime
    interval_days: int


class FlightResponse(BaseModel):
    flight_id: str
    route: str
    airline: str
    departure_date: datetime


class PriceHistoryResponse(BaseModel):
    route: str
    airline: str
    price_history: List[PricePoint]


class SearchResult(BaseModel):
    flight_id: str
    route: str
    airline: str
    score: float
