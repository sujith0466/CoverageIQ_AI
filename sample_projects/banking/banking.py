"""
Banking System Sample Project
"""

class BankAccount:
    def __init__(self, account_id: str, owner: str, balance: float = 0.0):
        self.account_id = account_id
        self.owner = owner
        self.balance = balance
        self.transactions = []

    def deposit(self, amount: float) -> dict:
        """Deposit money into the account."""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        self.transactions.append({"type": "deposit", "amount": amount})
        return {"success": True, "balance": self.balance}

    def withdraw(self, amount: float) -> dict:
        """Withdraw money from the account."""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance:
            raise ValueError("Insufficient funds.")
        self.balance -= amount
        self.transactions.append({"type": "withdrawal", "amount": amount})
        return {"success": True, "balance": self.balance}

    def transfer(self, target_account: 'BankAccount', amount: float) -> dict:
        """Transfer funds to another account."""
        self.withdraw(amount)
        target_account.deposit(amount)
        return {"success": True, "transferred": amount}

    def calculate_interest(self, rate: float, years: int) -> float:
        """Calculate compound interest."""
        if rate < 0 or years < 0:
            raise ValueError("Rate and years must be non-negative.")
        return round(self.balance * ((1 + rate) ** years - 1), 2)

    def get_transaction_history(self) -> list:
        """Return full transaction history."""
        return self.transactions

    def close_account(self) -> dict:
        """Close the account and zero out balance."""
        final_balance = self.balance
        self.balance = 0.0
        return {"closed": True, "refunded": final_balance}
