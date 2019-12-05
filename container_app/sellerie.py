from celery import Celery

app = Celery('container_app',
                broker='amqp://admin:mypass@rabbit:5672', backend='rpc://',
                include=['container_app.tasks'],
                broker_heartbeat=0)
