from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Literal

class FlightRequest(BaseModel):
    
    airline: str = Field(...,min_length = 2, max_length = 3, description = "IATA airline code")
    origin: str = Field(...,min_length = 3, max_length = 3, description = "IATA departure airport code")
    destination: str = Field(...,min_length = 3, max_length = 3, description = "IATA arrival airport code")
    scheduled_departure: datetime = Field(..., description = "Time departure")
    weather: Optional[Literal["clear","cloudy","rainy", "snowy", "stromy"]] = Field( default = "clear", description = "Meteo conditions")

class PredictionResponse(BaseModel):
    
    prediction: Literal["on_time", "delayed"]
    probability: float = Field(...,ge = 0.0, le = 1.0)
    estimated_delay_minutes: Optional[int] = Field(default = None, ge = 0)
    model_version: str = "v1.0.0"
    request_id: str
    timestamp: datetime