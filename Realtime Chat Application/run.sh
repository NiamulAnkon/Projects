#!/bin/bash

echo "Starting the Chat Server..."
python3 Server/server.py &

sleep 2  # Wait for the server to start

echo "Starting the Chat Client..."
python3 Client/main.py
