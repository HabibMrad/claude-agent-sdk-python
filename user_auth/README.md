## # User Authentication System

A complete user authentication system powered by **Claude Agent SDK**, demonstrating how to build AI-enhanced security features.

## Features

### 🔐 Core Authentication
- **User Registration** - Create new user accounts
- **User Login** - Authenticate with username/password
- **Session Management** - Token-based sessions with expiration
- **Secure Password Storage** - SHA-256 hashed passwords

### 🤖 Claude-Powered Features
- **Password Strength Validation** - Claude analyzes password security
- **Email Format Validation** - Claude verifies email addresses
- **Security Risk Analysis** - Claude provides account security recommendations
- **Intelligent Feedback** - User-friendly validation messages

## Quick Start

### Run the Demo

```bash
cd user_auth
python demo.py
```

This will run all demonstration scenarios showing:
1. Registration with various password strengths
2. Login with correct/incorrect credentials
3. Session verification and logout
4. Security analysis using Claude
5. Complete authentication workflow

### Use in Your Code

```python
import anyio
from user_auth import UserAuthSystem

async def main():
    auth = UserAuthSystem()

    # Register a new user
    success, msg = await auth.register_user(
        username="john",
        password="MyStr0ng!Pass",
        email="john@example.com"
    )
    print(msg)

    # Login
    success, msg, token = await auth.login("john", "MyStr0ng!Pass")
    if success:
        print(f"Logged in! Token: {token}")

    # Verify session
    is_valid, username = auth.verify_session(token)
    if is_valid:
        print(f"Session valid for: {username}")

    # Logout
    auth.logout(token)

anyio.run(main)
```

## API Reference

### UserAuthSystem

#### `__init__(db_path: str = "user_auth/users_db.json")`
Initialize the authentication system.

#### `async register_user(username: str, password: str, email: str) -> tuple[bool, str]`
Register a new user with Claude-powered validation.

**Returns:** `(success, message)`

**Features:**
- Checks for duplicate usernames
- Validates password strength using Claude
- Validates email format using Claude
- Stores hashed passwords securely

#### `async login(username: str, password: str) -> tuple[bool, str, Optional[str]]`
Authenticate a user.

**Returns:** `(success, message, session_token)`

**Features:**
- Verifies username and password
- Creates 24-hour session token
- Updates last login timestamp

#### `verify_session(session_token: str) -> tuple[bool, Optional[str]]`
Verify if a session token is valid.

**Returns:** `(is_valid, username)`

#### `logout(session_token: str) -> bool`
Invalidate a session token.

**Returns:** `True` if successful

#### `get_user_info(username: str) -> Optional[dict]`
Get user information (excludes password hash).

**Returns:** User info dict or None

#### `async analyze_security_risk(username: str) -> str`
Use Claude to analyze account security.

**Returns:** Security analysis report

## How It Works

### Claude Integration

The system uses Claude Agent SDK to enhance security validation:

1. **Password Strength Analysis**
   ```python
   # Claude analyzes password characteristics
   is_valid, feedback = await auth.validate_password_strength("MyPassword123!")
   # Returns: (True, "Strong password with good character variety")
   ```

2. **Email Validation**
   ```python
   # Claude validates email format
   is_valid = await auth._validate_email("user@example.com")
   # Returns: True
   ```

3. **Security Risk Analysis**
   ```python
   # Claude provides security recommendations
   analysis = await auth.analyze_security_risk("john")
   # Returns: Personalized security advice
   ```

### Data Storage

User data is stored in JSON format:

```json
{
  "username": {
    "password_hash": "hashed_password",
    "email": "user@example.com",
    "created_at": "2025-10-25T...",
    "last_login": "2025-10-25T..."
  }
}
```

### Session Management

- Sessions are stored in-memory
- 24-hour expiration by default
- Token-based authentication
- Automatic cleanup on logout

## Demo Output Examples

### Password Validation

```
[Test 1] Registering user with weak password...
Result: FAILED
Message: Weak password: Password is too short and lacks complexity.
         Add uppercase, numbers, and symbols.

[Test 3] Registering user with strong password...
Result: SUCCESS
Message: User 'charlie' registered successfully!
         Strong password with excellent character variety.
```

### Security Analysis

```
Security Analysis:
------------------------------------------------------------------
Based on the account details:
1. Enable two-factor authentication for additional security
2. Consider updating password every 90 days
3. Review login activity regularly for suspicious access
------------------------------------------------------------------
```

## Requirements

- Python 3.10+
- `claude-agent-sdk`
- Claude Pro subscription (for free usage) or API credits

## Architecture

```
user_auth/
├── __init__.py          # Package initialization
├── auth_system.py       # Core authentication logic
├── demo.py             # Demonstration scripts
├── README.md           # This file
└── users_db.json       # User database (created on first use)
```

## Security Notes

⚠️ **This is a demonstration project**. For production use:

1. Use stronger password hashing (bcrypt, argon2)
2. Store sessions in a database, not memory
3. Add rate limiting for login attempts
4. Implement HTTPS for all communications
5. Add email verification
6. Implement password reset functionality
7. Add multi-factor authentication
8. Use environment variables for sensitive config
9. Add comprehensive logging
10. Regular security audits

## Why This Demonstrates the SDK Well

This authentication system showcases:

1. **ClaudeSDKClient Usage** - Interactive validation with Claude
2. **Real-World Application** - Practical authentication features
3. **AI-Enhanced Security** - Claude provides intelligent feedback
4. **Async Programming** - Proper async/await patterns
5. **Error Handling** - Graceful handling of validation failures
6. **State Management** - Session and user data management
7. **Claude Agent Options** - Custom system prompts and configurations

## License

MIT
