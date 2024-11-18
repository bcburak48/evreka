from celery import Celery
from sqlalchemy.orm import Session
from database.database import SessionLocal
from database import models

app = Celery("tasks", broker="amqp://guest@rabbitmq//")

@app.task
def process_data(data):
    try:
        data.pop('timestamp', None)

        db: Session = SessionLocal()
        location_data = models.LocationData(**data)
        db.add(location_data)
        db.commit()
        db.refresh(location_data)
        db.close()
    except Exception as e:
        print(f"Error processing data: {e}")
