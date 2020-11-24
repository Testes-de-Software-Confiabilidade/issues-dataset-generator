import redis
import rq
import os
from dotenv import load_dotenv
from rq import Worker, Queue, Connection

load_dotenv()

# queue = rq.Queue(
# 	'redis-15795-db-0',
# 	connection=redis.Redis.from_url(os.environ.get("REDIS_URL", None))
# )
# job = queue.enqueue('example.example', 23)

listen = ['high', 'default', 'low']

redis_url = os.getenv('REDIS_URL', None)
conn = redis.from_url(redis_url)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()