"""Check current Claude Code authentication status."""

import os
import anyio
from claude_agent_sdk import query, SystemMessage

# Remove API key to check other auth methods
if 'ANTHROPIC_API_KEY' in os.environ:
    del os.environ['ANTHROPIC_API_KEY']

async def main():
    print("=" * 70)
    print("Claude Code Authentication Status Check")
    print("=" * 70)
    print()

    try:
        async for message in query(prompt="Hello, what is 1+1?"):
            if isinstance(message, SystemMessage) and message.subtype == 'init':
                print("Authentication Information:")
                print("-" * 70)

                data = message.data

                # Key authentication fields
                print(f"API Key Source: {data.get('apiKeySource', 'Not specified')}")
                print(f"Model: {data.get('model', 'Not specified')}")
                print(f"Claude Code Version: {data.get('claude_code_version', 'Not specified')}")
                print(f"Session ID: {data.get('session_id', 'Not specified')}")

                # Check if there's any billing/subscription info
                if 'billing' in data:
                    print(f"Billing Info: {data['billing']}")

                if 'subscription' in data:
                    print(f"Subscription Info: {data['subscription']}")

                print()
                print("Full init data:")
                print("-" * 70)
                for key, value in data.items():
                    if key not in ['tools', 'mcp_servers', 'slash_commands', 'agents', 'skills', 'plugins']:
                        print(f"  {key}: {value}")

                break  # We only need the init message

    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}")

if __name__ == "__main__":
    anyio.run(main)
