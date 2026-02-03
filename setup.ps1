# PulseTag Setup Script for PowerShell
Write-Host "🚀 Setting up PulseTag..." -ForegroundColor Green

# Check if Docker is installed
try {
    docker --version | Out-Null
} catch {
    Write-Host "❌ Docker is not installed. Please install Docker first." -ForegroundColor Red
    exit 1
}

# Check if Docker Compose is installed
try {
    docker-compose --version | Out-Null
} catch {
    Write-Host "❌ Docker Compose is not installed. Please install Docker Compose first." -ForegroundColor Red
    exit 1
}

# Create .env file if it doesn't exist
if (-not (Test-Path "backend\.env")) {
    Write-Host "📝 Creating .env file..." -ForegroundColor Yellow
    Copy-Item "backend\.env.example" "backend\.env"
    Write-Host "✅ Please edit backend\.env with your OpenRouter API key" -ForegroundColor Green
    Write-Host "   Get your free key at: https://openrouter.ai/keys" -ForegroundColor Cyan
}

# Build and start the application
Write-Host "🐳 Building and starting containers..." -ForegroundColor Yellow
docker-compose up --build -d

Write-Host "✅ PulseTag is now running!" -ForegroundColor Green
Write-Host "   Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host "   Backend API: http://localhost:8000" -ForegroundColor Cyan
Write-Host "   API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "📝 Don't forget to add your OpenRouter API key to backend\.env!" -ForegroundColor Yellow
