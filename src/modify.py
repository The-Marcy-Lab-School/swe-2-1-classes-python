# Change the code below as the Modify question asks.
# This class is separate from your From Scratch answers, so you can start here at any time.


# ---------- Question 6: Dock ----------

class Dock:
    def __init__(self, station, number):
        self.station = station
        self.number = number

    def __repr__(self):
        return f"Dock(station={self.station!r}, number={self.number!r})"

    def __eq__(self, other):
        return self.station == other.station and self.number == other.number
