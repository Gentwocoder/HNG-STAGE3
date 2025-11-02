"""
Message routes for direct message sending (REST API).
"""

import logging
from fastapi import APIRouter, HTTPException
from app.models.schemas import MessageResponse, ActionResponse
from app.services import get_telex_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/messages", tags=["messages"])


@router.post("/send", response_model=ActionResponse)
async def send_message(message: MessageResponse):
    """
    Send a message via the Telex.im API.
    
    This endpoint allows sending messages directly to users or chats.
    """
    try:
        logger.info(f"Sending message to chat {message.chat_id}")
        
        telex_service = get_telex_service()
        result = await telex_service.send_message(message)
        
        return ActionResponse(
            success=True,
            message="Message sent successfully",
            data=result
        )
    
    except Exception as e:
        logger.error(f"Error sending message: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to send message: {str(e)}"
        )


@router.post("/broadcast")
async def broadcast_message(chat_ids: list[str], text: str):
    """
    Broadcast a message to multiple chats.
    
    Args:
        chat_ids: List of chat IDs to send message to
        text: Message text to broadcast
    """
    try:
        logger.info(f"Broadcasting message to {len(chat_ids)} chats")
        
        telex_service = get_telex_service()
        results = []
        errors = []
        
        for chat_id in chat_ids:
            try:
                result = await telex_service.send_text_message(chat_id, text)
                results.append({"chat_id": chat_id, "success": True, "result": result})
            except Exception as e:
                errors.append({"chat_id": chat_id, "error": str(e)})
                logger.error(f"Failed to send to {chat_id}: {str(e)}")
        
        return ActionResponse(
            success=len(errors) == 0,
            message=f"Broadcast completed: {len(results)} successful, {len(errors)} failed",
            data={
                "successful": results,
                "failed": errors,
                "total": len(chat_ids)
            }
        )
    
    except Exception as e:
        logger.error(f"Error broadcasting message: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to broadcast message: {str(e)}"
        )
