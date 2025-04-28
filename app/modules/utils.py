"""Utility functions for the Currency Converter application."""
from typing import Dict, Any, Optional, List

import config

def identify_currencies_from_text(text: str) -> Dict[str, Optional[str]]:
    """
    Try to identify currencies mentioned in a text.
    
    Args:
        text: The text to analyze
        
    Returns:
        Dictionary with potential base and target currencies
    """
    text_lower = text.lower()
    result = {"base_currency": None, "target_currency": None}
    
    # Check for each currency in the mapping
    currencies_found = []
    for term, code in config.CURRENCY_MAPPING.items():
        if term in text_lower:
            currencies_found.append(code)
    
    # If we found at least two currencies, assume the first is base and second is target
    if len(currencies_found) >= 2:
        result["base_currency"] = currencies_found[0]
        result["target_currency"] = currencies_found[1]
    elif len(currencies_found) == 1:
        # If only one currency is found, assume it's the base and leave target as None
        result["base_currency"] = currencies_found[0]
    
    return result

def format_currency(amount: float, currency_code: str) -> str:
    """
    Format a currency amount with the appropriate symbol.
    
    Args:
        amount: The amount to format
        currency_code: The currency code (e.g., USD)
        
    Returns:
        Formatted currency string
    """
    symbols = {
        "USD": "$", "EUR": "€", "GBP": "£", "JPY": "¥",
        "EGP": "ج.م", "SAR": "ر.س", "AED": "د.إ", "KWD": "د.ك"
    }
    
    symbol = symbols.get(currency_code, currency_code)
    
    # Format with two decimal places for most currencies
    if currency_code == "JPY":
        # JPY typically doesn't use decimal places
        formatted_amount = f"{int(amount):,}"
    else:
        formatted_amount = f"{amount:,.2f}"
    
    # For Arabic currencies, place the symbol at the end
    arabic_currencies = ["EGP", "SAR", "AED", "KWD"]
    if currency_code in arabic_currencies:
        return f"{formatted_amount} {symbol}"
    else:
        return f"{symbol}{formatted_amount}"