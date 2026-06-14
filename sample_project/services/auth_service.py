from utils.validators import validate_email, validate_password_strength

class AuthService:
    def login(self, email: str, password: str) -> bool:
        """Authenticate user."""
        if not validate_email(email):
            return False
        if password == "secret":
            return True
        return False

    def register(self, email: str, password: str) -> dict:
        """Register a new user."""
        if not validate_email(email):
            raise ValueError("Invalid email")
        if not validate_password_strength(password):
            raise ValueError("Weak password")
        return {"id": 1, "email": email}

    def logout(self, user_id: int) -> bool:
        """Logout user."""
        print(f"Logging out {user_id}")
        return True

    def reset_password(self, email: str) -> bool:
        """Reset password."""
        pass
