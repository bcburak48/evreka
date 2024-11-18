from celery import Celery

celery_app = Celery(
    'celery_app',
    broker='amqp://guest@rabbitmq//',
    backend='rpc://'
)

celery_app.conf.update(
    result_expires=3600,
)
