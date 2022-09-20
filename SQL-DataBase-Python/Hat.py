class Hat:
    def __init__(self, id, topping, supplier_id, quantity):
        self.id = id
        self.topping = topping
        self.supplier_id = supplier_id
        self.quantity = quantity


class _Hats:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, hat):
        self._conn.execute("""
        INSERT INTO hats (id, topping, supplier, quantity) VALUES (?,?,?,?)
        """, [hat.id, hat.topping, hat.supplier_id, hat.quantity])

    def find(self, hat_id):
        c = self._conn.cursor()

        c.execute("""
        SELECT * FROM hats WHERE id = ?""", [hat_id])

        return Hat(*c.fetchone())

    def find_first_supplier_of_topping(self, topping):
        c = self._conn.cursor()
        c.execute("""
        SELECT * FROM hats WHERE topping = ?""", [topping])

        all_hats_with_topping = c.fetchall()
        min_id = all_hats_with_topping[0][2]
        ##loop through all suppliers that supply this topping and gets the one with the minimum num of id
        for hat in all_hats_with_topping:
            i = hat[2]
            if min_id > i:
                min_id = i

        for hat in all_hats_with_topping:
            if hat[2] == min_id:
                return Hat(*hat)


    def decrement_quantity(self, hat):
        c = self._conn.cursor()
        c.execute("""
        UPDATE hats SET quantity = ? WHERE id = ?""", [hat.quantity-1, hat.id])

    def remove(self, hat_id):
        self._conn.execute("""
        DELETE FROM hats WHERE id = ?""", [hat_id])
