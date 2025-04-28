"""Define application routes."""
import asyncio
from flask import Blueprint, render_template, request, jsonify
from loguru import logger

from app.modules.currency_service import convert_currency
from app.modules.gemini_client import process_user_message


def register_routes(app):
    """Register routes with the Flask application."""
    
    @app.route("/")
    def index():
        """Render the main chat interface."""
        return render_template("index.html")
    
    @app.route("/api/chat", methods=["POST"])
    async def chat():
        """Process a chat message and return a response."""
        try:
            data = request.json
            user_message = data.get("message", "")
            
            if not user_message:
                return jsonify({"error": "No message provided"}), 400
            
            logger.info(f"Received chat message: {user_message}")
            
            # Process the message with Gemini
            response = await process_user_message(user_message)
            
            return jsonify({"response": response})
            
        except Exception as e:
            logger.error(f"Error processing chat: {str(e)}")
            return jsonify({"error": f"Failed to process message: {str(e)}"}), 500
    
    @app.route("/api/convert", methods=["POST"])
    async def convert():
        """Convert currency directly from API."""
        try:
            data = request.json
            amount = float(data.get("amount", 0))
            base_currency = data.get("base_currency", "").upper()
            target_currency = data.get("target_currency", "").upper()
            
            if not amount or not base_currency or not target_currency:
                return jsonify({"error": "Missing required parameters"}), 400
            
            logger.info(f"Converting {amount} {base_currency} to {target_currency}")
            
            # Perform the conversion
            result = await convert_currency(amount, base_currency, target_currency)
            
            return jsonify({
                "amount": amount,
                "base_currency": base_currency,
                "target_currency": target_currency,
                "result": result
            })
            
        except Exception as e:
            logger.error(f"Error converting currency: {str(e)}")
            return jsonify({"error": f"Failed to convert currency: {str(e)}"}), 500
    
    @app.errorhandler(404)
    def page_not_found(e):
        """Handle 404 errors."""
        return render_template("error.html", error="الصفحة غير موجودة"), 404
    
    @app.errorhandler(500)
    def server_error(e):
        """Handle 500 errors."""
        return render_template("error.html", error="حدث خطأ في الخادم"), 500