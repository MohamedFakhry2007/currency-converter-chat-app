# Currency Converter App Setup Script
echo "Setting up Currency Converter App..."

# Check if Poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "Poetry is not installed. Installing Poetry..."
    curl -sSL https://install.python-poetry.org | python3 -
fi

# Install dependencies
echo "Installing dependencies..."
poetry install

# Create logs directory if it doesn't exist
mkdir -p logs

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Creating .env file..."
    echo "GEMINI_API_KEY=your_api_key_here" > .env
    echo "Please update .env with your Gemini API key before running the app."
fi

# Run the app
echo "Starting Currency Converter App..."
poetry run python -m app.main

echo "Setup complete!"