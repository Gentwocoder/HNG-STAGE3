"""
AI Agent service for answering questions about Yoruba history and culture.
Uses pydantic-ai for intelligent responses.
"""

import logging
import os
from typing import Optional
from pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModel
from app.core.config import settings

logger = logging.getLogger(__name__)


class YorubaAgent:
    """
    AI Agent specialized in Yoruba history and culture.
    
    This agent is designed to provide accurate, informative responses about:
    - Yoruba history and origins
    - Cultural practices and traditions
    - Religious beliefs (Ifa, Orisha worship)
    - Language and proverbs
    - Art, music, and literature
    - Notable historical figures
    - Festivals and celebrations
    """
    
    SYSTEM_PROMPT = """You are Orunmila, an AI assistant specialized in Yoruba history and culture. 
You are named after the Yoruba deity of wisdom, knowledge, and divination.

Your expertise includes:
- **History**: The origins of the Yoruba people, ancient kingdoms (Oyo, Ife, Benin connections), 
  historical migrations, colonialism impact, and modern Yoruba states in Nigeria.
  
- **Culture**: Traditional practices, family structures, chieftaincy systems, naming ceremonies 
  (Isomoloruko), weddings (Igbeyawo), funerals, and social customs.
  
- **Religion**: Ifa divination system, Orisha worship (Orunmila, Sango, Oya, Osun, Obatala, etc.), 
  ancestor veneration, and the integration with Christianity and Islam.
  
- **Language**: Yoruba language structure, proverbs (Owe), greetings, tonal system, and the importance 
  of language in cultural preservation.
  
- **Arts**: Gelede masks, Egungun masquerades, bronze and terracotta works, Aso-Oke weaving, 
  indigo dyeing (Adire), sculpture, and contemporary Yoruba art.
  
- **Music & Dance**: Talking drums (Dundun, Gangan), Bata drums, traditional music styles, 
  dance forms, and their roles in ceremonies.
  
- **Notable Figures**: Historical leaders (Sango, Oduduwa, Moremi), scholars, activists, 
  and contemporary influencers.
  
- **Festivals**: Olojo Festival, Osun-Osogbo Festival, Eyo Festival, and other cultural celebrations.

- **Diaspora**: Yoruba influence in the Americas (Cuba, Brazil, Trinidad), Santeria, Candomblé, 
  and the preservation of Yoruba culture globally.

Guidelines for responses:
1. Provide accurate, well-researched information
2. Be respectful and culturally sensitive
3. Acknowledge the diversity within Yoruba culture
4. When uncertain, say so and offer to explore the topic further
5. Use Yoruba terms when appropriate, with English translations
6. Keep responses informative but concise
7. Encourage cultural appreciation and learning

Remember: You're an educational resource promoting understanding and appreciation of Yoruba heritage.
"""

    def __init__(self):
        """Initialize the Yoruba AI Agent."""
        try:
            # Set Google Gemini API key in environment (pydantic-ai uses env variables)
            if settings.gemini_api_key:
                os.environ['GEMINI_API_KEY'] = settings.gemini_api_key
            
            # Initialize the Gemini model
            # Using gemini-2.5-flash (latest stable version)
            model = GeminiModel('gemini-2.5-flash')
            
            # Create the agent with the specialized system prompt
            self.agent = Agent(
                model=model,
                system_prompt=self.SYSTEM_PROMPT,
            )
            
            logger.info("Yoruba AI Agent initialized successfully with Gemini 2.5 Flash")
            
        except Exception as e:
            logger.error(f"Failed to initialize Yoruba AI Agent: {str(e)}")
            raise
    
    async def get_response(self, question: str, user_context: Optional[dict] = None) -> str:
        """
        Get a response from the AI agent for a given question.
        
        Args:
            question: The user's question about Yoruba history and culture
            user_context: Optional context about the user for personalized responses
            
        Returns:
            The AI agent's response as a string
        """
        try:
            # Add user context to the question if available
            enhanced_question = question
            if user_context:
                user_name = user_context.get('name', 'friend')
                enhanced_question = f"Question from {user_name}: {question}"
            
            # Get response from the agent
            result = await self.agent.run(enhanced_question)
            
            # Extract response text from result
            # pydantic-ai v0.0.14+ uses .output attribute
            if hasattr(result, 'output'):
                response_text = result.output
            elif hasattr(result, 'data'):
                response_text = result.data
            elif hasattr(result, 'content'):
                response_text = result.content
            else:
                response_text = str(result)
            
            logger.info(f"Generated response for question: {question[:50]}...")
            
            return response_text
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return (
                "Mo dùpẹ́ (Thank you) for your question. I encountered an issue while "
                "processing it. Please try rephrasing your question or ask about a specific "
                "aspect of Yoruba history and culture."
            )
    
    async def is_relevant_question(self, question: str) -> bool:
        """
        Check if a question is relevant to Yoruba history and culture.
        
        Args:
            question: The user's question
            
        Returns:
            True if relevant, False otherwise
        """
        # Simple keyword-based check (can be enhanced with AI classification)
        yoruba_keywords = [
            'yoruba', 'oyo', 'ife', 'nigeria', 'orisha', 'ifa', 'sango', 'orunmila',
            'oduduwa', 'obatala', 'osun', 'oya', 'african', 'west africa', 'igbo',
            'hausa', 'benin', 'festival', 'traditional', 'culture', 'history',
            'language', 'proverb', 'owe', 'egungun', 'gelede', 'adire', 'aso-oke'
        ]
        
        question_lower = question.lower()
        return any(keyword in question_lower for keyword in yoruba_keywords)
    
    async def get_greeting_response(self) -> str:
        """
        Get a friendly greeting response.
        
        Returns:
            A greeting message
        """
        return (
            "Ẹ káàbọ̀! (Welcome!) 🌟\n\n"
            "I am Orunmila, your guide to Yoruba history and culture. "
            "I'm here to answer your questions about:\n\n"
            "• Yoruba history and ancient kingdoms\n"
            "• Cultural practices and traditions\n"
            "• Religion and spirituality (Ifa, Orisha)\n"
            "• Language, proverbs, and sayings\n"
            "• Art, music, and dance\n"
            "• Festivals and celebrations\n"
            "• Notable historical figures\n\n"
            "Feel free to ask me anything about Yoruba heritage!"
        )
    
    async def get_help_response(self) -> str:
        """
        Get a help message with example questions.
        
        Returns:
            A help message with examples
        """
        return (
            "📚 **How to Ask Questions**\n\n"
            "Here are some example questions you can ask:\n\n"
            "**History:**\n"
            "• Who was Oduduwa?\n"
            "• Tell me about the Oyo Empire\n"
            "• What is the significance of Ile-Ife?\n\n"
            "**Culture:**\n"
            "• What are Yoruba naming ceremonies like?\n"
            "• Explain the chieftaincy system\n\n"
            "**Religion:**\n"
            "• Who is Sango?\n"
            "• What is Ifa divination?\n\n"
            "**Arts:**\n"
            "• What are Gelede masks?\n"
            "• Tell me about Adire cloth\n\n"
            "**Language:**\n"
            "• Share a Yoruba proverb\n"
            "• How do you say hello in Yoruba?\n\n"
            "Just ask your question naturally, and I'll do my best to help!"
        )


# Global agent instance
_agent_instance: Optional[YorubaAgent] = None


def get_yoruba_agent() -> YorubaAgent:
    """
    Get or create the global Yoruba agent instance.
    
    Returns:
        YorubaAgent instance
    """
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = YorubaAgent()
    return _agent_instance
