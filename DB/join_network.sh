#!/bin/bash

# Load environment variables
set -a
source .env
set +a

# Check if required environment variables are set
if [ -z "$DB_ENGINE_PORT" ] || [ -z "$P2P_PORT" ] || [ -z "$KNOWN_PEERS" ]; then
    echo "Please set the required environment variables in the .env file:"
    echo "DB_ENGINE_PORT: The port for the database engine API"
    echo "P2P_PORT: The port for P2P communication"
    echo "KNOWN_PEERS: A comma-separated list of known peer addresses"
    exit 1
fi

# Pull the latest images
docker-compose pull

# Start the node
docker-compose up -d db_engine

# Wait for the service to be ready
echo "Waiting for the DB Engine to start..."
while ! curl -s http://localhost:$DB_ENGINE_PORT/peers > /dev/null; do
    sleep 1
done

echo "Node started successfully!"
echo "DB Engine API is available at http://localhost:$DB_ENGINE_PORT"
echo "P2P communication is running on port $P2P_PORT"

# Connect to known peers
IFS=',' read -ra PEER_ARRAY <<< "$KNOWN_PEERS"
for peer in "${PEER_ARRAY[@]}"; do
    echo "Connecting to peer: $peer"
    curl -X POST -H "Content-Type: application/json" -d "{\"peer_addr\":\"$peer\"}" http://localhost:$DB_ENGINE_PORT/peers/
done
# Run tests if the 'test' argument is provided
if [ "$1" = "test" ]; then
    echo "Running tests..."
    ./run_tests.sh
    exit $?
fi
echo "Node setup complete!"