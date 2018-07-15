from celery import Celery
from microlab.settings import AMPQ_PASS


app = Celery(
    'tasks',
    broker='pyamqp://microlab:%s@localhost:5672/microlab' % AMPQ_PASS
)


@app.task
def add(x, y):
        return x + y

