# 🚀 Quick Start Guide - Orunmila AI Agent

Get your Yoruba History & Culture AI Agent up and running in 5 minutes!

## Prerequisites

- Python 3.11 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- (Optional) Telex.im account for webhook integration

## Step 1: Set Up Environment

```bash
# Navigate to project directory
cd /home/gentle/Documents/HNG-STAGE3

# Create virtual environment (if not already created)
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Linux/Mac
# OR
# venv\Scripts\activate  # On Windows
```

## Step 2: Install Dependencies

```bash
# Install all required packages
pip install -e .

# OR use requirements.txt
pip install -r requirements.txt
```

## Step 3: Configure API Keys

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your favorite editor
nano .env  # or vim, code, etc.
```

**Minimum required configuration:**
```env
OPENAI_API_KEY=sk-your-openai-api-key-here
```

**Optional (for Telex.im integration):**
```env
TELEX_API_KEY=your_telex_api_key
TELEX_WEBHOOK_SECRET=your_webhook_secret
TELEX_BOT_ID=your_bot_id
```

## Step 4: Verify Setup

```bash
# Run the verification script
python test_setup.py
```

You should see:
```
✅ Configuration loaded successfully
✅ AI Agent initialized successfully
✅ Agent response generated successfully
✅ All tests passed!
```

## Step 5: Start the Server

```bash
# Start in development mode
python main.py
```

You should see:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Starting Orunmila - Yoruba History & Culture AI Agent v0.1.0
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## Step 6: Test the API

### In Your Browser

1. **Interactive Documentation**: http://localhost:8000/docs
2. **Health Check**: http://localhost:8000/health
3. **Root Info**: http://localhost:8000

### Using cURL

```bash
# Get greeting
curl http://localhost:8000/agent/greeting

# Ask a question
curl -X POST http://localhost:8000/agent/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Who was Oduduwa?"}'

# Get help
curl http://localhost:8000/agent/help
```

### Using Python

```python
import httpx
import asyncio

async def test_agent():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/agent/ask",
            json={"question": "What is Ifa divination?"}
        )
        print(response.json()["answer"])

asyncio.run(test_agent())
```

## 🎉 You're Ready!

Your Orunmila AI Agent is now running and ready to answer questions about Yoruba history and culture.

## Next Steps

### For Development
- Read [DEVELOPMENT.md](DEVELOPMENT.md) for development guidelines
- Check [API_EXAMPLES.md](API_EXAMPLES.md) for more API examples
- Explore the interactive docs at http://localhost:8000/docs

### For Telex.im Integration
1. Set up a bot on Telex.im
2. Add your credentials to `.env`
3. Configure webhook URL: `https://your-domain.com/webhook/telex`
4. Test with a message to your bot

### For Deployment
- See [README.md](README.md#-deployment) for deployment options
- Configure environment variables for production
- Set `DEBUG=False` in production

## Troubleshooting

### "ModuleNotFoundError"
```bash
# Make sure virtual environment is activated and dependencies installed
source venv/bin/activate
pip install -e .
```

### "OpenAI API Error"
- Check your API key is correct in `.env`
- Ensure you have credits in your OpenAI account
- Verify internet connection

### "Port already in use"
```bash
# Change port in .env or run with custom port
PORT=8080 python main.py
```

### Agent not responding
- Check logs for error messages
- Verify OpenAI API key is valid
- Ensure internet connection is working

## Common Commands

```bash
# Start server
python main.py

# Test setup
python test_setup.py

# Install dependencies
pip install -e .

# Update dependencies
pip install --upgrade -r requirements.txt

# Check logs (in terminal where server is running)
# Logs appear in real-time
```

## Getting Help

1. Check [README.md](README.md) for comprehensive documentation
2. Review [API_EXAMPLES.md](API_EXAMPLES.md) for usage examples
3. Visit http://localhost:8000/docs for interactive API testing
4. Check the logs in your terminal

## Example Questions to Try

- "Who was Oduduwa?"
- "Tell me about the Oyo Empire"
- "What is Ifa divination?"
- "Who is Sango?"
- "What are Gelede masks?"
- "Tell me about Adire cloth"
- "Share a Yoruba proverb"
- "What is the Osun-Osogbo Festival?"
- "How do you greet someone in Yoruba?"
- "Who was Moremi?"

---

**Ẹ káàbọ̀!** (Welcome!) Your journey into Yoruba history and culture starts now! 🌟
