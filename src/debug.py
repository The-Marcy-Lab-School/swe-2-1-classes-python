# Each class below has one bug. The README describes what goes wrong.


class Mechanic:
    def __init__(self, name, shift):
        name = name
        self.shift = shift

    def label(self):
        return f"{self.name} ({self.shift} shift)"


class RepairTicket:
    def __init__(self, serial, problem):
        self.serial = serial
        self.problem = problem

    def describe():
        return f"{self.serial}: {self.problem}"
