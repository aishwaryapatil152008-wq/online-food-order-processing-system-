"""Bill calculation and receipt printing."""
from menu import MENU

GST_RATE = 0.05
DELIVERY_FEE = 40
FREE_DELIVERY_ABOVE = 500
EXPRESS_FEE = 30

# code -> (type, value, minimum subtotal)
COUPONS = {
    "WELCOME10": ("percent", 10, 0),
    "SAVE50":    ("flat",    50, 300),
}


def calculate_bill(items, express=False, coupon=""):
    subtotal = sum(MENU[i]["price"] * q for i, q in items.items())
    discount, message = 0.0, ""
    code = coupon.strip().upper()
    if code:
        if code not in COUPONS:
            message = f"Coupon '{code}' is not valid."
        else:
            kind, value, minimum = COUPONS[code]
            if subtotal < minimum:
                message = f"{code} needs a minimum order of Rs.{minimum}."
            else:
                discount = subtotal * value / 100 if kind == "percent" else value
                message = f"Coupon {code} applied!"
    discount = min(discount, subtotal)
    taxable = subtotal - discount
    gst = taxable * GST_RATE
    delivery = 0 if subtotal >= FREE_DELIVERY_ABOVE else DELIVERY_FEE
    express_fee = EXPRESS_FEE if express else 0
    total = taxable + gst + delivery + express_fee
    return {
        "subtotal": round(subtotal, 2), "discount": round(discount, 2),
        "gst": round(gst, 2), "delivery_fee": delivery,
        "express_fee": express_fee, "total": round(total, 2),
        "coupon_message": message,
    }


def format_receipt(order):
    b = order.bill
    lines = ["", "=" * 44, f"  RECEIPT - Order #{order.order_id}", "=" * 44,
             f"Customer : {order.customer}", f"Phone    : {order.phone}",
             f"Address  : {order.address}", f"Placed at: {order.created_at}",
             f"Type     : {'EXPRESS' if order.express else 'Normal'}",
             f"Status   : {order.status}", "-" * 44]
    for item_id, qty in order.items.items():
        item = MENU[item_id]
        lines.append(f"{item['name'][:24]:<24} {qty:>2} x {item['price']:<4} = {item['price'] * qty:>6.2f}")
    lines.append("-" * 44)
    lines.append(f"{'Subtotal':<30}{b['subtotal']:>12.2f}")
    if b["discount"]:
        lines.append(f"{'Discount':<30}{-b['discount']:>12.2f}")
    lines.append(f"{'GST (5%)':<30}{b['gst']:>12.2f}")
    lines.append(f"{'Delivery fee':<30}{b['delivery_fee']:>12.2f}")
    if b["express_fee"]:
        lines.append(f"{'Express fee':<30}{b['express_fee']:>12.2f}")
    lines.append("=" * 44)
    lines.append(f"{'TOTAL (Rs.)':<30}{b['total']:>12.2f}")
    lines.append("=" * 44)
    return "\n".join(lines)
