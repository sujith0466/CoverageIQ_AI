import os
import zipfile

# Create files
os.makedirs("sample_project/services", exist_ok=True)
os.makedirs("sample_project/utils", exist_ok=True)

validators_py = """import re

def validate_email(email: str) -> bool:
    \"\"\"Validate email format.\"\"\"
    if not email:
        return False
    pattern = r"^[\\w\\.-]+@[\\w\\.-]+\\.\\w+$"
    return bool(re.match(pattern, email))

def validate_password_strength(password: str) -> bool:
    \"\"\"Validate password strength.\"\"\"
    if len(password) < 8:
        return False
    if not any(char.isdigit() for char in password):
        return False
    return True

def is_valid_username(username: str) -> bool:
    \"\"\"Check if username is alphanumeric and proper length.\"\"\"
    if len(username) < 3 or len(username) > 20:
        return False
    return username.isalnum()
"""

auth_service_py = """from utils.validators import validate_email, validate_password_strength

class AuthService:
    def login(self, email: str, password: str) -> bool:
        \"\"\"Authenticate user.\"\"\"
        if not validate_email(email):
            return False
        if password == "secret":
            return True
        return False

    def register(self, email: str, password: str) -> dict:
        \"\"\"Register a new user.\"\"\"
        if not validate_email(email):
            raise ValueError("Invalid email")
        if not validate_password_strength(password):
            raise ValueError("Weak password")
        return {"id": 1, "email": email}

    def logout(self, user_id: int) -> bool:
        \"\"\"Logout user.\"\"\"
        print(f"Logging out {user_id}")
        return True

    def reset_password(self, email: str) -> bool:
        \"\"\"Reset password.\"\"\"
        pass
"""

user_service_py = """class UserService:
    def get_user(self, user_id: int) -> dict:
        \"\"\"Retrieve user by ID.\"\"\"
        if user_id <= 0:
            return None
        return {"id": user_id, "name": "John Doe"}

    def update_profile(self, user_id: int, data: dict) -> bool:
        \"\"\"Update user profile data.\"\"\"
        if not data:
            return False
        if "email" in data:
            print("Email update requested")
        return True

    def delete_account(self, user_id: int) -> bool:
        \"\"\"Delete user account.\"\"\"
        if user_id == 1:
            return False
        return True

    def calculate_profile_completion(self, user_id: int) -> int:
        \"\"\"Calculate profile completion percentage.\"\"\"
        base = 50
        bonus = 50
        return base + bonus
"""

payment_service_py = """class PaymentService:
    def process_payment(self, amount: float, currency: str) -> bool:
        \"\"\"Process a payment transaction.\"\"\"
        if amount <= 0:
            raise ValueError("Invalid amount")
        if currency not in ["USD", "EUR"]:
            raise ValueError("Unsupported currency")
        return True

    def refund_payment(self, transaction_id: str) -> bool:
        \"\"\"Refund a payment.\"\"\"
        if not transaction_id:
            return False
        if len(transaction_id) < 5:
            return False
        return True

    def calculate_tax(self, amount: float, region: str) -> float:
        \"\"\"Calculate tax based on region.\"\"\"
        if region == "US":
            return amount * 0.08
        if region == "EU":
            return amount * 0.20
        return amount * 0.10
        
    def generate_invoice(self, amount: float) -> str:
        \"\"\"Generate invoice ID.\"\"\"
        return f"INV-{int(amount)}"
"""

with open("sample_project/utils/validators.py", "w") as f:
    f.write(validators_py)
with open("sample_project/services/auth_service.py", "w") as f:
    f.write(auth_service_py)
with open("sample_project/services/user_service.py", "w") as f:
    f.write(user_service_py)
with open("sample_project/services/payment_service.py", "w") as f:
    f.write(payment_service_py)

# Generate Zip
with zipfile.ZipFile("sample_project.zip", "w") as zf:
    for root, _, files in os.walk("sample_project"):
        for file in files:
            zf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), "sample_project"))

# Generate coverage.xml
coverage_xml = """<?xml version="1.0" ?>
<coverage branch-rate="0.5" branches-covered="10" branches-valid="20" complexity="0" line-rate="0.65" lines-covered="35" lines-valid="55" timestamp="1710000000" version="6.2">
    <!-- Generated for CoverageIQ AI Testing -->
    <sources>
        <source>sample_project</source>
    </sources>
    <packages>
        <package branch-rate="0.5" complexity="0" line-rate="0.6" name="utils">
            <classes>
                <class branch-rate="0.5" complexity="0" filename="utils/validators.py" line-rate="0.5" name="validators.py">
                    <methods/>
                    <lines>
                        <!-- validate_email (Covered) -->
                        <line hits="1" number="5"/>
                        <line hits="1" number="6"/>
                        <line hits="1" number="7"/>
                        <line hits="1" number="8"/>
                        <!-- validate_password_strength (Partial) -->
                        <line hits="1" number="12"/>
                        <line hits="1" number="13"/>
                        <line hits="0" number="14"/>
                        <line hits="0" number="15"/>
                        <line hits="1" number="16"/>
                        <!-- is_valid_username (Uncovered) -->
                        <line hits="0" number="20"/>
                        <line hits="0" number="21"/>
                        <line hits="0" number="22"/>
                    </lines>
                </class>
            </classes>
        </package>
        <package branch-rate="0.5" complexity="0" line-rate="0.7" name="services">
            <classes>
                <class branch-rate="0.5" complexity="0" filename="services/auth_service.py" line-rate="0.6" name="auth_service.py">
                    <methods/>
                    <lines>
                        <!-- login (Covered) -->
                        <line hits="1" number="6"/>
                        <line hits="1" number="7"/>
                        <line hits="1" number="8"/>
                        <line hits="1" number="9"/>
                        <line hits="1" number="10"/>
                        <!-- register (Partial) -->
                        <line hits="1" number="14"/>
                        <line hits="0" number="15"/>
                        <line hits="1" number="16"/>
                        <line hits="1" number="17"/>
                        <line hits="1" number="18"/>
                        <!-- logout (Uncovered) -->
                        <line hits="0" number="22"/>
                        <line hits="0" number="23"/>
                        <!-- reset_password (0 Executable lines/Unknown, so no line hits) -->
                    </lines>
                </class>
                <class branch-rate="0.5" complexity="0" filename="services/user_service.py" line-rate="0.75" name="user_service.py">
                    <methods/>
                    <lines>
                        <!-- get_user (Covered) -->
                        <line hits="1" number="4"/>
                        <line hits="1" number="5"/>
                        <line hits="1" number="6"/>
                        <!-- update_profile (Partial) -->
                        <line hits="1" number="10"/>
                        <line hits="0" number="11"/>
                        <line hits="1" number="12"/>
                        <line hits="1" number="13"/>
                        <line hits="1" number="14"/>
                        <!-- delete_account (Uncovered) -->
                        <line hits="0" number="18"/>
                        <line hits="0" number="19"/>
                        <line hits="0" number="20"/>
                        <!-- calculate_profile_completion (Covered) -->
                        <line hits="1" number="24"/>
                        <line hits="1" number="25"/>
                        <line hits="1" number="26"/>
                    </lines>
                </class>
                <class branch-rate="0.5" complexity="0" filename="services/payment_service.py" line-rate="0.7" name="payment_service.py">
                    <methods/>
                    <lines>
                        <!-- process_payment (Covered) -->
                        <line hits="1" number="4"/>
                        <line hits="1" number="5"/>
                        <line hits="1" number="6"/>
                        <line hits="1" number="7"/>
                        <line hits="1" number="8"/>
                        <!-- refund_payment (Partial) -->
                        <line hits="1" number="12"/>
                        <line hits="1" number="13"/>
                        <line hits="0" number="14"/>
                        <line hits="0" number="15"/>
                        <line hits="1" number="16"/>
                        <!-- calculate_tax (Uncovered) -->
                        <line hits="0" number="20"/>
                        <line hits="0" number="21"/>
                        <line hits="0" number="22"/>
                        <line hits="0" number="23"/>
                        <line hits="0" number="24"/>
                        <!-- generate_invoice (Covered) -->
                        <line hits="1" number="28"/>
                    </lines>
                </class>
            </classes>
        </package>
    </packages>
</coverage>
"""

with open("coverage.xml", "w") as f:
    f.write(coverage_xml)
