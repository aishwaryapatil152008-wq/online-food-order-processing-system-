"""Order data model."""
from dataclasses import dataclass, field, asdict
from datetime import datetime

# Normal life of an order
STATUS_FLOW = ["PLACED", "PREPARING", "OUT FOR DELIVERY", "DELIVERED"]


@dataclass
class Order:
    order_id: int
    customer: str
    phone: str
    address: str
    items: dict                      # item_id -> quantity
    express: bool = False
    coupon: str = ""
    status: str = "PLACED"
    bill: dict = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def to_dict(self):
        return asdict(self)

    @staticmethod
    def from_dict(data):
        data = dict(data)
        data["items"] = {int(k): v for k, v in data["items"].items()}  # JSON keys are text
        return Order(**data)
