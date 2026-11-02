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


class Member:
    def __init__(self, name, limit):
        Member.name = name
        Member.limit = limit

    def label(self):
        return f"{self.name} ({self.limit} rides)"


class Ride:
    def __init__(self, member, bike, minutes):
        self.member = member
        self.bike = bike
        self.minutes = minutes

    def is_long(self):
        return self.minutes >= 30

    def __repr__(self):
        print(f"Ride({self.member.name!r}, {self.bike.serial!r}, {self.minutes})")
