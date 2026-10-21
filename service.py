"""OrderManager: place, track, cancel and process orders."""
import time
from billing import calculate_bill
from models import Order, STATUS_FLOW
from order_queue import OrderProcessor
from storage import save_orders, load_orders


class OrderManager:
    def __init__(self, storage_path="data/orders.json"):
        self.storage_path = storage_path          # None = do not save to disk
        self.orders = {}                          # order_id -> Order (hash map)
        self.processor = OrderProcessor()
        self.next_id = 1001
        if storage_path:
            self.orders, self.next_id = load_orders(storage_path)
            for order in sorted(self.orders.values(), key=lambda o: o.order_id):
                if order.status == "PLACED":      # orders still waiting
                    self.processor.add(order)

    def _save(self):
        if self.storage_path:
            save_orders(self.storage_path, self.orders, self.next_id)

    def place_order(self, customer, phone, address, items, express=False, coupon=""):
        if not items:
            raise ValueError("Your cart is empty.")
        if not customer.strip():
            raise ValueError("Name cannot be empty.")
        if not (phone.isdigit() and len(phone) == 10):
            raise ValueError("Phone number must be 10 digits.")
        if len(address.strip()) < 5:
            raise ValueError("Please enter a proper delivery address.")
        order = Order(self.next_id, customer.strip(), phone, address.strip(),
                      dict(items), express, coupon.strip().upper())
        order.bill = calculate_bill(order.items, express, coupon)
        self.orders[order.order_id] = order
        self.processor.add(order)
        self.next_id += 1
        self._save()
        return order

    def get_order(self, order_id):
        if order_id not in self.orders:
            raise ValueError(f"Order #{order_id} not found.")
        return self.orders[order_id]

    def cancel_order(self, order_id):
        order = self.get_order(order_id)
        if order.status != "PLACED":
            raise ValueError(f"Order #{order_id} is {order.status} and cannot be cancelled.")
        self.processor.remove(order_id)
        order.status = "CANCELLED"
        self._save()
        return order

    def process_next(self, delay=0, on_step=None):
        """Take the highest-priority order and move it through every stage."""
        order = self.processor.next_order()
        if order is None:
            return None
        for status in STATUS_FLOW[1:]:
            order.status = status
            if on_step:
                on_step(order)
            if delay:
                time.sleep(delay)
        self._save()
        return order

    def pending_orders(self):
        return self.processor.pending()

    def history(self):
        return sorted(self.orders.values(), key=lambda o: o.order_id)
