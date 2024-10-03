from flask import Flask, render_template, jsonify
import docker

app = Flask(__name__)
client = docker.from_env()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/nodes')
def get_nodes():
    nodes = []
    for container in client.containers.list():
        if 'node-worker' in container.name or 'node-master' in container.name:
            nodes.append({
                'id': container.id[:12],
                'name': container.name,
                'status': container.status
            })
    return jsonify(nodes)

@app.route('/api/start_worker')
def start_worker():
    try:
        client.containers.run('decentralized-db:latest', 
                              command='/bin/bash -c "/app/scripts/init_node.sh worker && /app/scripts/join_network.sh && python /app/worker/worker.py"',
                              detach=True,
                              name=f'node-worker-{len(client.containers.list())+1}',
                              network='decentralized-db-network')
        return jsonify({'status': 'success', 'message': 'Worker node started'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)