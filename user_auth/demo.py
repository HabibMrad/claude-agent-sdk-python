"""
Demo script for the User Authentication System.

This demonstrates all the features of the authentication system
powered by Claude Agent SDK.
"""

import anyio

from auth_system import UserAuthSystem


async def demo_registration():
    """Demonstrate user registration with various password strengths."""
    print("=" * 70)
    print("DEMO 1: User Registration with Password Validation")
    print("=" * 70)

    auth = UserAuthSystem()

    # Test 1: Weak password
    print("\n[Test 1] Registering user with weak password...")
    success, msg = await auth.register_user("alice", "123", "alice@example.com")
    print(f"Result: {'SUCCESS' if success else 'FAILED'}")
    print(f"Message: {msg}\n")

    # Test 2: Medium password
    print("[Test 2] Registering user with medium password...")
    success, msg = await auth.register_user("bob", "password123", "bob@example.com")
    print(f"Result: {'SUCCESS' if success else 'FAILED'}")
    print(f"Message: {msg}\n")

    # Test 3: Strong password
    print("[Test 3] Registering user with strong password...")
    success, msg = await auth.register_user(
        "charlie", "MyStr0ng!Pass2024", "charlie@example.com"
    )
    print(f"Result: {'SUCCESS' if success else 'FAILED'}")
    print(f"Message: {msg}\n")

    # Test 4: Duplicate username
    print("[Test 4] Attempting to register duplicate username...")
    success, msg = await auth.register_user(
        "charlie", "AnotherP@ss123", "charlie2@example.com"
    )
    print(f"Result: {'SUCCESS' if success else 'FAILED'}")
    print(f"Message: {msg}\n")


async def demo_login():
    """Demonstrate user login."""
    print("=" * 70)
    print("DEMO 2: User Login")
    print("=" * 70)

    auth = UserAuthSystem()

    # First, ensure we have a user
    await auth.register_user("testuser", "SecureP@ss123", "test@example.com")

    # Test 1: Successful login
    print("\n[Test 1] Logging in with correct credentials...")
    success, msg, token = await auth.login("testuser", "SecureP@ss123")
    print(f"Result: {'SUCCESS' if success else 'FAILED'}")
    print(f"Message: {msg}")
    if token:
        print(f"Session Token: {token[:20]}...{token[-10:]}\n")

    # Test 2: Wrong password
    print("[Test 2] Logging in with wrong password...")
    success, msg, token = await auth.login("testuser", "WrongPassword")
    print(f"Result: {'SUCCESS' if success else 'FAILED'}")
    print(f"Message: {msg}\n")

    # Test 3: Non-existent user
    print("[Test 3] Logging in with non-existent user...")
    success, msg, token = await auth.login("nobody", "password")
    print(f"Result: {'SUCCESS' if success else 'FAILED'}")
    print(f"Message: {msg}\n")

    return token if success else None


async def demo_session_management():
    """Demonstrate session verification and logout."""
    print("=" * 70)
    print("DEMO 3: Session Management")
    print("=" * 70)

    auth = UserAuthSystem()

    # Create a session
    await auth.register_user("sessionuser", "MyP@ssw0rd!", "session@example.com")
    success, msg, token = await auth.login("sessionuser", "MyP@ssw0rd!")

    if token:
        # Verify session
        print("\n[Test 1] Verifying valid session...")
        is_valid, username = auth.verify_session(token)
        print(f"Valid: {is_valid}")
        print(f"Username: {username}\n")

        # Logout
        print("[Test 2] Logging out...")
        logged_out = auth.logout(token)
        print(f"Logout successful: {logged_out}\n")

        # Verify session after logout
        print("[Test 3] Verifying session after logout...")
        is_valid, username = auth.verify_session(token)
        print(f"Valid: {is_valid}")
        print(f"Username: {username}\n")


async def demo_security_analysis():
    """Demonstrate Claude-powered security analysis."""
    print("=" * 70)
    print("DEMO 4: Security Analysis (Claude-Powered)")
    print("=" * 70)

    auth = UserAuthSystem()

    # Create a user and login
    await auth.register_user("analyst", "Analyz3r!2024", "analyst@example.com")
    await auth.login("analyst", "Analyz3r!2024")

    print("\n[Analyzing account security using Claude...]")
    analysis = await auth.analyze_security_risk("analyst")
    print("\nSecurity Analysis:")
    print("-" * 70)
    print(analysis)
    print("-" * 70)


async def demo_complete_workflow():
    """Demonstrate a complete authentication workflow."""
    print("\n" + "=" * 70)
    print("DEMO 5: Complete Authentication Workflow")
    print("=" * 70)

    auth = UserAuthSystem()

    # Step 1: Register
    print("\nStep 1: Register new user...")
    success, msg = await auth.register_user(
        "workflowuser", "C0mpl3x!Pass", "workflow@example.com"
    )
    print(f"Registration: {msg}")

    if not success:
        return

    # Step 2: Login
    print("\nStep 2: Login...")
    success, msg, token = await auth.login("workflowuser", "C0mpl3x!Pass")
    print(f"Login: {msg}")

    if not token:
        return

    # Step 3: Verify session
    print("\nStep 3: Verify session...")
    is_valid, username = auth.verify_session(token)
    print(f"Session valid: {is_valid} for user: {username}")

    # Step 4: Get user info
    print("\nStep 4: Get user information...")
    user_info = auth.get_user_info(username)
    print(f"User Info:")
    for key, value in user_info.items():
        print(f"  {key}: {value}")

    # Step 5: Security analysis
    print("\nStep 5: Security analysis...")
    analysis = await auth.analyze_security_risk(username)
    print(f"Analysis: {analysis}")

    # Step 6: Logout
    print("\nStep 6: Logout...")
    logged_out = auth.logout(token)
    print(f"Logged out: {logged_out}")


async def main():
    """Run all demos."""
    print("\n")
    print("*" * 70)
    print("  User Authentication System - Powered by Claude Agent SDK")
    print("*" * 70)
    print()

    try:
        # Run individual demos
        await demo_registration()
        await demo_login()
        await demo_session_management()
        await demo_security_analysis()
        await demo_complete_workflow()

        print("\n" + "=" * 70)
        print("All demos completed!")
        print("=" * 70)
        print("\nDatabase saved to: user_auth/users_db.json")
        print("Check the file to see stored users (passwords are hashed).")

    except Exception as e:
        print(f"\nError during demo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    anyio.run(main)
