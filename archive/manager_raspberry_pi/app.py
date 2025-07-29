import redis
import json
import time

r = redis.Redis(host='redis', port=6379, db=0)

# Tworzymy 10 zadań
for i in range(10):
    task = {'id': i, 'number': i + 1}
    r.lpush('task_queue', json.dumps(task))
    print(f"[Manager] Wysłano zadanie: {task}")
    time.sleep(0.5)