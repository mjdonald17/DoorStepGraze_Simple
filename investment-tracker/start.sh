#!/bin/bash

echo "🚀 Starting Investment Tracker..."
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "Starting Flask server..."
echo "Access the app at: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

cd backend
python app.py
