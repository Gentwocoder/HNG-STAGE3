#!/usr/bin/env python3
"""
Quick test script to verify the Orunmila agent setup.
Run this after setting up your environment to ensure everything works.
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


async def test_configuration():
    """Test that configuration loads properly."""
    print("🔧 Testing configuration...")
    try:
        from app.core.config import settings
        print(f"✅ Configuration loaded successfully")
        print(f"   App Name: {settings.app_name}")
        print(f"   Version: {settings.app_version}")
        print(f"   Debug Mode: {settings.debug}")
        
        # Check critical settings
        if not settings.openai_api_key:
            print("⚠️  WARNING: OPENAI_API_KEY not set!")
        else:
            print(f"✅ OpenAI API key is configured")
        
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False


async def test_agent_initialization():
    """Test that the AI agent initializes properly."""
    print("\n🤖 Testing AI Agent initialization...")
    try:
        from app.services.yoruba_agent import get_yoruba_agent
        agent = get_yoruba_agent()
        print("✅ AI Agent initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Agent initialization failed: {e}")
        print("   Make sure your OPENAI_API_KEY is set in .env")
        return False


async def test_agent_response():
    """Test that the agent can generate a response."""
    print("\n💬 Testing AI Agent response generation...")
    try:
        from app.services.yoruba_agent import get_yoruba_agent
        agent = get_yoruba_agent()
        
        question = "Who was Oduduwa?"
        print(f"   Question: {question}")
        
        response = await agent.get_response(question)
        print(f"   Response: {response[:100]}...")
        print("✅ Agent response generated successfully")
        return True
    except Exception as e:
        print(f"❌ Agent response test failed: {e}")
        return False


async def test_greeting():
    """Test greeting message."""
    print("\n👋 Testing greeting message...")
    try:
        from app.services.yoruba_agent import get_yoruba_agent
        agent = get_yoruba_agent()
        
        greeting = await agent.get_greeting_response()
        print(f"   Greeting: {greeting[:80]}...")
        print("✅ Greeting generated successfully")
        return True
    except Exception as e:
        print(f"❌ Greeting test failed: {e}")
        return False


async def test_telex_service():
    """Test Telex service initialization."""
    print("\n📡 Testing Telex.im service...")
    try:
        from app.services.telex_service import get_telex_service
        from app.core.config import settings
        
        service = get_telex_service()
        print("✅ Telex service initialized successfully")
        
        if not settings.telex_api_key:
            print("⚠️  WARNING: TELEX_API_KEY not set (optional for direct agent testing)")
        
        return True
    except Exception as e:
        print(f"❌ Telex service test failed: {e}")
        return False


async def main():
    """Run all tests."""
    print("=" * 60)
    print("🌟 ORUNMILA - AI AGENT VERIFICATION TESTS")
    print("=" * 60)
    
    results = []
    
    # Run tests
    results.append(await test_configuration())
    results.append(await test_agent_initialization())
    
    # Only run response test if previous tests passed
    if all(results):
        results.append(await test_agent_response())
        results.append(await test_greeting())
    
    results.append(await test_telex_service())
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    
    print(f"Tests Passed: {passed}/{total}")
    
    if passed == total:
        print("✅ All tests passed! Your Orunmila agent is ready to use.")
        print("\n🚀 Next steps:")
        print("   1. Run the server: python main.py")
        print("   2. Visit the docs: http://localhost:8000/docs")
        print("   3. Test the agent: curl http://localhost:8000/agent/greeting")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("\n🔍 Common issues:")
        print("   - Missing OPENAI_API_KEY in .env file")
        print("   - Dependencies not installed (run: pip install -e .)")
        print("   - Python version < 3.11")
    
    print("=" * 60)
    
    return 0 if passed == total else 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
