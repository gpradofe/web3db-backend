#!/bin/bash

# Build and start the services
sudo docker-compose up -d

# Wait for services to be ready (you might need to adjust the sleep time)
sleep 10

# Run the tests
sudo docker-compose run --rm -e PYTHONPATH=/app db_engine_tests

# Stop and remove containers after tests
sudo docker-compose down --volumes --remove-orphans