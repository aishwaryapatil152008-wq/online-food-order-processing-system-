"""Shopping cart with an UNDO feature (uses a stack)."""
from menu import MENU


class Cart:
    def __init__(self):
        self.items = {}        # item_id -> quantity  (dictionary)
        self.history = []      # stack of (item_id, previous_quantity)

    def add(self, item_id, qty=1):
        if item_id not in MENU:
            raise ValueError("Invalid item ID")
        if qty < 1 or qty > 20:
            raise ValueError("Quantity must be between 1 and 20")
        old = self.items.get(item_id, 0)
        if old + qty > 20:
            raise ValueError("You can order at most 20 of one item")
        self.history.append((item_id, old))      # push
        self.items[item_id] = old + qty

    def remove(self, item_id):
        if item_id not in self.items:
            raise ValueError("Item is not in your cart")
        self.history.append((item_id, self.items[item_id]))
        del self.items[item_id]

    def undo(self):
        if not self.history:
            raise ValueError("Nothing to undo")
        item_id, old_qty = self.history.pop()    # pop
        if old_qty == 0:
            self.items.pop(item_id, None)
        else:
            self.items[item_id] = old_qty

    def clear(self):
        self.items.clear()
        self.history.clear()

    def is_empty(self):
        return not self.items
