"""Google Gemini API client module for natural language processing."""
import asyncio
import json
from typing import Dict, Any, Optional

import google.generativeai as genai
from loguru import logger

import config
from app.modules.currency_service import convert_currency

# Configure Gemini API
genai.configure(api_key=config.GEMINI_API_KEY)

# Function declarations for Gemini
FUNCTION_DECLARATIONS = [
    {
        "name": "convert_currency",
        "description": "تحويل مبلغ من عملة إلى عملة أخرى باستخدام رموز العملات القياسية ثلاثية الأحرف.",
        "parameters": {
            "type": "object",
            "properties": {
                "amount": {
                    "type": "number", 
                    "description": "المبلغ المراد تحويله"
                },
                "base_currency": {
                    "type": "string", 
                    "description": "رمز العملة الأصلية (مثل USD, EUR, EGP للجنيه المصري, GBP للجنيه البريطاني)"
                },
                "target_currency": {
                    "type": "string", 
                    "description": "رمز العملة المستهدفة (مثل EUR, USD, JPY)"
                }
            },
            "required": ["amount", "base_currency", "target_currency"]
        }
    }
]

# System instruction for Gemini
SYSTEM_INSTRUCTION = """
أنت مساعد محادثة متخصص في تحويل العملات. يجب عليك الرد باللغة العربية بشكل طبيعي وودود.

لأي طلب، قم بتحديد هذه المكونات الثلاثة:
1. المبلغ المراد تحويله
2. العملة الأصلية (استخدم الرموز القياسية ثلاثية الأحرف)
3. العملة المستهدفة (استخدم الرموز القياسية ثلاثية الأحرف)

استخدم دائمًا رموز العملات القياسية ثلاثية الأحرف في استدعاء الدالة convert_currency:
- USD للدولار الأمريكي
- EUR لليورو
- GBP للجنيه البريطاني
- EGP للجنيه المصري
- JPY للين الياباني
(إلخ.)

أمثلة على المدخلات واستدعاءات الدالة المتوقعة:
1. "حول 100 دولار إلى يورو" → convert_currency(amount=100, base_currency="USD", target_currency="EUR")
2. "كم يساوي 50 يورو بالين الياباني؟" → convert_currency(amount=50, base_currency="EUR", target_currency="JPY")
3. "حول 100 جنيه إلى دولار أمريكي" → convert_currency(amount=100, base_currency="EGP", target_currency="USD")
4. "معايا 50 دولار، بيساووا كام بالجنيه؟" → convert_currency(amount=50, base_currency="USD", target_currency="EGP")

تذكر أن تكون ودودًا ومحترفًا في ردودك، وقدم معلومات مساعدة حول تحويل العملات عند الحاجة.
"""

# Create a class to manage Gemini chat sessions
class GeminiChat:
    """Manages a Gemini chat session for currency conversion."""
    
    def __init__(self):
        """Initialize a new Gemini chat session."""
        try:
            self.model = genai.GenerativeModel(
                model_name=config.GEMINI_MODEL,
                tools=[{"function_declarations": FUNCTION_DECLARATIONS}],
                system_instruction=SYSTEM_INSTRUCTION
            )
            self.chat = self.model.start_chat()
            logger.info("Gemini chat session initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini chat: {str(e)}")
            raise
    
    async def send_message(self, message: str) -> Dict[str, Any]:
        """
        Send a message to the Gemini model and process the response.
        
        Args:
            message: The user's message
            
        Returns:
            Dictionary containing the response text and any additional data
        """
        try:
            logger.debug(f"Sending message to Gemini: {message}")
            response = self.chat.send_message(message)
            
            # --- Add detailed logging here ---
            logger.debug(f"Raw Gemini Response Object: {response}")
            try:
                # Log the parts if they exist
                logger.debug(f"Gemini Response Parts: {response.candidates[0].content.parts}")
            except (AttributeError, IndexError):
                logger.debug("Gemini Response has no parts or candidates.")
            # --- End of added logging ---
            
            logger.debug(f"Received response from Gemini")
            
            # Check for function calls
            # Use .parts[-1] to check the latest part for a function call
            latest_part = response.candidates[0].content.parts[-1]
            if hasattr(latest_part, 'function_call') and latest_part.function_call:
                 logger.info("Function call detected in the latest part.")
                 return await self._handle_function_call(latest_part.function_call, message)

            
            # If no function call in the latest part, return the text response
            logger.info("No function call detected. Returning text response.")
            return {"text": response.text, "type": "text"}
            
        except Exception as e:
            logger.error(f"Error sending message to Gemini: {str(e)}")
            # Also log the exception traceback for more details
            logger.exception("Exception details:") 
            return {"text": "عذراً، حدث خطأ أثناء معالجة طلبك. يرجى المحاولة مرة أخرى.", "type": "error"}
    
    async def _handle_function_call(self, function_call, original_message: str) -> Dict[str, Any]:
        """
        Handle a function call from Gemini.
        
        Args:
            function_call: The function call object from Gemini
            original_message: The original user message
            
        Returns:
            Dictionary containing the response data
        """
        func_name = function_call.name
        args = function_call.args
        
        logger.info(f"Function call detected: {func_name} with args {args}")
        
        if func_name == "convert_currency":
            try:
                # Extract parameters
                amount = float(args.get("amount", 0))
                base_currency = args.get("base_currency", "").upper()
                target_currency = args.get("target_currency", "").upper()
                
                if not amount or not base_currency or not target_currency:
                    raise ValueError(f"Missing required parameters for currency conversion")
                
                # Perform the conversion
                result = await convert_currency(amount, base_currency, target_currency)
                
                # Format the result for the user
                result_prompt = f"""
                نتيجة التحويل هي:
                {amount} {base_currency} = {result} {target_currency}
                
                يرجى الرد على المستخدم باللغة العربية، مع دمج هذه النتيجة بشكل طبيعي.
                استفسار المستخدم الأصلي: {original_message}
                """
                
                final_response = self.chat.send_message(result_prompt)
                return {
                    "text": final_response.text,
                    "type": "conversion",
                    "data": {
                        "amount": amount,
                        "base_currency": base_currency,
                        "target_currency": target_currency,
                        "result": result
                    }
                }
                
            except Exception as e:
                logger.error(f"Error during currency conversion: {str(e)}")
                error_prompt = f"""
                حدث خطأ أثناء التحويل: {str(e)}
                يرجى إبلاغ المستخدم باللغة العربية أن هناك مشكلة في تحويل العملة.
                استفسار المستخدم الأصلي: {original_message}
                """
                error_response = self.chat.send_message(error_prompt)
                return {"text": error_response.text, "type": "error"}
        else:
            logger.warning(f"Unknown function call: {func_name}")
            return {"text": "عذراً، لا يمكنني معالجة هذا النوع من الطلبات.", "type": "error"}

# Create a global chat session
_gemini_chat = None

async def get_gemini_chat() -> GeminiChat:
    """Get or create a Gemini chat session."""
    global _gemini_chat
    if _gemini_chat is None:
        _gemini_chat = GeminiChat()
    return _gemini_chat

async def process_user_message(message: str) -> Dict[str, Any]:
    """
    Process a user message using the Gemini API.
    
    Args:
        message: The user's message
        
    Returns:
        Dictionary containing the response
    """
    try:
        chat = await get_gemini_chat()
        return await chat.send_message(message)
    except Exception as e:
        logger.error(f"Error processing user message: {str(e)}")
        return {"text": "عذراً، حدث خطأ أثناء معالجة طلبك. يرجى المحاولة مرة أخرى.", "type": "error"}
