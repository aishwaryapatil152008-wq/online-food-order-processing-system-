"""Non-interactive demo (nothing is saved).  Run: python demo.py"""
from billing import format_receipt
from cart import Cart
from service import OrderManager

manager = OrderManager(storage_path=None)

print("1) Cart with UNDO (stack)")
cart = Cart()
cart.add(3, 1)
cart.add(9, 2)
cart.add(11, 1)
print("   Cart:", cart.items)
cart.undo()
print("   After undo:", cart.items)

print("\n2) Placing three orders")
o1 = manager.place_order("Aarav", "9876543210", "12 MG Road, Pune", {1: 2, 9: 1})
o2 = manager.place_order("Diya", "9123456780", "45 Baner Road, Pune", {6: 2, 11: 2},
                         express=True, coupon="WELCOME10")
o3 = manager.place_order("Rohan", "9988776655", "7 FC Road, Pune", {3: 1, 4: 1, 10: 1},
                         coupon="SAVE50")
print(format_receipt(o2))

print("\n3) Kitchen queue (express first, then first-come-first-served)")
for pos, o in enumerate(manager.pending_orders(), 1):
    print(f"   {pos}. Order #{o.order_id} - {o.customer} {'[EXPRESS]' if o.express else ''}")

print("\n4) Cancel order", o1.order_id)
manager.cancel_order(o1.order_id)
print("   Status:", manager.get_order(o1.order_id).status)

print("\n5) Processing orders")
while True:
    done = manager.process_next(on_step=lambda o: print(f"   Order #{o.order_id}: {o.status}"))
    if done is None:
        break

print("\n6) Final history")
for o in manager.history():
    print(f"   #{o.order_id} | {o.customer:<6} | {o.status:<10} | Rs.{o.bill['total']}")
