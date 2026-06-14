class UserService:
    def get_user(self, user_id: int) -> dict:
        """Retrieve user by ID."""
        if user_id <= 0:
            return None
        return {"id": user_id, "name": "John Doe"}

    def update_profile(self, user_id: int, data: dict) -> bool:
        """Update user profile data."""
        if not data:
            return False
        if "email" in data:
            print("Email update requested")
        return True

    def delete_account(self, user_id: int) -> bool:
        """Delete user account."""
        if user_id == 1:
            return False
        return True

    def calculate_profile_completion(self, user_id: int) -> int:
        """Calculate profile completion percentage."""
        base = 50
        bonus = 50
        return base + bonus
