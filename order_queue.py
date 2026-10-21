"""Kitchen queue using a PRIORITY QUEUE (min-heap).

Express orders (priority 0) are cooked before normal orders (priority 1).
Orders with the same priority are served first-come-first-served (FIFO).
"""
import heapq
import itertools


class OrderProcessor:
    def __init__(self):
        self._heap = []                      # items: (priority, arrival_no, order)
        self._counter = itertools.count()    # arrival number keeps FIFO order

    def add(self, order):
        priority = 0 if order.express else 1
        heapq.heappush(self._heap, (priority, next(self._counter), order))

    def next_order(self):
        if not self._heap:
            return None
        return heapq.heappop(self._heap)[2]

    def remove(self, order_id):
        """Remove a cancelled order and rebuild the heap."""
        self._heap = [e for e in self._heap if e[2].order_id != order_id]
        heapq.heapify(self._heap)

    def pending(self):
        """Orders in the exact order they will be processed."""
        return [e[2] for e in sorted(self._heap)]

    def __len__(self):
        return len(self._heap)
