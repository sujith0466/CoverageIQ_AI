"""
Inventory Management Sample Project
"""
from typing import List, Dict, Optional
from datetime import datetime


class InventoryManager:
    def __init__(self):
        self.inventory: Dict[str, dict] = {}
        self.transaction_log: List[dict] = []

    def add_item(self, item_id: str, name: str, quantity: int, unit_price: float) -> dict:
        """Add a new item or update stock for existing item."""
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")
        if unit_price < 0:
            raise ValueError("Unit price cannot be negative.")
        if item_id in self.inventory:
            self.inventory[item_id]["quantity"] += quantity
        else:
            self.inventory[item_id] = {
                "name": name, "quantity": quantity, "unit_price": unit_price
            }
        self._log("ADD", item_id, quantity)
        return {"success": True, "item_id": item_id}

    def remove_item(self, item_id: str, quantity: int) -> dict:
        """Remove stock from an item."""
        if item_id not in self.inventory:
            raise ValueError("Item not found.")
        if quantity <= 0:
            raise ValueError("Quantity must be positive.")
        if self.inventory[item_id]["quantity"] < quantity:
            raise ValueError("Insufficient stock.")
        self.inventory[item_id]["quantity"] -= quantity
        self._log("REMOVE", item_id, quantity)
        return {"success": True, "remaining": self.inventory[item_id]["quantity"]}

    def update_stock(self, item_id: str, new_quantity: int) -> dict:
        """Directly set stock quantity for an item."""
        if item_id not in self.inventory:
            raise ValueError("Item not found.")
        if new_quantity < 0:
            raise ValueError("Quantity cannot be negative.")
        old_qty = self.inventory[item_id]["quantity"]
        self.inventory[item_id]["quantity"] = new_quantity
        self._log("UPDATE", item_id, new_quantity - old_qty)
        return {"success": True, "old_quantity": old_qty, "new_quantity": new_quantity}

    def generate_report(self) -> dict:
        """Generate a full inventory report with totals."""
        if not self.inventory:
            return {"success": True, "items": [], "total_value": 0.0}
        items = []
        total_value = 0.0
        for item_id, data in self.inventory.items():
            value = data["quantity"] * data["unit_price"]
            total_value += value
            items.append({
                "item_id": item_id,
                "name": data["name"],
                "quantity": data["quantity"],
                "unit_price": data["unit_price"],
                "total_value": round(value, 2)
            })
        return {
            "success": True,
            "items": items,
            "total_items": len(items),
            "total_value": round(total_value, 2)
        }

    def get_low_stock_alerts(self, threshold: int = 5) -> List[dict]:
        """Return items below a stock threshold."""
        return [
            {"item_id": k, "name": v["name"], "quantity": v["quantity"]}
            for k, v in self.inventory.items()
            if v["quantity"] <= threshold
        ]

    def _log(self, action: str, item_id: str, quantity: int):
        self.transaction_log.append({
            "timestamp": datetime.utcnow().isoformat(),
            "action": action,
            "item_id": item_id,
            "quantity": quantity
        })
