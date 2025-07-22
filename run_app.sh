#!/bin/bash

echo "Installing dependencies..."
pip install -r package_requirements.txt

echo "Starting Sharpy Educational App..."
streamlit run app.py --server.port 5000