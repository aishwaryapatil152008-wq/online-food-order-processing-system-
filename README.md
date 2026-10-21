# 🍔 Online Food Order Processing System

> 👥 **Team 

- Yash Sachin Bonde (32251)
- Sakshi Sunil Zunzunwala (32252)
- Aishwarya Pramod Patil (32253)
- Vicky Harishkumar Badmera (32254)
- Divya Dilip Tirodkar (32255)

## ✨1. Features

| 🎯 Feature | 📝 Description |
|---|---|
| 📜 Menu | 12 items in 5 categories (burgers, pizza, mains, snacks, drinks) |
| 🛒 Cart | Add, remove and **undo** changes |
| 🎟️ Coupons | `WELCOME10` (10% off) and `SAVE50` (Rs.50 off on orders of Rs.300+) |
| 🧾 Billing | Subtotal, discount, 5% GST, delivery fee (free above Rs.500), express fee (Rs.30) |
| ⚡ Express orders | Jump ahead of normal orders in the kitchen queue |
| 🔍 Track order | See the current status and the full receipt |
| ❌ Cancel order | Allowed only while the order is still `PLACED` |
| 📚 Order history | See all past orders |
| ✅ Input checks | Phone must be 10 digits, quantity limits, empty cart and invalid IDs are handled |
| 🧪 Unit tests | 9 automatic tests included |

## 🧠 2. Data structures used (the DSA part)

| 🏗️ Data structure | 📍 Where it is used | 💡 Why |
|---|---|---|
| 🗂️ **Dictionary (hash map)** | `menu.py`, cart items, all orders by ID | Find an item or order instantly by its ID |
| 🥞 **Stack** | `cart.py` – undo history | Last change is undone first (LIFO) |
| ⛰️ **Priority queue (min-heap)** | `order_queue.py` – kitchen queue | Express orders (priority 0) come out before normal orders (priority 1) |
| 🚶 **Queue behaviour (FIFO)** | Same heap with an arrival counter | Orders with equal priority are served in the order they arrived |
| 📋 **List** | Pending orders, order history | Display and sorting |
| 🔄 **State flow** | `models.py` – `STATUS_FLOW` | Moves an order step by step through its stages |

**⏱️ Time complexity:** add to queue `O(log n)`, take next order `O(log n)`, find order by ID `O(1)`, cart add/undo `O(1)`.

## 📁 3. Project structure

```
online-food-order-processing/
├── 📜 menu.py          # Menu dictionary and menu display
├── 📦 models.py        # Order class and status flow
├── 🛒 cart.py          # Cart with undo (stack)
├── 🧾 billing.py       # Bill calculation, coupons, receipt
├── ⛰️  order_queue.py   # Kitchen priority queue (heap)
├── 💾 storage.py       # Save / load orders (JSON)
├── ⚙️  service.py       # OrderManager: place, cancel, process, track
├── 💻 main.py          # Main menu program (run this!)
├── 🎬 demo.py          # Automatic demo (great for presentations)
├── 🧪 test_orders.py   # Unit tests
├── 🗂️  data/            # orders.json is created here
├── 📋 requirements.txt
└── 📘 README.md
```

## ▶️ 4. How to run

You need **🐍 Python 3.8 or newer**.

```bash
# 💻 Run the interactive app
python main.py

# 🎬 Watch an automatic demo (nothing is saved)
python demo.py

# 🧪 Run the tests
python -m unittest -v
```

### 🧭 Main menu options

```
 1. View menu              7. Track an order
 2. Add item to cart       8. Cancel an order
 3. Remove item from cart  9. Process next order (kitchen)
 4. Undo last cart change 10. View kitchen queue
 5. View cart & bill      11. Order history
 6. Place order            0. Exit
```

### 🚶 Quick walk-through

1. Choose **2** → add a *Margherita Pizza* (ID 3) ➕
2. Choose **5** → see your cart 🛒
3. Choose **6** → enter name, 10-digit phone, address, express (y/n) and a coupon 🎟️
4. Choose **10** → see the kitchen queue 📋
5. Choose **9** → the kitchen processes the next order 🍳➡️🚚➡️✅
6. Choose **7** → track your order with its receipt 🧾

## 🎬 6. Sample output (from `python demo.py`)

```
3) Kitchen queue (express first, then first-come-first-served)
   1. Order #1002 - Diya [EXPRESS]
   2. Order #1001 - Aarav
   3. Order #1003 - Rohan

5) Processing orders
   Order #1002: PREPARING
   Order #1002: OUT FOR DELIVERY
   Order #1002: DELIVERED
```

Order #1002 was placed **second** but is cooked **first**, because it is an ⚡ express order. 🎉

### 🧾 Bill example

Diya's order: 2 × Chicken Biryani + 2 × Cold Coffee, express, coupon `WELCOME10`

```
Subtotal      656.00
Discount      -65.60   (10% off)
GST (5%)       29.52
Delivery        0.00   (free above Rs.500)
Express fee    30.00
TOTAL         649.92
```

## ⚠️ 6. Limitations

- 💻 Console only – no website or mobile app
- 💳 No real payment, login or live delivery tracking
- 🕒 "Cooking" is simulated with short delays
- 👤 One user at a time (no multiple users at once)
- 💾 Data is stored in a simple JSON file, not a real database

## 🚀 7. Future improvements

- 🌐 Web app using Flask or Django
- 🗄️ Database such as SQLite or MySQL
- 🔐 User accounts and login
- 💳 Payment gateway
- ⏱️ Estimated delivery time and delivery partner assignment
- ⭐ Ratings and reviews
- 📱 Mobile app
