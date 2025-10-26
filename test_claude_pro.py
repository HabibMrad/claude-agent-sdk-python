"""Test Claude Agent SDK with Claude Pro subscription (no API charges)."""

import os
import anyio
from claude_agent_sdk import query, AssistantMessage, TextBlock, ResultMessage

# IMPORTANT: Remove API key to use Claude Pro instead of paid API
if 'ANTHROPIC_API_KEY' in os.environ:
    del os.environ['ANTHROPIC_API_KEY']
    print("[OK] Removed ANTHROPIC_API_KEY - will use Claude Pro subscription")
else:
    print("[OK] No ANTHROPIC_API_KEY found - will use Claude Pro subscription")

print()

async def main():
    print("=" * 60)
    print("Testing with Claude Pro Authentication (FREE with subscription)")
    print("=" * 60)
    print()

    try:
        async for message in query(prompt="What is 5 + 5? Answer in one sentence."):
            # Print all message types to see authentication info
            if hasattr(message, 'data') and isinstance(message.data, dict):
                if 'apiKeySource' in message.data:
                    print(f"\n[AUTH INFO] API Key Source: {message.data['apiKeySource']}")
                if 'forceLoginMethod' in message.data:
                    print(f"[AUTH INFO] Login Method: {message.data.get('forceLoginMethod')}")
            if isinstance(message, AssistantMessage):
                print("Response from Claude:")
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"  {block.text}")
                print()
            elif isinstance(message, ResultMessage):
                print(f"\n{'=' * 60}")
                print(f"Session completed successfully!")
                print(f"  Duration: {message.duration_ms}ms")
                print(f"  API Duration: {message.duration_api_ms}ms")
                print(f"  Turns: {message.num_turns}")

                # Check if we're using Claude Pro (cost should be 0 or None)
                if message.total_cost_usd is None or message.total_cost_usd == 0:
                    print(f"  Cost: FREE (using Claude Pro subscription) [OK]")
                else:
                    print(f"  Cost: ${message.total_cost_usd:.6f} (using paid API)")
                print(f"{'=' * 60}")

    except Exception as e:
        print(f"\n[ERROR] {type(e).__name__}: {e}")
        print("\nPossible issues:")
        print("1. Claude Code CLI not installed: npm install -g @anthropic-ai/claude-code")
        print("2. Not logged in to Claude Pro: Run 'claude login' or 'claude-code login'")
        print("3. CLI path incorrect (Windows users may need to specify cli_path)")

if __name__ == "__main__":
    anyio.run(main)
