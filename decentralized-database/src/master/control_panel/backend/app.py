from flask import Flask, jsonify, send_from_directory
import docker
import psutil
import uuid
import os

app = Flask(__name__, static_folder='../frontend/build')
client = docker.from_env()

def get_system_info():
    info = client.info()
    return {
        "containers": info["Containers"],
        "images": info["Images"],
        "memory": f"{info['MemTotal'] / (1024**3):.2f} GB",
        "cpus": info["NCPU"]
    }

def get_nodes():
    containers = client.containers.list()
    return [
        {
            "id": c.id,
            "name": c.name,
            "status": c.status,
            "cpu": c.stats(stream=False)['cpu_stats']['cpu_usage']['total_usage'],
            "memory": c.stats(stream=False)['memory_stats']['usage'] / (1024**2)
        }
        for c in containers
    ]

def get_bootstrap_id():
    return str(uuid.uuid4())

def get_active_queries():
    # Placeholder: Replace with actual query fetching logic
    return [
        {"sql": "SELECT * FROM users", "status": "running", "duration": 1500},
        {"sql": "INSERT INTO logs VALUES (...)", "status": "completed", "duration": 500}
    ]

@app.route('/api/system-info')
def api_system_info():
    return jsonify(get_system_info())

@app.route('/api/nodes')
def api_nodes():
    return jsonify(get_nodes())

@app.route('/api/bootstrap-id')
def api_bootstrap_id():
    return jsonify({"id": get_bootstrap_id()})

@app.route('/api/queries')
def api_queries():
    return jsonify(get_active_queries())

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)