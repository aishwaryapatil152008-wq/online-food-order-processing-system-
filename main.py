"""Online Food Order Processing - console application.  Run: python main.py"""
from billing import calculate_bill, format_receipt
from cart import Cart
from menu import MENU, show_menu
from service import OrderManager

MENU_TEXT = """
================ ONLINE FOOD ORDERING ================
 1. View menu              7. Track an order
 2. Add item to cart       8. Cancel an order
 3. Remove item from cart  9. Process next order (kitchen)
 4. Undo last cart change 10. View kitchen queue
 5. View cart & bill      11. Order history
 6. Place order            0. Exit
======================================================"""


def ask_int(prompt, low=None, high=None):
    while True:
        text = input(prompt).strip()
        try:
            value = int(text)
        except ValueError:
            print("  Please enter a number.")
            continue
        if (low is not None and value < low) or (high is not None and value > high):
            print(f"  Enter a number between {low} and {high}.")
            continue
        return value


def show_cart(cart):
    if cart.is_empty():
        print("\n  Your cart is empty.")
        return
    print("\nYour cart:")
    for item_id, qty in cart.items.items():
        item = MENU[item_id]
        print(f"  {item['name']:<32} {qty} x Rs.{item['price']} = Rs.{item['price'] * qty}")
    bill = calculate_bill(cart.items)
    print(f"  Subtotal: Rs.{bill['subtotal']}  (GST and delivery are added at checkout)")


def place_order(manager, cart):
    if cart.is_empty():
        print("\n  Your cart is empty. Add some items first.")
        return
    show_cart(cart)
    name = input("\nYour name: ")
    phone = input("Phone (10 digits): ").strip()
    address = input("Delivery address: ")
    express = input("Express delivery (+Rs.30, cooked first)? (y/n): ").strip().lower() == "y"
    coupon = input("Coupon code (WELCOME10 / SAVE50, or press Enter): ")
    try:
        order = manager.place_order(name, phone, address, cart.items, express, coupon)
    except ValueError as err:
        print(f"\n  Could not place order: {err}")
        return
    if order.bill["coupon_message"]:
        print("  " + order.bill["coupon_message"])
    print(format_receipt(order))
    print(f"\nOrder placed! Your order ID is #{order.order_id}")
    cart.clear()


def main():
    manager = OrderManager()
    cart = Cart()
    while True:
        print(MENU_TEXT)
        choice = input("Choose an option: ").strip()
        try:
            if choice == "1":
                show_menu()
            elif choice == "2":
                show_menu()
                item_id = ask_int("Item ID: ")
                qty = ask_int("Quantity: ")
                cart.add(item_id, qty)
                print(f"  Added {qty} x {MENU[item_id]['name']}.")
            elif choice == "3":
                show_cart(cart)
                cart.remove(ask_int("Item ID to remove: "))
                print("  Item removed.")
            elif choice == "4":
                cart.undo()
                print("  Last change undone.")
                show_cart(cart)
            elif choice == "5":
                show_cart(cart)
            elif choice == "6":
                place_order(manager, cart)
            elif choice == "7":
                print(format_receipt(manager.get_order(ask_int("Order ID: "))))
            elif choice == "8":
                order = manager.cancel_order(ask_int("Order ID to cancel: "))
                print(f"  Order #{order.order_id} cancelled.")
            elif choice == "9":
                done = manager.process_next(
                    delay=0.5, on_step=lambda o: print(f"  Order #{o.order_id}: {o.status}"))
                print("  No orders waiting." if done is None else f"  Order #{done.order_id} completed!")
            elif choice == "10":
                pending = manager.pending_orders()
                if not pending:
                    print("\n  Kitchen queue is empty.")
                for pos, o in enumerate(pending, 1):
                    print(f"  {pos}. Order #{o.order_id} - {o.customer} "
                          f"{'[EXPRESS]' if o.express else ''}")
            elif choice == "11":
                history = manager.history()
                if not history:
                    print("\n  No orders yet.")
                for o in history:
                    print(f"  #{o.order_id} | {o.customer:<15} | {o.status:<17} | Rs.{o.bill['total']}")
            elif choice == "0":
                print("Thank you! Goodbye.")
                break
            else:
                print("  Invalid option. Try again.")
        except ValueError as err:
            print(f"  Error: {err}")


if __name__ == "__main__":
    main()
