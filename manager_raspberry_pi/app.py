import random
import requests
import time
import threading
from flask import Flask, request, jsonify
import redis

app = Flask(__name__)

# Stan aktywnych tasków
pending_tasks = {
    "pc_worker": False,
    "laptop_worker": False
}

@app.route('/result', methods=['POST'])
def receive_result():
    data = request.json
    worker = data.get("worker")
    print(f"Received result from {worker}: {data}")

    # Oznacz, że worker skończył
    pending_tasks[worker] = False

    # Zapisz wynik
    with open("results/output.txt", "a") as f:
        f.write(str(data) + "\n")
    return jsonify({"status": "ok"})

def send_task(worker, number, operations):
    payload = {'number': number, 'operations': operations, 'worker': worker}
    try:
        r = requests.post(f"http://{worker}:5000/task", json=payload)
        if r.ok:
            pending_tasks[worker] = True
            print(f"Sent task to {worker}")
        else:
            print(f"Failed to send task to {worker}: {r.status_code}")
    except Exception as e:
        print(f"Error sending task to {worker}: {e}")

def task_manager_loop():
    time.sleep(5)  # poczekaj na start
    while True:
        for worker in pending_tasks:
            if not pending_tasks[worker]:
                number = random.randint(2, 20)
                operations = random.randint(5, 15)
                send_task(worker, number, operations)
        time.sleep(1)  # co sekundę sprawdź status workerów

if __name__ == "__main__":
    threading.Thread(target=task_manager_loop, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)
