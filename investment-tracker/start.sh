#!/bin/bash

echo "🚀 Starting Investment Tracker..."
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "========================================"
echo "📱 ACCESS FROM YOUR IPHONE"
echo "========================================"
echo ""
echo "1. Make sure your iPhone is on the same WiFi network as this computer"
echo ""
echo "2. On your iPhone, open Safari and go to:"
echo ""

# Try to get the local IP address
if command -v hostname &> /dev/null; then
    LOCAL_IP=$(hostname -I | awk '{print $1}')
    if [ ! -z "$LOCAL_IP" ]; then
        echo "   http://${LOCAL_IP}:5000"
    else
        echo "   http://YOUR_COMPUTER_IP:5000"
    fi
else
    echo "   http://YOUR_COMPUTER_IP:5000"
fi

echo ""
echo "3. To find your computer's IP address, run:"
echo "   - Mac/Linux: hostname -I or ifconfig"
echo "   - Windows: ipconfig"
echo ""
echo "========================================"
echo ""
echo "Starting Flask server..."
echo "Press Ctrl+C to stop the server"
echo ""

cd backend
python app.py
