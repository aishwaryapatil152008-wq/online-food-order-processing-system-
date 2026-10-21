"""Run tests:  python -m unittest -v"""
import os
import tempfile
import unittest

from billing import calculate_bill
from cart import Cart
from service import OrderManager

ADDR = "12 Main Road, Pune"


class TestBilling(unittest.TestCase):
    def test_plain_bill(self):
        b = calculate_bill({1: 2})            # 2 x Rs.99 = 198
        self.assertEqual(b["subtotal"], 198)
        self.assertEqual(b["gst"], 9.9)
        self.assertEqual(b["delivery_fee"], 40)
        self.assertEqual(b["total"], 247.9)

    def test_free_delivery(self):
        self.assertEqual(calculate_bill({3: 2})["delivery_fee"], 40)  # Rs.498 -> not free
        self.assertEqual(calculate_bill({3: 3})["delivery_fee"], 0)   # Rs.747 -> free

    def test_coupons(self):
        self.assertEqual(calculate_bill({3: 1}, coupon="WELCOME10")["discount"], 24.9)
        self.assertEqual(calculate_bill({1: 1}, coupon="SAVE50")["discount"], 0)   # below minimum
        self.assertIn("not valid", calculate_bill({1: 1}, coupon="FAKE")["coupon_message"])


class TestCart(unittest.TestCase):
    def test_undo(self):
        c = Cart()
        c.add(1, 2)
        c.add(1, 1)
        c.undo()
        self.assertEqual(c.items, {1: 2})
        c.undo()
        self.assertTrue(c.is_empty())

    def test_invalid(self):
        c = Cart()
        with self.assertRaises(ValueError):
            c.add(99)
        with self.assertRaises(ValueError):
            c.add(1, 0)
        with self.assertRaises(ValueError):
            c.undo()


class TestOrders(unittest.TestCase):
    def setUp(self):
        self.m = OrderManager(storage_path=None)

    def test_express_first_then_fifo(self):
        a = self.m.place_order("A", "9999999991", ADDR, {1: 1})
        b = self.m.place_order("B", "9999999992", ADDR, {1: 1}, express=True)
        c = self.m.place_order("C", "9999999993", ADDR, {1: 1})
        self.assertEqual([o.order_id for o in self.m.pending_orders()],
                         [b.order_id, a.order_id, c.order_id])
        self.assertEqual(self.m.process_next().order_id, b.order_id)

    def test_cancel_rules(self):
        a = self.m.place_order("A", "9999999991", ADDR, {1: 1})
        self.m.cancel_order(a.order_id)
        self.assertEqual(a.status, "CANCELLED")
        self.assertEqual(len(self.m.pending_orders()), 0)
        b = self.m.place_order("B", "9999999992", ADDR, {1: 1})
        self.m.process_next()
        with self.assertRaises(ValueError):
            self.m.cancel_order(b.order_id)       # already delivered

    def test_validation(self):
        with self.assertRaises(ValueError):
            self.m.place_order("A", "123", ADDR, {1: 1})        # bad phone
        with self.assertRaises(ValueError):
            self.m.place_order("A", "9999999991", ADDR, {})     # empty cart

    def test_persistence(self):
        path = os.path.join(tempfile.mkdtemp(), "orders.json")
        m1 = OrderManager(storage_path=path)
        o = m1.place_order("A", "9999999991", ADDR, {1: 2, 9: 1})
        m2 = OrderManager(storage_path=path)
        self.assertEqual(m2.get_order(o.order_id).items, {1: 2, 9: 1})
        self.assertEqual(len(m2.pending_orders()), 1)         # still waiting


if __name__ == "__main__":
    unittest.main()
