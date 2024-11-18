from pydantic import BaseModel
import datetime


class LocationDataBase(BaseModel):
    device_id: str
    latitude: float
    longitude: float
    speed: float


class LocationDataCreate(LocationDataBase):
    pass


class LocationData(LocationDataBase):
    id: int
    timestamp: datetime.datetime

    class Config:
        orm_mode = True
