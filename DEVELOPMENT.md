# Development Guide

## Setting Up Development Environment

1. **Clone and setup**
   ```bash
   cd /home/gentle/Documents/HNG-STAGE3
   python -m venv venv
   source venv/bin/activate
   pip install -e .
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Run in development mode**
   ```bash
   python main.py
   ```

## Code Structure

### Adding New Features

#### Add a New Endpoint

1. Create a new router in `app/api/`
2. Define Pydantic models in `app/models/schemas.py`
3. Implement business logic in `app/services/`
4. Register router in `main.py`

#### Extend Agent Knowledge

Edit `app/services/yoruba_agent.py` and update the `SYSTEM_PROMPT` with additional information.

#### Add New Services

1. Create service file in `app/services/`
2. Implement service class
3. Export in `app/services/__init__.py`

## Testing

### Manual Testing with cURL

**Test health endpoint:**
```bash
curl http://localhost:8000/health
```

**Test agent:**
```bash
curl -X POST http://localhost:8000/agent/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is Ifa divination?",
    "user_name": "Developer"
  }'
```

**Test webhook (simulate Telex.im):**
```bash
curl -X POST http://localhost:8000/webhook/telex \
  -H "Content-Type: application/json" \
  -d '{
    "event_id": "evt_test_123",
    "event_type": "message",
    "timestamp": "2025-11-02T10:00:00Z",
    "message": {
      "message_id": "msg_test_456",
      "from": {
        "id": "user_test",
        "first_name": "Test",
        "username": "tester"
      },
      "chat_id": "chat_test",
      "text": "Who was Oduduwa?",
      "message_type": "text"
    }
  }'
```

### Using the Interactive Docs

1. Navigate to `http://localhost:8000/docs`
2. Expand any endpoint
3. Click "Try it out"
4. Fill in parameters
5. Execute and view response

## Debugging

### Enable Debug Logging

Set in `.env`:
```env
DEBUG=True
LOG_LEVEL=DEBUG
```

### Common Issues

**Issue: Agent not responding**
- Check OpenAI API key is set correctly
- Verify internet connection
- Check logs for errors

**Issue: Telex.im webhook failing**
- Verify webhook URL is publicly accessible
- Check webhook secret matches
- Review webhook logs in Telex.im dashboard

**Issue: Import errors**
- Ensure virtual environment is activated
- Run `pip install -e .` again

## Performance Optimization

### Caching

To enable Redis caching:
```env
REDIS_ENABLED=True
REDIS_URL=redis://localhost:6379/0
```

### Background Tasks

Long-running operations are handled in background tasks. See `app/api/webhook.py` for examples.

## Deployment Checklist

- [ ] Set `DEBUG=False` in production
- [ ] Use strong webhook secrets
- [ ] Configure CORS appropriately
- [ ] Set up monitoring and logging
- [ ] Use environment-specific `.env` files
- [ ] Enable HTTPS
- [ ] Set up rate limiting
- [ ] Configure health checks
- [ ] Set proper worker count for uvicorn

## Code Style

Follow PEP 8 guidelines:
```bash
# Format code (if using black)
black app/ main.py

# Sort imports (if using isort)
isort app/ main.py
```

## Contributing Workflow

1. Create a feature branch
2. Make changes
3. Test thoroughly
4. Update documentation
5. Submit pull request

## Resources

- [FastAPI Best Practices](https://fastapi.tiangolo.com/tutorial/)
- [Pydantic AI Guide](https://ai.pydantic.dev/)
- [Python Async Programming](https://docs.python.org/3/library/asyncio.html)
