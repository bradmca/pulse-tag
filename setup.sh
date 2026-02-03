#!/bin/bash

# PulseTag Setup Script
echo "🚀 Setting up PulseTag..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f "backend/.env" ]; then
    echo "📝 Creating .env file..."
    cp backend/.env.example backend/.env
    echo "✅ Please edit backend/.env with your OpenRouter API key"
    echo "   Get your free key at: https://openrouter.ai/keys"
fi

# Build and start the application
echo "🐳 Building and starting containers..."
docker-compose up --build -d

echo "✅ PulseTag is now running!"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "📝 Don't forget to add your OpenRouter API key to backend/.env!"
