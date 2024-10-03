#!/bin/bash

NODE_TYPE=$1

if [ "$NODE_TYPE" != "master" ] && [ "$NODE_TYPE" != "worker" ]; then
    echo "Usage: $0 [master|worker]"
    exit 1
fi

# Set up common configurations
cp /config/node.conf /app/node.conf

if [ "$NODE_TYPE" == "master" ]; then
    # Master-specific setup
    ipfs init
    ipfs config Addresses.API /ip4/0.0.0.0/tcp/5001
    ipfs config Addresses.Gateway /ip4/0.0.0.0/tcp/8080
else
    # Worker-specific setup
    echo "Setting up worker node..."
fi

echo "Node initialization complete."