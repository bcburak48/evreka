import datetime

from click import DateTime

from . import Base
from sqlalchemy import Column, Integer, String


class LocationData(Base):
    __tablename__ = 'location_data'
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String)
    latitude = Column(String)
    longitude = Column(String)
    speed = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)