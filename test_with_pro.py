"""Test SDK with Claude Pro (no API key)."""

import os
import anyio
from claude_agent_sdk import query, ClaudeAgentOptions

# Remove API key to force use of Claude Pro
if 'ANTHROPIC_API_KEY' in os.environ:
    del os.environ['ANTHROPIC_API_KEY']
    print("Removed ANTHROPIC_API_KEY from environment")

async def main():
    print("Testing with Claude Pro authentication...")
    print("-" * 50)

    # Configure to use the correct CLI path
    options = ClaudeAgentOptions(
        cli_path=r"C:\Users\Admin\AppData\Roaming\npm\claude.cmd"
    )

    try:
        async for message in query(
            prompt="What is 3 + 3? Answer in one sentence.",
            options=options
        ):
            print(f"{message}\n")
    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}")

if __name__ == "__main__":
    anyio.run(main)
