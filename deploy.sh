#!/bin/bash

set -e

echo "🚀 Starting deployment..."

# Update & install dependencies
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv curl git

# Optional: install tmux for long sessions
sudo apt install -y tmux

# Set up virtual environment
echo "📦 Setting up Python environment..."
python3 -m venv stu
source stu/bin/activate
pip install --upgrade pip

# Install Python packages
pip install flask flask-cors requests gunicorn

# Clone your repo (or skip if already uploaded)
# git clone https://github.com/YOUR_USERNAME/Student_BIO.git
# cd Student_BIO

# Make sure app.py exists
if [ ! -f app.py ]; then
    echo "❌ Error: app.py not found in current directory."
    exit 1
fi

# Install Ollama
echo "🤖 Installing Ollama..."
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama in background
nohup ollama serve > ollama.log 2>&1 &
sleep 2

# Pull Gemma model
echo "📥 Pulling gemma3:1b..."
ollama run gemma3:1b || true  # Safe retry if already pulled

# Start Flask app using Gunicorn
echo "🔥 Launching app with Gunicorn..."
nohup gunicorn -b 0.0.0.0:5000 app:app > server.log 2>&1 &

echo "✅ Deployment complete. App should be live at:"
curl -s ifconfig.me | awk '{print "🌐 http://"$1":5000"}'
