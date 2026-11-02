class Locker:
    def __init__(self, number, assigned_to):
        Locker.number = number
        Locker.assigned_to = assigned_to

    def label(self):
        return f"{self.number}: {self.assigned_to}"

class Entry:
    """Already written for you. Do not change it."""

    def __init__(self, client, days_old, unpaid):
        self.client = client
        self.days_old = days_old
        self.unpaid = unpaid

    def is_overdue(self):
        return self.unpaid and self.days_old > 30

    def __repr__(self):
        return f"Entry({self.client!r}, {self.days_old}, {self.unpaid})"


class Ledger:
    def __init__(self):
        self.entries = []

    def add(self, entry):
        self.entries.append(entry)

    def overdue(self):
        found = []
        for entry in self.entries:
            if entry.is_overdue():
                found.append(entry)
                return found
        return found
