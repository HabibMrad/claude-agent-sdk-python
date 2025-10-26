"""
User Authentication System using Claude Agent SDK.

This module demonstrates how to build a user authentication system
that leverages Claude for validation, security checks, and user feedback.
"""

import hashlib
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import anyio

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ClaudeSDKClient,
    TextBlock,
)


class UserAuthSystem:
    """User authentication system with Claude-powered validation."""

    def __init__(self, db_path: str = "user_auth/users_db.json"):
        """Initialize the authentication system.

        Args:
            db_path: Path to the JSON file storing user data
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(exist_ok=True)
        self.sessions = {}  # In-memory session storage
        self._load_users()

    def _load_users(self):
        """Load users from the database file."""
        if self.db_path.exists():
            with open(self.db_path, 'r') as f:
                self.users = json.load(f)
        else:
            self.users = {}

    def _save_users(self):
        """Save users to the database file."""
        with open(self.db_path, 'w') as f:
            json.dump(self.users, f, indent=2)

    @staticmethod
    def _hash_password(password: str) -> str:
        """Hash a password using SHA-256.

        Args:
            password: Plain text password

        Returns:
            Hashed password
        """
        return hashlib.sha256(password.encode()).hexdigest()

    async def validate_password_strength(self, password: str) -> tuple[bool, str]:
        """Use Claude to validate password strength.

        Args:
            password: Password to validate

        Returns:
            Tuple of (is_valid, feedback_message)
        """
        options = ClaudeAgentOptions(
            system_prompt="You are a security expert. Analyze password strength and provide concise feedback.",
            max_turns=1
        )

        prompt = f"""Analyze this password strength: "{password}"

Provide a brief assessment (1-2 sentences) covering:
- Is it strong enough? (min 8 chars, mix of upper/lower/numbers/symbols)
- Security concerns if any

Format: "VALID: message" or "INVALID: message"
"""

        async with ClaudeSDKClient(options=options) as client:
            await client.query(prompt)

            async for msg in client.receive_response():
                if isinstance(msg, AssistantMessage):
                    for block in msg.content:
                        if isinstance(block, TextBlock):
                            response = block.text.strip()
                            # Remove markdown formatting
                            response_clean = response.replace("**", "").strip()

                            if "VALID:" in response_clean or "VALID" in response_clean[:20]:
                                # Check if it's truly valid or has concerns
                                if "extremely weak" in response.lower() or "very weak" in response.lower():
                                    return False, response
                                return True, response
                            elif "INVALID:" in response_clean:
                                return False, response
                            else:
                                # Parse response for indicators
                                is_valid = ("meets" in response.lower() and "requirement" in response.lower()) or \
                                          ("strong" in response.lower() and "weak" not in response.lower())
                                return is_valid, response

        return False, "Unable to validate password"

    async def register_user(self, username: str, password: str, email: str) -> tuple[bool, str]:
        """Register a new user with Claude-powered validation.

        Args:
            username: Desired username
            password: User's password
            email: User's email

        Returns:
            Tuple of (success, message)
        """
        # Check if user already exists
        if username in self.users:
            return False, f"Username '{username}' already exists"

        # Validate password strength using Claude
        is_valid, feedback = await self.validate_password_strength(password)
        if not is_valid:
            return False, f"Weak password: {feedback}"

        # Validate email format using Claude
        email_valid = await self._validate_email(email)
        if not email_valid:
            return False, "Invalid email format"

        # Create user
        self.users[username] = {
            "password_hash": self._hash_password(password),
            "email": email,
            "created_at": datetime.now().isoformat(),
            "last_login": None
        }

        self._save_users()
        return True, f"User '{username}' registered successfully! {feedback}"

    async def _validate_email(self, email: str) -> bool:
        """Validate email format using Claude.

        Args:
            email: Email to validate

        Returns:
            True if valid, False otherwise
        """
        options = ClaudeAgentOptions(
            system_prompt="You are a validator. Answer only 'YES' or 'NO'.",
            max_turns=1
        )

        async with ClaudeSDKClient(options=options) as client:
            await client.query(f"Is this a valid email format? {email}")

            async for msg in client.receive_response():
                if isinstance(msg, AssistantMessage):
                    for block in msg.content:
                        if isinstance(block, TextBlock):
                            response = block.text.strip().upper()
                            return "YES" in response

        return False

    async def login(self, username: str, password: str) -> tuple[bool, str, Optional[str]]:
        """Authenticate a user.

        Args:
            username: Username
            password: Password

        Returns:
            Tuple of (success, message, session_token)
        """
        if username not in self.users:
            return False, "Invalid username or password", None

        # Check password
        password_hash = self._hash_password(password)
        if self.users[username]["password_hash"] != password_hash:
            return False, "Invalid username or password", None

        # Create session
        session_token = hashlib.sha256(
            f"{username}{datetime.now().isoformat()}".encode()
        ).hexdigest()

        self.sessions[session_token] = {
            "username": username,
            "login_time": datetime.now(),
            "expires_at": datetime.now() + timedelta(hours=24)
        }

        # Update last login
        self.users[username]["last_login"] = datetime.now().isoformat()
        self._save_users()

        return True, f"Welcome back, {username}!", session_token

    def verify_session(self, session_token: str) -> tuple[bool, Optional[str]]:
        """Verify if a session token is valid.

        Args:
            session_token: Session token to verify

        Returns:
            Tuple of (is_valid, username)
        """
        if session_token not in self.sessions:
            return False, None

        session = self.sessions[session_token]

        # Check if expired
        if datetime.now() > session["expires_at"]:
            del self.sessions[session_token]
            return False, None

        return True, session["username"]

    def logout(self, session_token: str) -> bool:
        """Logout a user by invalidating their session.

        Args:
            session_token: Session token to invalidate

        Returns:
            True if successful, False otherwise
        """
        if session_token in self.sessions:
            del self.sessions[session_token]
            return True
        return False

    def get_user_info(self, username: str) -> Optional[dict]:
        """Get user information (excluding password hash).

        Args:
            username: Username to lookup

        Returns:
            User info dict or None
        """
        if username not in self.users:
            return None

        user_data = self.users[username].copy()
        user_data.pop("password_hash", None)  # Don't expose password hash
        return user_data

    async def analyze_security_risk(self, username: str) -> str:
        """Use Claude to analyze account security.

        Args:
            username: Username to analyze

        Returns:
            Security analysis report
        """
        if username not in self.users:
            return "User not found"

        user_info = self.get_user_info(username)

        options = ClaudeAgentOptions(
            system_prompt="You are a security analyst. Provide brief security recommendations.",
            max_turns=1
        )

        prompt = f"""Analyze this user account security:
- Created: {user_info['created_at']}
- Last login: {user_info['last_login'] or 'Never'}

Provide 2-3 brief security recommendations."""

        async with ClaudeSDKClient(options=options) as client:
            await client.query(prompt)

            async for msg in client.receive_response():
                if isinstance(msg, AssistantMessage):
                    for block in msg.content:
                        if isinstance(block, TextBlock):
                            return block.text

        return "Unable to analyze security"
