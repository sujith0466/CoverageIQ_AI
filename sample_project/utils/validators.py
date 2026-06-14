import re

def validate_email(email: str) -> bool:
    """Validate email format."""
    if not email:
        return False
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return bool(re.match(pattern, email))

def validate_password_strength(password: str) -> bool:
    """Validate password strength."""
    if len(password) < 8:
        return False
    if not any(char.isdigit() for char in password):
        return False
    return True

def is_valid_username(username: str) -> bool:
    """Check if username is alphanumeric and proper length."""
    if len(username) < 3 or len(username) > 20:
        return False
    return username.isalnum()
