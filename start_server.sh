#!/bin/bash

echo "Starting Centralized Allure Reports Server..."
echo

# Check if .env exists
if [ ! -f .env ]; then
    echo "Warning: .env file not found!"
    echo "Please copy .env.example to .env and configure your AWS credentials."
    echo
    exit 1
fi

# Start the server
python app.py
