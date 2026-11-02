class Order:
    """Yours to write. The tests import this name, so leave the class here."""


class PrintShop:
    def __init__(self):
        self.orders = []

    def add_order(self, customer, page_count, rush):
        self.orders.append(
            {"customer": customer, "page_count": page_count, "rush": rush}
        )

    def priority_orders(self):
        found = []
        for order in self.orders:
            if order["rush"] or order["page_count"] > 500:
                found.append(order)
        return found

class Sensor:
    def __init__(self, sensor_id, reading):
        self.sensor_id = sensor_id
        self.reading = reading

    def is_freezing(self):
        return self.reading <= 0

class Warehouse:
    crates = []

    def __init__(self, site):
        self.site = site

    def receive(self, item):
        self.crates.append(item)

    def crate_count(self):
        return len(self.crates)
