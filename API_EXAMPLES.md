# API Usage Examples

This document provides practical examples of using the Orunmila API.

## Prerequisites

Ensure the server is running:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

---

## 1. Health Check

Check if the service is running properly.

**Request:**
```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "timestamp": "2025-11-02T10:00:00.123456"
}
```

---

## 2. Get Agent Greeting

Retrieve the welcome message from the agent.

**Request:**
```bash
curl http://localhost:8000/agent/greeting
```

**Response:**
```json
{
  "greeting": "Ẹ káàbọ̀! (Welcome!) 🌟\n\nI am Orunmila...",
  "agent": "Orunmila - Yoruba History & Culture AI"
}
```

---

## 3. Ask a Question (Direct Agent API)

Ask the AI agent a question directly without Telex.im.

**Request:**
```bash
curl -X POST http://localhost:8000/agent/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Who was Oduduwa?",
    "user_name": "John",
    "user_id": "user123"
  }'
```

**Response:**
```json
{
  "question": "Who was Oduduwa?",
  "answer": "Oduduwa is a central figure in Yoruba mythology and history...",
  "timestamp": "2025-11-02T10:05:00.123456"
}
```

**More Example Questions:**

History:
```bash
curl -X POST http://localhost:8000/agent/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Tell me about the Oyo Empire"}'
```

Culture:
```bash
curl -X POST http://localhost:8000/agent/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What are Yoruba naming ceremonies like?"}'
```

Religion:
```bash
curl -X POST http://localhost:8000/agent/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Who is Sango?"}'
```

Arts:
```bash
curl -X POST http://localhost:8000/agent/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What are Gelede masks?"}'
```

Language:
```bash
curl -X POST http://localhost:8000/agent/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Share a Yoruba proverb"}'
```

---

## 4. Receive Webhook from Telex.im

This endpoint receives messages from Telex.im.

**Request:**
```bash
curl -X POST http://localhost:8000/webhook/telex \
  -H "Content-Type: application/json" \
  -d '{
    "event_id": "evt_12345",
    "event_type": "message",
    "timestamp": "2025-11-02T10:00:00Z",
    "message": {
      "message_id": "msg_67890",
      "from": {
        "id": "user_abc",
        "first_name": "Alice",
        "username": "alice_wonder",
        "language_code": "en"
      },
      "chat_id": "chat_xyz",
      "text": "What is Ifa divination?",
      "message_type": "text",
      "timestamp": "2025-11-02T10:00:00Z"
    }
  }'
```

**Response:**
```json
{
  "success": true,
  "message": "Message received and being processed"
}
```

---

## 5. Send Message via Telex.im

Send a message to a user through Telex.im API.

**Request:**
```bash
curl -X POST http://localhost:8000/messages/send \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "chat_xyz",
    "text": "Ẹ káàbọ̀! How can I help you today?",
    "reply_to_message_id": "msg_67890"
  }'
```

**Response:**
```json
{
  "success": true,
  "message": "Message sent successfully",
  "data": {
    "message_id": "msg_new123",
    "status": "sent"
  }
}
```

---

## 6. Broadcast Message

Send the same message to multiple chats.

**Request:**
```bash
curl -X POST http://localhost:8000/messages/broadcast \
  -H "Content-Type: application/json" \
  -d '{
    "chat_ids": ["chat_1", "chat_2", "chat_3"],
    "text": "Important: The Osun-Osogbo Festival will be held next month!"
  }'
```

**Response:**
```json
{
  "success": true,
  "message": "Broadcast completed: 3 successful, 0 failed",
  "data": {
    "successful": [
      {"chat_id": "chat_1", "success": true, "result": {...}},
      {"chat_id": "chat_2", "success": true, "result": {...}},
      {"chat_id": "chat_3", "success": true, "result": {...}}
    ],
    "failed": [],
    "total": 3
  }
}
```

---

## 7. Get Help

Retrieve help information with example questions.

**Request:**
```bash
curl http://localhost:8000/agent/help
```

**Response:**
```json
{
  "help": "📚 **How to Ask Questions**\n\nHere are some example questions...",
  "agent": "Orunmila - Yoruba History & Culture AI"
}
```

---

## Interactive API Documentation

Visit these URLs in your browser for interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These interfaces allow you to:
- Try out endpoints directly in the browser
- See detailed request/response schemas
- View all available endpoints
- Test with different parameters

---

## Python Example

Here's how to use the API from Python:

```python
import httpx
import asyncio

async def ask_orunmila(question: str):
    """Ask a question to the Orunmila agent."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/agent/ask",
            json={
                "question": question,
                "user_name": "Python Script"
            }
        )
        result = response.json()
        return result["answer"]

# Run the example
async def main():
    questions = [
        "Who was Moremi?",
        "What is the Osun-Osogbo Festival?",
        "Tell me about Yoruba talking drums"
    ]
    
    for question in questions:
        print(f"\nQ: {question}")
        answer = await ask_orunmila(question)
        print(f"A: {answer}\n")
        print("-" * 60)

asyncio.run(main())
```

---

## JavaScript/Node.js Example

```javascript
const axios = require('axios');

async function askOrunmila(question) {
    try {
        const response = await axios.post('http://localhost:8000/agent/ask', {
            question: question,
            user_name: 'JS Client'
        });
        
        return response.data.answer;
    } catch (error) {
        console.error('Error:', error.message);
    }
}

// Example usage
(async () => {
    const questions = [
        'What is Adire cloth?',
        'Tell me about the Eyo Festival'
    ];
    
    for (const question of questions) {
        console.log(`\nQ: ${question}`);
        const answer = await askOrunmila(question);
        console.log(`A: ${answer}\n`);
        console.log('-'.repeat(60));
    }
})();
```

---

## Error Handling

**Invalid Request (422):**
```json
{
  "error": "ValidationError",
  "message": "Request validation failed",
  "details": {
    "errors": [
      {
        "loc": ["body", "question"],
        "msg": "field required",
        "type": "value_error.missing"
      }
    ]
  },
  "timestamp": "2025-11-02T10:00:00.123456"
}
```

**Server Error (500):**
```json
{
  "error": "InternalServerError",
  "message": "An unexpected error occurred",
  "timestamp": "2025-11-02T10:00:00.123456"
}
```

---

## Rate Limiting (If Implemented)

If rate limiting is enabled, you may receive:

```json
{
  "error": "RateLimitExceeded",
  "message": "Too many requests. Please try again later.",
  "details": {
    "retry_after": 60
  }
}
```

---

## Webhook Verification

When Telex.im sends webhooks, they include a signature header for verification:

```
X-Telex-Signature: sha256=abc123...
```

The server validates this signature using the `TELEX_WEBHOOK_SECRET` from your environment variables.
