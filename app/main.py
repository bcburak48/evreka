from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app import schemas
from database.database import SessionLocal, engine, get_db
from database import models
from celery_app.tasks import process_data


@asynccontextmanager
async def lifespan(app: FastAPI):
    models.Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/data")
async def receive_data(data: schemas.LocationDataCreate):
    # Send data to Celery for asynchronous processing
    process_data.delay(data.dict())
    return {"message": "Data received"}


@app.get("/data")
def get_data(start_date: str, end_date: str, db: Session = Depends(get_db)):
    # Retrieve data within date range
    data = db.query(models.LocationData).filter(
        models.LocationData.timestamp.between(start_date, end_date)
    ).all()
    return data


@app.get("/data/latest/{device_id}")
def get_latest_data(device_id: str, db: Session = Depends(get_db)):
    # Retrieve the latest data for a device
    data = db.query(models.LocationData).filter_by(device_id=device_id).order_by(
        models.LocationData.timestamp.desc()
    ).first()
    return data
