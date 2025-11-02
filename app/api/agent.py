"""
Agent routes for direct interaction with the AI agent.
"""

import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services import get_yoruba_agent

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/agent", tags=["agent"])


class QuestionRequest(BaseModel):
    """Request model for asking questions."""
    question: str
    user_name: str | None = None
    user_id: str | None = None


class QuestionResponse(BaseModel):
    """Response model for agent answers."""
    question: str
    answer: str
    timestamp: str


@router.post("/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    """
    Ask a question to the Yoruba AI agent.
    
    This endpoint allows direct interaction with the AI agent without going through Telex.im.
    Useful for testing or integration with other platforms.
    """
    try:
        logger.info(f"Received question: {request.question[:50]}...")
        
        agent = get_yoruba_agent()
        
        # Prepare user context if provided
        user_context = None
        if request.user_name or request.user_id:
            user_context = {
                'name': request.user_name or 'friend',
                'user_id': request.user_id
            }
        
        # Get response from agent
        answer = await agent.get_response(request.question, user_context)
        
        from datetime import datetime
        
        return QuestionResponse(
            question=request.question,
            answer=answer,
            timestamp=datetime.utcnow().isoformat()
        )
    
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process question: {str(e)}"
        )


@router.get("/greeting")
async def get_greeting():
    """Get the agent's greeting message."""
    try:
        agent = get_yoruba_agent()
        greeting = await agent.get_greeting_response()
        
        return {
            "greeting": greeting,
            "agent": "Orunmila - Yoruba History & Culture AI"
        }
    
    except Exception as e:
        logger.error(f"Error getting greeting: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get greeting: {str(e)}"
        )


@router.get("/help")
async def get_help():
    """Get help information and example questions."""
    try:
        agent = get_yoruba_agent()
        help_text = await agent.get_help_response()
        
        return {
            "help": help_text,
            "agent": "Orunmila - Yoruba History & Culture AI"
        }
    
    except Exception as e:
        logger.error(f"Error getting help: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get help: {str(e)}"
        )
