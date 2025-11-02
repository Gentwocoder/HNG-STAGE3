"""
Main FastAPI application for Orunmila - Yoruba History & Culture AI Agent.
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from datetime import datetime

from app.core.config import settings
from app.utils.logging import setup_logging
from app.models.schemas import HealthResponse, ErrorResponse
from app.api import webhook_router, messages_router, agent_router

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Handles startup and shutdown events.
    """
    # Startup
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"Debug mode: {settings.debug}")
    
    # Initialize services
    try:
        from app.services import get_yoruba_agent, get_telex_service
        
        # Initialize agent
        agent = get_yoruba_agent()
        logger.info("Yoruba AI Agent initialized successfully")
        
        # Initialize Telex service
        telex = get_telex_service()
        logger.info("Telex.im service initialized successfully")
        
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}", exc_info=True)
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down application...")


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="""
    Orunmila is an AI agent specialized in Yoruba history and culture, integrated with Telex.im.
    
    ## Features
    
    * **AI-Powered Responses**: Intelligent answers about Yoruba history, culture, religion, and traditions
    * **Telex.im Integration**: Seamless webhook integration for real-time messaging
    * **REST API**: Direct API access for testing and integration
    * **Comprehensive Knowledge**: Covers history, culture, religion, language, arts, and more
    
    ## Endpoints
    
    * **/webhook/telex**: Receives events from Telex.im
    * **/messages/send**: Send messages via Telex.im API
    * **/agent/ask**: Direct interaction with the AI agent
    * **/health**: Health check endpoint
    
    Named after Orunmila, the Yoruba deity of wisdom and divination.
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
    debug=settings.debug
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)


# Exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors."""
    logger.error(f"Validation error: {exc.errors()}")
    
    return JSONResponse(
        status_code=422,
        content=ErrorResponse(
            error="ValidationError",
            message="Request validation failed",
            details={"errors": exc.errors()},
            timestamp=datetime.utcnow()
        ).model_dump()
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="InternalServerError",
            message="An unexpected error occurred",
            details={"error": str(exc)} if settings.debug else None,
            timestamp=datetime.utcnow()
        ).model_dump()
    )


# Include routers
app.include_router(webhook_router)
app.include_router(messages_router)
app.include_router(agent_router)


# Root endpoints
@app.get("/", tags=["root"])
async def root():
    """Root endpoint with basic information."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "description": "AI Agent for Yoruba History and Culture",
        "status": "active",
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "webhook": "/webhook/telex",
            "agent": "/agent/ask"
        },
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/health", response_model=HealthResponse, tags=["health"])
async def health_check():
    """
    Health check endpoint.
    
    Returns the current status of the application and its services.
    """
    try:
        # Check if agent is initialized
        from app.services import get_yoruba_agent, get_telex_service
        
        agent = get_yoruba_agent()
        telex = get_telex_service()
        
        return HealthResponse(
            status="healthy",
            version=settings.app_version,
            timestamp=datetime.utcnow()
        )
    
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return JSONResponse(
            status_code=503,
            content=HealthResponse(
                status="unhealthy",
                version=settings.app_version,
                timestamp=datetime.utcnow()
            ).model_dump()
        )


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
