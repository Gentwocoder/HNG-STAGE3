"""
Telex.im integration service for sending messages and handling API calls.
"""

import logging
import httpx
from typing import Optional, Dict, Any
from app.core.config import settings
from app.models.schemas import MessageResponse

logger = logging.getLogger(__name__)


class TelexService:
    """Service for interacting with Telex.im API."""
    
    def __init__(self):
        """Initialize the Telex service."""
        self.api_url = settings.telex_api_url
        self.api_key = settings.telex_api_key
        self.bot_id = settings.telex_bot_id
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def send_message(self, message_response: MessageResponse) -> Dict[str, Any]:
        """
        Send a message through Telex.im API.
        
        Args:
            message_response: MessageResponse object with message details
            
        Returns:
            API response as dict
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_url}/messages",
                    json=message_response.model_dump(exclude_none=True),
                    headers=self.headers,
                    timeout=10.0
                )
                
                response.raise_for_status()
                result = response.json()
                
                logger.info(f"Message sent successfully to chat {message_response.chat_id}")
                return result
                
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error sending message: {e.response.status_code} - {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"Error sending message: {str(e)}")
            raise
    
    async def send_text_message(
        self, 
        chat_id: str, 
        text: str, 
        reply_to_message_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Send a simple text message.
        
        Args:
            chat_id: Chat ID to send message to
            text: Message text
            reply_to_message_id: Optional message ID to reply to
            
        Returns:
            API response as dict
        """
        message = MessageResponse(
            chat_id=chat_id,
            text=text,
            reply_to_message_id=reply_to_message_id
        )
        
        return await self.send_message(message)
    
    async def send_typing_action(self, chat_id: str) -> None:
        """
        Send typing indicator to show the bot is processing.
        
        Args:
            chat_id: Chat ID to send typing indicator to
        """
        try:
            async with httpx.AsyncClient() as client:
                await client.post(
                    f"{self.api_url}/actions",
                    json={"chat_id": chat_id, "action": "typing"},
                    headers=self.headers,
                    timeout=5.0
                )
                logger.debug(f"Typing indicator sent to chat {chat_id}")
        except Exception as e:
            # Don't fail if typing indicator fails
            logger.warning(f"Failed to send typing indicator: {str(e)}")
    
    def validate_webhook_signature(self, payload: str, signature: str) -> bool:
        """
        Validate webhook signature from Telex.im.
        
        Args:
            payload: Raw request payload
            signature: Signature from webhook headers
            
        Returns:
            True if valid, False otherwise
        """
        # Implement signature validation based on Telex.im's specification
        # This is a placeholder - adjust based on actual Telex.im webhook security
        import hmac
        import hashlib
        
        if not settings.telex_webhook_secret:
            logger.warning("Webhook secret not configured, skipping validation")
            return True
        
        try:
            expected_signature = hmac.new(
                settings.telex_webhook_secret.encode(),
                payload.encode(),
                hashlib.sha256
            ).hexdigest()
            
            return hmac.compare_digest(signature, expected_signature)
        except Exception as e:
            logger.error(f"Error validating webhook signature: {str(e)}")
            return False


# Global service instance
_telex_service: Optional[TelexService] = None


def get_telex_service() -> TelexService:
    """
    Get or create the global Telex service instance.
    
    Returns:
        TelexService instance
    """
    global _telex_service
    if _telex_service is None:
        _telex_service = TelexService()
    return _telex_service
