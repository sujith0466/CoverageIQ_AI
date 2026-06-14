"""
Authentication System Sample Project
"""
import hashlib
import secrets
from typing import Optional


class AuthService:
    def __init__(self):
        self.users: dict = {}
        self.sessions: dict = {}
        self.reset_tokens: dict = {}

    def register(self, username: str, email: str, password: str) -> dict:
        """Register a new user account."""
        if not username or not email or not password:
            raise ValueError("Username, email, and password are required.")
        if username in self.users:
            raise ValueError("Username already exists.")
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters.")
        hashed = self._hash_password(password)
        self.users[username] = {"email": email, "password": hashed, "verified": False}
        return {"success": True, "username": username}

    def login(self, username: str, password: str) -> dict:
        """Log in a user and create a session token."""
        if username not in self.users:
            raise ValueError("User not found.")
        user = self.users[username]
        if not self._verify_password(password, user["password"]):
            raise ValueError("Invalid password.")
        token = secrets.token_hex(32)
        self.sessions[token] = username
        return {"success": True, "token": token}

    def logout(self, token: str) -> dict:
        """Invalidate a session token."""
        if token not in self.sessions:
            raise ValueError("Invalid session token.")
        del self.sessions[token]
        return {"success": True}

    def reset_password(self, email: str) -> dict:
        """Generate a password reset token."""
        user = next((u for u, d in self.users.items() if d["email"] == email), None)
        if not user:
            raise ValueError("Email not found.")
        token = secrets.token_hex(16)
        self.reset_tokens[token] = user
        return {"success": True, "reset_token": token}

    def verify_email(self, username: str, code: str) -> dict:
        """Verify a user's email address with a code."""
        if username not in self.users:
            raise ValueError("User not found.")
        expected_code = self._generate_verification_code(username)
        if code != expected_code:
            raise ValueError("Invalid verification code.")
        self.users[username]["verified"] = True
        return {"success": True, "verified": True}

    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def _verify_password(self, plain: str, hashed: str) -> bool:
        return self._hash_password(plain) == hashed

    def _generate_verification_code(self, username: str) -> str:
        return hashlib.md5(username.encode()).hexdigest()[:6].upper()
