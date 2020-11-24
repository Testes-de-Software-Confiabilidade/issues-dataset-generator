import redis
import rq
import os
from dotenv import load_dotenv
from rq import Worker, Queue, Connection

load_dotenv()

listen = ['reliability-tasks']

redis_url = os.getenv('REDIS_URL', None)
conn = redis.from_url(redis_url)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()