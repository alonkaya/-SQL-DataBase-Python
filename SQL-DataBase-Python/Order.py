class Order:
    def __init__(self, id, location, hat_id):
        self.id = id
        self.location = location
        self.hat_id = hat_id


class _Orders:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, order):
        self._conn.execute("""
        INSERT INTO orders (id, location, hat) VALUES (?,?,?)""",
                           [order.id, order.location, order.hat_id])

    def find(self, order_id):
        c = self._conn.cursor()

        c.execute("""
        SELECT id, location, hat FROM orders WHERE id = ?""", [order_id])

        return Order(*c.fetchone())
