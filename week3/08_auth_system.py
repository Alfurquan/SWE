"""
Week 3 - Problem 8: Authentication System with JWT
Difficulty: Hard | Time Limit: 80 minutes | Google L5 Security Systems

PROBLEM STATEMENT:
Design secure authentication system with JWT tokens

OPERATIONS:
- register(username, password): Create new user account
- login(username, password): Authenticate and return JWT
- validateToken(token): Verify token validity
- refreshToken(refresh_token): Get new access token
- logout(token): Invalidate token

REQUIREMENTS:
- Secure password hashing (bcrypt/scrypt)
- JWT token generation and validation
- Refresh token rotation
- Rate limiting for auth attempts
- Support for token blacklisting

ALGORITHM:
JWT, password hashing, token rotation, security best practices

REAL-WORLD CONTEXT:
OAuth 2.0, OpenID Connect, enterprise SSO systems

FOLLOW-UP QUESTIONS:
- How to handle compromised tokens?
- Multi-factor authentication integration?
- Federated identity support?
- Session management at scale?

EXPECTED INTERFACE:
auth = AuthSystem(secret_key="your-secret-key")
user_id = auth.register("john_doe", "secure_password")
tokens = auth.login("john_doe", "secure_password")
is_valid = auth.validateToken(tokens["access_token"])
new_tokens = auth.refreshToken(tokens["refresh_token"])
auth.logout(tokens["access_token"])
"""

# Your implementation here
if __name__ == "__main__":
    # Add your test cases here
    pass
