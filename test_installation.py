"""Simple test to verify claude-agent-sdk installation."""

import anyio
from claude_agent_sdk import query, ClaudeSDKClient, ClaudeAgentOptions

async def test_basic_query():
    """Test basic query functionality."""
    print("Testing basic query...")
    print("-" * 50)

    try:
        async for message in query(prompt="What is 2 + 2? Answer in one sentence."):
            print(f"Received message: {message}")
            print()
    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}")

async def test_import():
    """Test that all imports work."""
    print("\nTesting imports...")
    print("-" * 50)

    from claude_agent_sdk import (
        query,
        ClaudeSDKClient,
        ClaudeAgentOptions,
        AssistantMessage,
        UserMessage,
        TextBlock,
        ClaudeSDKError,
        CLINotFoundError,
    )

    print("[OK] All imports successful!")
    print(f"[OK] query: {query}")
    print(f"[OK] ClaudeSDKClient: {ClaudeSDKClient}")
    print(f"[OK] ClaudeAgentOptions: {ClaudeAgentOptions}")

async def main():
    """Run all tests."""
    print("=" * 50)
    print("CLAUDE AGENT SDK - Installation Test")
    print("=" * 50)

    # Test imports first
    await test_import()

    # Test basic query (requires Claude Code CLI to be installed)
    print("\n" + "=" * 50)
    print("Testing query() function")
    print("=" * 50)
    await test_basic_query()

    print("\n" + "=" * 50)
    print("Test complete!")
    print("=" * 50)

if __name__ == "__main__":
    anyio.run(main)
