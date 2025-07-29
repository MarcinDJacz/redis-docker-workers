from flask import Flask, request, jsonify
import requests
import time
time.sleep(5)
app = Flask(__name__)

@app.route('/task', methods=['POST'])
def task():
    data = request.json
    number = data['number']
    operations = data['operations']
    worker_name = data['worker']
    print(f"Working on number {number} for {operations} times")

    for _ in range(operations):
        number = number + 2

    # Send result back to manager
    requests.post("http://manager_raspberry_pi:5000/result",
                  json={
                  'result': number,
                  'worker': worker_name})
    return jsonify({"status": "done"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
