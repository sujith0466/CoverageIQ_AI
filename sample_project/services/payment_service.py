class PaymentService:
    def process_payment(self, amount: float, currency: str) -> bool:
        """Process a payment transaction."""
        if amount <= 0:
            raise ValueError("Invalid amount")
        if currency not in ["USD", "EUR"]:
            raise ValueError("Unsupported currency")
        return True

    def refund_payment(self, transaction_id: str) -> bool:
        """Refund a payment."""
        if not transaction_id:
            return False
        if len(transaction_id) < 5:
            return False
        return True

    def calculate_tax(self, amount: float, region: str) -> float:
        """Calculate tax based on region."""
        if region == "US":
            return amount * 0.08
        if region == "EU":
            return amount * 0.20
        return amount * 0.10
        
    def generate_invoice(self, amount: float) -> str:
        """Generate invoice ID."""
        return f"INV-{int(amount)}"
