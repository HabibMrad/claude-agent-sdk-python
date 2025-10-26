# How to Switch to Claude Pro (FREE with subscription)

## Current Status
You're currently using the **paid Anthropic API** which charges ~$0.016 per request.

## Steps to Switch to Claude Pro

### Step 1: Set Up Claude Pro Authentication

Open a **new Command Prompt or PowerShell window** and run:

```cmd
npx @anthropic-ai/claude-code setup-token
```

This will:
1. Open your web browser
2. Ask you to log in to your Claude.ai account (the one with Claude Pro subscription)
3. Generate a long-lived authentication token
4. Save it to your Claude Code configuration

### Step 2: Verify the Setup

After completing the setup, the SDK will automatically use your Claude Pro subscription instead of the paid API.

### Step 3: Test It

Run the test script to verify you're using Claude Pro:

```cmd
python test_claude_pro.py
```

**Expected Result:**
- Cost should show as `FREE (using Claude Pro subscription) [OK]`
- OR `total_cost_usd: 0` or `None`

**If still showing costs:**
- You might still have API credentials configured
- Try removing the `ANTHROPIC_API_KEY` environment variable completely
- Check if there's a `.env` file with API credentials

### Step 4: Update Your Scripts

Make sure all your scripts remove the API key:

```python
import os

# Remove API key to use Claude Pro
if 'ANTHROPIC_API_KEY' in os.environ:
    del os.environ['ANTHROPIC_API_KEY']
```

## Benefits of Claude Pro

- **FREE API calls** within your Claude Pro subscription limits
- No per-request charges
- Same features and capabilities
- Better for development and testing

## Troubleshooting

### If you don't have Claude Pro
You need a Claude Pro subscription ($20/month) at https://claude.ai/

### If setup-token fails
1. Make sure you're logged in to claude.ai in your browser
2. Try clearing browser cookies for claude.ai
3. Try a different browser

### If still seeing costs after setup
1. Check environment variables: `echo %ANTHROPIC_API_KEY%` (should be empty)
2. Check for `.env` files in your project
3. The Claude Code configuration might still have API credentials stored

## Additional Resources

- Claude Code Documentation: https://docs.claude.com/en/docs/claude-code
- Claude Pro: https://claude.ai/upgrade
