class Bike:
    """Already written for you. Do not change it."""

    def __init__(self, serial, station, needs_repair):
        self.serial = serial
        self.station = station
        self.needs_repair = needs_repair

    def is_rentable(self):
        return not self.needs_repair

    def __repr__(self):
        return f"Bike({self.serial!r}, {self.station!r}, {self.needs_repair})"


class Station:
    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity
        self.bikes = []

    def dock(self, bike):
        self.bikes.append(bike)

    def repair_list(self):
        found = []
        for bike in list(self.bikes):
            if bike.needs_repair:
                found.append(bike)
                self.bikes.remove(bike)
        return found


class Member:
    def __init__(self, name, limit):
        self.name = name
        self.limit = limit
        self.rides = []

    def take(self, member, bike, minutes):
        self.rides.append(
            {"member": member, "bike": bike, "minutes": minutes}
        )

    def long_rides(self):
        found = []
        for ride in self.rides:
            if ride["minutes"] >= 30:
                found.append(ride)
        return found


class Ride:
    """Yours to write. The tests import this name, so leave the class here."""


def total_minutes(names, minutes):
    total = 0
    for index in range(len(names)):
        total += minutes[index]
    return total
