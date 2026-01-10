from pydantic import BaseModel

class PredictInput(BaseModel):
    Population: float
    Latitude: float
    Longitude: float