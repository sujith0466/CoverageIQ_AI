"""
E-Commerce System Sample Project
"""
from typing import List, Dict, Optional


class Cart:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.items: List[Dict] = []

    def add_to_cart(self, product_id: str, quantity: int, price: float) -> dict:
        """Add an item to the shopping cart."""
        if quantity <= 0:
            raise ValueError("Quantity must be positive.")
        if price < 0:
            raise ValueError("Price cannot be negative.")
        for item in self.items:
            if item["product_id"] == product_id:
                item["quantity"] += quantity
                return {"success": True, "items": len(self.items)}
        self.items.append({"product_id": product_id, "quantity": quantity, "price": price})
        return {"success": True, "items": len(self.items)}

    def remove_from_cart(self, product_id: str) -> dict:
        """Remove an item from the cart."""
        original_len = len(self.items)
        self.items = [i for i in self.items if i["product_id"] != product_id]
        removed = original_len - len(self.items)
        return {"success": removed > 0, "removed": removed}

    def checkout(self) -> dict:
        """Process cart checkout and calculate totals."""
        if not self.items:
            raise ValueError("Cart is empty.")
        subtotal = sum(i["price"] * i["quantity"] for i in self.items)
        tax = round(subtotal * 0.1, 2)
        total = round(subtotal + tax, 2)
        return {"success": True, "subtotal": subtotal, "tax": tax, "total": total}

    def process_payment(self, amount: float, method: str) -> dict:
        """Process payment for the cart total."""
        valid_methods = ["credit_card", "paypal", "bank_transfer"]
        if method not in valid_methods:
            raise ValueError(f"Invalid payment method. Must be one of {valid_methods}")
        checkout = self.checkout()
        if amount < checkout["total"]:
            raise ValueError("Insufficient payment amount.")
        change = round(amount - checkout["total"], 2)
        self.items.clear()
        return {"success": True, "paid": amount, "change": change, "method": method}

    def refund_order(self, order_id: str, reason: str) -> dict:
        """Initiate a refund for a given order."""
        if not order_id:
            raise ValueError("Order ID is required.")
        if not reason:
            raise ValueError("Refund reason is required.")
        return {"success": True, "order_id": order_id, "status": "REFUND_INITIATED"}

    def apply_discount(self, code: str) -> dict:
        """Apply a discount code to the cart."""
        discounts = {"SAVE10": 0.10, "SAVE20": 0.20, "HALF": 0.50}
        if code not in discounts:
            return {"success": False, "message": "Invalid discount code."}
        discount = discounts[code]
        return {"success": True, "discount_percent": discount * 100}
