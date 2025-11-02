"""
Pydantic models for Telex.im webhook requests and responses.
"""

from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class MessageType(str, Enum):
    """Types of messages supported."""
    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    FILE = "file"
    LOCATION = "location"


class EventType(str, Enum):
    """Types of events from Telex.im."""
    MESSAGE = "message"
    MESSAGE_DELIVERED = "message.delivered"
    MESSAGE_READ = "message.read"
    USER_JOINED = "user.joined"
    USER_LEFT = "user.left"


class User(BaseModel):
    """User information model."""
    id: str = Field(..., description="User ID")
    username: Optional[str] = Field(None, description="Username")
    first_name: Optional[str] = Field(None, description="User's first name")
    last_name: Optional[str] = Field(None, description="User's last name")
    language_code: Optional[str] = Field(None, description="User's language code")


class Message(BaseModel):
    """Message model for incoming messages."""
    message_id: str = Field(..., description="Unique message ID")
    from_user: User = Field(..., alias="from", description="Sender information")
    chat_id: str = Field(..., description="Chat ID where the message was sent")
    text: Optional[str] = Field(None, description="Message text content")
    message_type: MessageType = Field(default=MessageType.TEXT, description="Type of message")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Message timestamp")
    reply_to_message_id: Optional[str] = Field(None, description="ID of message being replied to")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata")
    
    class Config:
        populate_by_name = True


class WebhookEvent(BaseModel):
    """Webhook event model from Telex.im."""
    event_id: str = Field(..., description="Unique event ID")
    event_type: EventType = Field(..., description="Type of event")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Event timestamp")
    message: Optional[Message] = Field(None, description="Message data if event is message-related")
    data: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional event data")


class MessageResponse(BaseModel):
    """Response model for sending messages."""
    chat_id: str = Field(..., description="Chat ID to send message to")
    text: str = Field(..., description="Message text to send")
    reply_to_message_id: Optional[str] = Field(None, description="ID of message to reply to")
    parse_mode: Optional[str] = Field(default="Markdown", description="Message formatting mode")
    disable_web_page_preview: bool = Field(default=False, description="Disable link previews")


class ActionResponse(BaseModel):
    """Generic action response model."""
    success: bool = Field(..., description="Whether the action was successful")
    message: Optional[str] = Field(None, description="Response message")
    data: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional response data")


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="Application version")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Health check timestamp")


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Error timestamp")
