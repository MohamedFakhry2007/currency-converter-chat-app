## Currency Converter Chatbot
Smart conversation for currency conversion in Arabic using AI technology from Google Gemini.

# Project Description
This application provides a conversational interface that allows users to convert between different currencies using natural language in Arabic. The application relies on:

Flask web interface
Google Gemini AI API
Real-time currency conversion data

# Basic Requirements
Python 3.11 or later
Poetry for managing dependencies
API key for Google Gemini

# Setup Instructions
Clone the repository:

bash
git clone https://github.com/MohamedFakhry2007/currency-converter-chat-app.git

Copy .env.example and make .env file

Add your API key in the .env file:

Run the setup script:

bash
 bash setup.sh

# How to Use

After running the application, you can:

Use the chat interface to enter currency conversion queries in Arabic, such as:
"Convert 100 dollars to euros"
“How much is 50 Egyptian pounds worth in US dollars?”
“I have 200 euros, how much is it worth in Egyptian pounds?”

# Development
The project uses Poetry to manage dependencies.
The code is organized into separate modules for easy maintenance.
It employs asynchronous programming for optimal performance.