import redis
import json
import time

r = redis.Redis(host='redis', port=6379, db=0)

print("[Worker] Czeka na zadania...")

while True:
    task_data = r.rpop('task_queue')
    if task_data:
        task = json.loads(task_data)
        number = task['number']
        task_id = task['id']
        result = number ** 2
        r.rpush('result_queue', json.dumps({"id": task_id, "result": result}))
        print(f"[Worker] Zadanie #{task['id']}: {number}^2 = {result}")
        time.sleep(1)  # symulacja pracy
    else:
        time.sleep(0.5)