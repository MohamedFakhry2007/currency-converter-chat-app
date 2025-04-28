"""Currency conversion service module."""
import asyncio
from typing import List, Dict, Any, Optional

import aiohttp
from loguru import logger

import config

async def convert_currency(amount: float, base_currency: str, target_currency: str) -> float:
    """
    Convert an amount from one currency to another.
    
    Args:
        amount: The amount to convert
        base_currency: The base/source currency code (e.g., USD)
        target_currency: The target currency code (e.g., EUR)
        
    Returns:
        The converted amount
        
    Raises:
        ValueError: If the conversion fails
    """
    logger.info(f"Converting {amount} {base_currency} to {target_currency}")
    
    # Ensure currency codes are lowercase for API
    base_currency_lower = base_currency.lower()
    target_currency_lower = target_currency.lower()
    
    # Format the URLs
    urls = [url.format(base=base_currency_lower) for url in config.CURRENCY_API_URLS]
    
    async with aiohttp.ClientSession() as session:
        for url in urls:
            try:
                logger.debug(f"Fetching exchange rate from: {url}")
                async with session.get(url, timeout=5) as resp:
                    resp.raise_for_status()
                    data = await resp.json()
                    
                    # Check if the response contains the expected data structure
                    if base_currency_lower not in data:
                        logger.warning(f"Invalid API response: base currency '{base_currency_lower}' not in response")
                        logger.debug(f"Response data keys: {list(data.keys())}")
                        continue
                        
                    if target_currency_lower not in data[base_currency_lower]:
                        logger.warning(f"Target currency '{target_currency_lower}' not found in response for {base_currency_lower}")
                        logger.debug(f"Available target currencies: {list(data[base_currency_lower].keys())[:10]}...")
                        continue
                    
                    # Extract the exchange rate
                    rate = data[base_currency_lower][target_currency_lower]
                    logger.info(f"Exchange rate found: 1 {base_currency} = {rate} {target_currency}")
                    
                    # Calculate and return the result
                    result = round(amount * rate, 2)
                    logger.info(f"Conversion result: {amount} {base_currency} = {result} {target_currency}")
                    return result
                    
            except Exception as e:
                logger.error(f"Failed to fetch from {url}: {str(e)}")
    
    # If we get here, all sources failed
    raise ValueError(f"جميع مصادر أسعار الصرف فشلت للتحويل من {base_currency} إلى {target_currency}")

async def get_popular_currencies() -> List[Dict[str, str]]:
    """
    Get a list of popular currencies.
    
    Returns:
        List of popular currencies with code and name
    """
    return [
        {"code": "USD", "name": "دولار أمريكي", "symbol": "$"},
        {"code": "EUR", "name": "يورو", "symbol": "€"},
        {"code": "GBP", "name": "جنيه إسترليني", "symbol": "£"},
        {"code": "EGP", "name": "جنيه مصري", "symbol": "ج.م"},
        {"code": "SAR", "name": "ريال سعودي", "symbol": "ر.س"},
        {"code": "AED", "name": "درهم إماراتي", "symbol": "د.إ"},
        {"code": "KWD", "name": "دينار كويتي", "symbol": "د.ك"},
        {"code": "JPY", "name": "ين ياباني", "symbol": "¥"},
        {"code": "CNY", "name": "يوان صيني", "symbol": "¥"},
        {"code": "CAD", "name": "دولار كندي", "symbol": "C$"}
    ]