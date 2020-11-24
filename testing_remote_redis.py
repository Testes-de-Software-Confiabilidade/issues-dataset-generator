import redis
import rq
import os
from dotenv import load_dotenv
from rq import Worker, Queue, Connection

load_dotenv()

listen = ['reliability-tasks']


redis_url = os.getenv('REDIS_URL', None)
# conn = redis.from_url(redis_url)
conn = redis.Redis(
	host='ec2-54-196-49-146.compute-1.amazonaws.com',
	port=7759,
	password='p99811caf28e7bba396308430818e8ee491725c3be79bd40f220dbc15a7bfc54f',
)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()