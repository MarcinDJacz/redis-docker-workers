import redis, json, time

r = redis.Redis(host='redis', port=6379)

# zadania
tasks = [{"id": 1, "number": 2, "operations": 5}, {"id": 2, "number": 4, "operations": 3}, {"id": 2, "number": 12, "operations": 44}]

# wrzuć zadania
for task in tasks:
    r.lpush('task_queue', json.dumps(task))

# odbiór wyników
for _ in range(len(tasks)):
    _, result = r.brpop('result_queue')
    print("Got result:", json.loads(result))