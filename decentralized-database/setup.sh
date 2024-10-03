#!/bin/bash

# Function to check system requirements
check_system_requirements() {
    echo "Checking system requirements..."
    
    # Check if Docker is installed
    if ! command -v docker &> /dev/null; then
        echo "Docker is not installed. Please install Docker and try again."
        exit 1
    fi
    
    # Check if Docker Compose is installed
    if ! command -v docker-compose &> /dev/null; then
        echo "Docker Compose is not installed. Please install Docker Compose and try again."
        exit 1
    fi
    
    echo "System requirements met."
}

# Function to prompt for configuration
prompt_configuration() {
    echo "Configuring node..."
    
    # Prompt for node type
    while true; do
        read -p "Enter node type (master/worker): " NODE_TYPE
        case $NODE_TYPE in
            master|worker) break;;
            *) echo "Please enter 'master' or 'worker'.";;
        esac
    done
    
    # Prompt for network information
    read -p "Enter network name: " NETWORK_NAME
    read -p "Enter bootstrap node address (or press enter to create a new network): " BOOTSTRAP_NODE
    
    # Save configuration to .env file
    echo "NODE_TYPE=$NODE_TYPE" > .env
    echo "NETWORK_NAME=$NETWORK_NAME" >> .env
    echo "BOOTSTRAP_NODE=$BOOTSTRAP_NODE" >> .env
    
    echo "Configuration saved."
}

# Function to pull Docker images
pull_docker_images() {
    echo "Pulling necessary Docker images..."
    
    docker pull ipfs/go-ipfs:latest
    docker pull apache/hadoop:3
    docker pull bitnami/spark:latest
    docker pull apache/hive:3.1.3
    
    echo "Docker images pulled successfully."
}

# Main script execution
echo "Decentralized Database Setup"
check_system_requirements
prompt_configuration
pull_docker_images

echo "Setup completed successfully."
echo "To start the node, run: docker-compose up -d"
