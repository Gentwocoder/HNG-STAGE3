"""
Webhook routes for handling Telex.im events and messages.
"""

import logging
from fastapi import APIRouter, Request, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from app.models.schemas import WebhookEvent, EventType, ActionResponse, ErrorResponse
from app.services import get_yoruba_agent, get_telex_service
from datetime import datetime

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/webhook", tags=["webhook"])


@router.post("/telex", response_model=ActionResponse)
async def handle_telex_webhook(
    event: WebhookEvent,
    background_tasks: BackgroundTasks,
    request: Request
):
    """
    Handle incoming webhooks from Telex.im.
    
    This endpoint receives events from Telex.im and processes them accordingly.
    Message events are handled by the AI agent.
    """
    try:
        logger.info(f"Received webhook event: {event.event_type} - {event.event_id}")
        
        # Validate webhook signature (optional but recommended)
        # signature = request.headers.get("X-Telex-Signature", "")
        # telex_service = get_telex_service()
        # body = await request.body()
        # if not telex_service.validate_webhook_signature(body.decode(), signature):
        #     raise HTTPException(status_code=401, detail="Invalid webhook signature")
        
        # Handle different event types
        if event.event_type == EventType.MESSAGE and event.message:
            # Process message in background to respond quickly
            background_tasks.add_task(process_message, event)
            
            return ActionResponse(
                success=True,
                message="Message received and being processed"
            )
        
        elif event.event_type in [EventType.MESSAGE_DELIVERED, EventType.MESSAGE_READ]:
            # Log delivery/read receipts
            logger.info(f"Message status update: {event.event_type}")
            
            return ActionResponse(
                success=True,
                message=f"Event {event.event_type} acknowledged"
            )
        
        elif event.event_type in [EventType.USER_JOINED, EventType.USER_LEFT]:
            # Handle user join/leave events
            logger.info(f"User event: {event.event_type}")
            
            return ActionResponse(
                success=True,
                message=f"Event {event.event_type} acknowledged"
            )
        
        else:
            logger.warning(f"Unhandled event type: {event.event_type}")
            return ActionResponse(
                success=True,
                message="Event type not handled"
            )
    
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error processing webhook: {str(e)}"
        )


async def process_message(event: WebhookEvent):
    """
    Process incoming message from Telex.im.
    
    Args:
        event: WebhookEvent containing the message
    """
    try:
        message = event.message
        if not message or not message.text:
            logger.warning("Message has no text content")
            return
        
        user = message.from_user
        chat_id = message.chat_id
        message_text = message.text.strip()
        
        logger.info(f"Processing message from {user.id}: {message_text[:50]}...")
        
        # Get services
        agent = get_yoruba_agent()
        telex_service = get_telex_service()
        
        # Send typing indicator
        await telex_service.send_typing_action(chat_id)
        
        # Handle special commands
        if message_text.lower() in ['/start', 'hello', 'hi', 'hey', 'greetings']:
            response_text = await agent.get_greeting_response()
        
        elif message_text.lower() in ['/help', 'help', 'what can you do']:
            response_text = await agent.get_help_response()
        
        else:
            # Get user context
            user_context = {
                'name': user.first_name or user.username or "friend",
                'user_id': user.id,
                'language': user.language_code
            }
            
            # Get AI response
            response_text = await agent.get_response(message_text, user_context)
        
        # Send response back to user
        await telex_service.send_text_message(
            chat_id=chat_id,
            text=response_text,
            reply_to_message_id=message.message_id
        )
        
        logger.info(f"Response sent to {user.id} in chat {chat_id}")
    
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}", exc_info=True)
        # Try to send error message to user
        try:
            telex_service = get_telex_service()
            await telex_service.send_text_message(
                chat_id=chat_id,
                text="Mo tọrọ gafara (I apologize). An error occurred while processing your message. Please try again.",
                reply_to_message_id=message.message_id if message else None
            )
        except:
            pass


@router.get("/health")
async def webhook_health():
    """Health check endpoint for webhook service."""
    return {
        "status": "healthy",
        "service": "webhook",
        "timestamp": datetime.utcnow().isoformat()
    }
