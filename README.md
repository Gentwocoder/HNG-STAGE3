# Orunmila - Yoruba History & Culture AI Agent

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**Orunmila** is an intelligent AI agent specialized in answering questions about Yoruba history and culture. Named after the Yoruba deity of wisdom and divination, this agent provides accurate, culturally sensitive information about Yoruba heritage, integrated seamlessly with Telex.im messaging platform.

## 🌟 Features

- **AI-Powered Knowledge Base**: Comprehensive understanding of Yoruba history, culture, religion, language, arts, and traditions
- **Telex.im Integration**: Real-time webhook support for instant messaging responses
- **REST API**: Clean, well-documented API for direct interaction
- **Robust Error Handling**: Proper validation and error responses
- **Background Processing**: Efficient message handling with async processing
- **Extensible Architecture**: Modular design for easy customization

## 📋 What the Agent Knows

### History
- Origins of the Yoruba people
- Ancient kingdoms (Oyo, Ife, Benin connections)
- Historical migrations and settlements
- Colonial era and independence
- Modern Yoruba states in Nigeria

### Culture
- Traditional practices and customs
- Family structures and chieftaincy systems
- Naming ceremonies (Isomoloruko)
- Weddings (Igbeyawo) and funerals
- Social etiquette and values

### Religion
- Ifa divination system
- Orisha worship (Sango, Oya, Osun, Obatala, etc.)
- Ancestor veneration
- Integration with Christianity and Islam

### Language
- Yoruba language structure
- Proverbs (Owe) and sayings
- Greetings and common phrases
- Tonal system and pronunciation

### Arts & Music
- Gelede masks and Egungun masquerades
- Bronze and terracotta works
- Aso-Oke weaving and Adire cloth
- Traditional music and dance
- Talking drums (Dundun, Gangan, Bata)

### Festivals
- Olojo Festival
- Osun-Osogbo Festival
- Eyo Festival
- Other cultural celebrations

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- OpenAI API key
- Telex.im account and API credentials (optional for webhook integration)

### Installation

1. **Clone the repository**
   ```bash
   cd /home/gentle/Documents/HNG-STAGE3
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Linux/Mac
   # or
   # venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -e .
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your API keys:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   TELEX_API_KEY=your_telex_api_key_here
   TELEX_WEBHOOK_SECRET=your_webhook_secret_here
   TELEX_BOT_ID=your_bot_id_here
   ```

### Running the Application

**Development mode:**
```bash
python main.py
```

**Production mode with Uvicorn:**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

The API will be available at:
- API: `http://localhost:8000`
- Interactive docs: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

## 📡 API Endpoints

### Webhook Endpoints

#### POST `/webhook/telex`
Receives webhook events from Telex.im.

**Request Body:**
```json
{
  "event_id": "evt_123",
  "event_type": "message",
  "timestamp": "2025-11-02T10:00:00Z",
  "message": {
    "message_id": "msg_456",
    "from": {
      "id": "user_789",
      "first_name": "John",
      "username": "john_doe"
    },
    "chat_id": "chat_101",
    "text": "Who was Oduduwa?",
    "message_type": "text"
  }
}
```

### Message Endpoints

#### POST `/messages/send`
Send a message via Telex.im API.

**Request Body:**
```json
{
  "chat_id": "chat_101",
  "text": "Hello! I'm Orunmila.",
  "reply_to_message_id": "msg_456"
}
```

#### POST `/messages/broadcast`
Broadcast a message to multiple chats.

**Request Body:**
```json
{
  "chat_ids": ["chat_101", "chat_102", "chat_103"],
  "text": "Important announcement!"
}
```

### Agent Endpoints

#### POST `/agent/ask`
Ask a question directly to the AI agent.

**Request Body:**
```json
{
  "question": "What is the significance of Ile-Ife?",
  "user_name": "John",
  "user_id": "user_789"
}
```

**Response:**
```json
{
  "question": "What is the significance of Ile-Ife?",
  "answer": "Ile-Ife is considered the spiritual and ancestral home...",
  "timestamp": "2025-11-02T10:00:00Z"
}
```

#### GET `/agent/greeting`
Get the agent's greeting message.

#### GET `/agent/help`
Get help information and example questions.

### Health Endpoint

#### GET `/health`
Check the health status of the application.

**Response:**
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "timestamp": "2025-11-02T10:00:00Z"
}
```

## 🏗️ Project Structure

```
HNG-STAGE3/
├── app/
│   ├── __init__.py
│   ├── api/                    # API route handlers
│   │   ├── __init__.py
│   │   ├── webhook.py         # Telex.im webhook handlers
│   │   ├── messages.py        # Message sending endpoints
│   │   └── agent.py           # Direct agent interaction
│   ├── core/                  # Core configurations
│   │   ├── __init__.py
│   │   └── config.py          # Settings and environment
│   ├── models/                # Pydantic models
│   │   ├── __init__.py
│   │   └── schemas.py         # Request/response schemas
│   ├── services/              # Business logic
│   │   ├── __init__.py
│   │   ├── yoruba_agent.py   # AI agent implementation
│   │   └── telex_service.py  # Telex.im integration
│   └── utils/                 # Utilities
│       ├── __init__.py
│       └── logging.py         # Logging configuration
├── main.py                    # FastAPI application
├── pyproject.toml            # Project dependencies
├── .env.example              # Environment template
└── README.md                 # This file
```

## 🔧 Configuration

All configuration is done through environment variables in `.env`:

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for the AI agent | Yes |
| `TELEX_API_KEY` | Telex.im API key | For webhook integration |
| `TELEX_WEBHOOK_SECRET` | Webhook validation secret | For webhook integration |
| `TELEX_BOT_ID` | Your bot ID on Telex.im | For webhook integration |
| `TELEX_API_URL` | Telex.im API base URL | Optional |
| `DEBUG` | Enable debug mode | Optional |
| `LOG_LEVEL` | Logging level (INFO, DEBUG, WARNING) | Optional |
| `HOST` | Server host | Optional (default: 0.0.0.0) |
| `PORT` | Server port | Optional (default: 8000) |

## 💬 Example Interactions

**User:** "Who was Oduduwa?"

**Orunmila:** "Oduduwa is a central figure in Yoruba mythology and history. He is regarded as the progenitor of the Yoruba people and the first divine king of Ile-Ife. According to legend, Oduduwa descended from heaven to create the earth and establish the first Yoruba settlement at Ile-Ife, which is considered the spiritual and ancestral home of all Yoruba people..."

**User:** "Tell me about Sango"

**Orunmila:** "Sango (also spelled Shango) is one of the most powerful and popular Orishas in Yoruba religion. He is the deity of thunder, lightning, fire, and justice. Historically, Sango was the fourth Alafin (king) of the Oyo Empire. According to tradition, he was a powerful and charismatic ruler known for his magical powers and warrior skills..."

**User:** "What is Adire?"

**Orunmila:** "Adire is a traditional Yoruba textile art form that involves the resist-dyeing of cotton fabric using indigo dye. The name 'Adire' comes from the Yoruba words 'adi' (to tie) and 're' (to dye). This ancient craft, primarily practiced by women, creates beautiful blue and white patterned cloth..."

## 🔐 Security

- **Webhook Validation**: Implement signature verification for Telex.im webhooks
- **API Key Management**: Store sensitive keys in environment variables
- **CORS Configuration**: Configure allowed origins appropriately
- **Rate Limiting**: Consider adding rate limiting for production use
- **Input Validation**: All inputs are validated using Pydantic models

## 🚢 Deployment

### Using Docker (Recommended)

Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install -e .

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t orunmila-agent .
docker run -p 8000:8000 --env-file .env orunmila-agent
```

### Using Cloud Platforms

The application can be deployed to:
- **Heroku**: Use Procfile with gunicorn
- **Railway**: Connect GitHub repo and deploy
- **Render**: Deploy with automatic HTTPS
- **AWS/GCP/Azure**: Use container services or serverless functions

### Webhook Setup

1. Deploy your application to a public URL (e.g., `https://your-domain.com`)
2. Configure webhook in Telex.im dashboard:
   - Webhook URL: `https://your-domain.com/webhook/telex`
   - Events: Select message events
3. Test the webhook connection

## 🧪 Testing

**Test the API locally:**
```bash
curl http://localhost:8000/health
```

**Test the agent:**
```bash
curl -X POST http://localhost:8000/agent/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Who was Moremi?"}'
```

**Test greeting:**
```bash
curl http://localhost:8000/agent/greeting
```

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic AI Documentation](https://ai.pydantic.dev/)
- [OpenAI API Reference](https://platform.openai.com/docs)
- [Yoruba Cultural Resources](https://en.wikipedia.org/wiki/Yoruba_people)

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional Yoruba cultural knowledge
- Enhanced NLP capabilities
- Multi-language support
- Caching for frequently asked questions
- Rate limiting and security enhancements

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Named after **Orunmila**, the Yoruba deity of wisdom and divination
- Built with respect for Yoruba culture and heritage
- Designed for educational purposes and cultural preservation

## 📞 Support

For questions or issues:
- Check the `/agent/help` endpoint for usage examples
- Review the interactive API docs at `/docs`
- Ensure your OpenAI API key is properly configured

---

**Ẹ káàbọ̀!** (Welcome!) - May this agent serve as a bridge to understanding and appreciating Yoruba heritage.
