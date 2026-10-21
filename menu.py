"""Restaurant menu stored in a dictionary (hash map): item_id -> details."""

MENU = {
    1:  {"name": "Veg Burger",        "category": "Burgers",  "price": 99},
    2:  {"name": "Chicken Burger",    "category": "Burgers",  "price": 149},
    3:  {"name": "Margherita Pizza",  "category": "Pizza",    "price": 249},
    4:  {"name": "Paneer Tikka Pizza","category": "Pizza",    "price": 299},
    5:  {"name": "Veg Biryani",       "category": "Mains",    "price": 189},
    6:  {"name": "Chicken Biryani",   "category": "Mains",    "price": 229},
    7:  {"name": "Paneer Butter Masala + 2 Roti", "category": "Mains", "price": 219},
    8:  {"name": "Pasta Alfredo",     "category": "Mains",    "price": 199},
    9:  {"name": "French Fries",      "category": "Snacks",   "price": 79},
    10: {"name": "Garlic Bread",      "category": "Snacks",   "price": 89},
    11: {"name": "Cold Coffee",       "category": "Drinks",   "price": 99},
    12: {"name": "Fresh Lime Soda",   "category": "Drinks",   "price": 59},
}


def show_menu():
    print("\n" + "=" * 52)
    print(f"{'ID':<4}{'Item':<34}{'Price':>8}")
    print("=" * 52)
    last_category = None
    for item_id, item in MENU.items():
        if item["category"] != last_category:
            print(f"-- {item['category']} --")
            last_category = item["category"]
        print(f"{item_id:<4}{item['name']:<34}{'Rs.' + str(item['price']):>8}")
    print("=" * 52)
