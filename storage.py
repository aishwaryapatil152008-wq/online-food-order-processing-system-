"""Save and load orders in a JSON file."""
import json
import os
from models import Order


def save_orders(path, orders, next_id):
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    data = {"next_id": next_id, "orders": [o.to_dict() for o in orders.values()]}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def load_orders(path):
    if not os.path.exists(path):
        return {}, 1001
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        orders = {}
        for d in data["orders"]:
            order = Order.from_dict(d)
            orders[order.order_id] = order
        return orders, data["next_id"]
    except (json.JSONDecodeError, KeyError, TypeError):
        print("Warning: saved data was unreadable, starting fresh.")
        return {}, 1001
