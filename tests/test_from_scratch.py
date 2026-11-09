import ast
import inspect
import textwrap


def attributes_set_on(instance):
    """The attribute names stored on this instance rather than on its class.

    An attribute written in the class body is shared by every instance, so it
    does not appear here. One assigned to self in __init__ does.
    """
    return set(vars(instance))


def calls_hasattr(function):
    """Whether the function's source calls the built-in hasattr()."""
    source = textwrap.dedent(inspect.getsource(function))
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "hasattr":
            return True
    return False


class FakeBike:
    """A stand-in whose flag says one thing and whose method says another.

    A Station that asks each bike is_rentable() follows the method. One that
    reads needs_repair itself follows the flag, and these tests can tell which.
    """

    def __init__(self, serial, rentable):
        self.serial = serial
        self.needs_repair = rentable  # deliberately the opposite of what is_rentable() says
        self._rentable = rentable

    def is_rentable(self):
        return self._rentable


from from_scratch import Bike, Member, Ride, Station, has_attribute


TEST_SUITE_NAME = "From Scratch Tests"


# ---------- Question 1: Bike ----------

def test_bike_stores_its_own_data():
    """Bike - __init__ stores the serial, station and repair flag on the instance"""
    bike = Bike("A1", "Grand Army", False)

    assert bike.serial == "A1"
    assert bike.station == "Grand Army"
    assert bike.needs_repair is False
    assert attributes_set_on(bike) >= {"serial", "station", "needs_repair"}, \
        "Assign all three to self inside __init__, so each bike carries its own."


def test_bike_reports_whether_it_can_be_rented():
    """Bike - is_rentable is True only when the bike does not need repair"""
    assert Bike("A1", "Grand Army", False).is_rentable() is True
    assert Bike("B7", "Borough Hall", True).is_rentable() is False


def test_two_bikes_hold_separate_data():
    """Bike - two instances do not share attribute values"""
    good = Bike("A1", "Grand Army", False)
    broken = Bike("B7", "Borough Hall", True)

    assert good.serial == "A1"
    assert broken.serial == "B7"
    assert good.is_rentable() != broken.is_rentable()


# ---------- Question 2: A Bike That Prints and Compares ----------

def test_bike_repr_names_the_bike():
    """Bike.__repr__ - returns the class name and all three values"""
    bike = Bike("A1", "Grand Army", False)

    assert repr(bike) == "Bike('A1', 'Grand Army', False)"
    assert repr([bike]) == "[Bike('A1', 'Grand Army', False)]", \
        "__repr__ has to return the text, so that a list of bikes can show it too."


def test_bikes_with_the_same_serial_are_equal():
    """Bike.__eq__ - two bikes with the same serial are ==, but are not the same object"""
    first_report = Bike("A1", "Grand Army", False)
    second_report = Bike("A1", "Borough Hall", True)

    assert first_report == second_report
    assert first_report is not second_report


def test_bikes_with_different_serials_are_not_equal():
    """Bike.__eq__ - two bikes with different serials are not =="""
    assert Bike("A1", "Grand Army", False) != Bike("A2", "Grand Army", False)


# ---------- Question 3: Station ----------

def test_station_starts_empty_and_docks_bikes():
    """Station - __init__ stores the name and capacity, and dock() adds a bike"""
    station = Station("Grand Army", 20)
    bike = Bike("A1", "Grand Army", False)

    assert station.name == "Grand Army"
    assert station.capacity == 20
    assert station.bikes == []

    station.dock(bike)
    assert len(station.bikes) == 1
    assert station.bikes[0] is bike


def test_rentable_and_repair_list_return_new_lists():
    """Station - rentable() and repair_list() return new lists and leave the station's bikes alone"""
    station = Station("Grand Army", 20)
    station.dock(Bike("A1", "Grand Army", True))
    station.dock(Bike("A2", "Grand Army", False))

    assert [bike.serial for bike in station.rentable()] == ["A2"]
    assert [bike.serial for bike in station.repair_list()] == ["A1"]

    station.rentable().clear()
    assert len(station.bikes) == 2, "Return a new list, so a caller who changes it cannot change the station."


def test_station_asks_each_bike():
    """Station - asks each bike is_rentable() instead of reading its needs_repair flag"""
    station = Station("Grand Army", 20)
    station.dock(FakeBike("A1", rentable=True))
    station.dock(FakeBike("A2", rentable=False))

    assert [bike.serial for bike in station.rentable()] == ["A1"], \
        "Ask each bike bike.is_rentable(); the rule lives in Bike."
    assert [bike.serial for bike in station.repair_list()] == ["A2"]


def test_new_station_has_no_bikes_to_list():
    """Station - a new station returns empty lists"""
    station = Station("Empty", 8)

    assert station.rentable() == []
    assert station.repair_list() == []


# ---------- Question 4: Member and Ride ----------

def test_member_stores_its_name():
    """Member - __init__ stores the name on the instance"""
    ada = Member("Ada")

    assert ada.name == "Ada"
    assert "name" in attributes_set_on(ada)


def test_ride_holds_a_member_and_a_bike():
    """Ride - holds the Member object and the Bike object themselves, plus the minutes"""
    ada = Member("Ada")
    bike = Bike("A1", "Grand Army", False)
    ride = Ride(ada, bike, 45)

    assert ride.member is ada, "Store the whole Member object, not just its name."
    assert ride.bike is bike, "Store the whole Bike object, not just its serial."
    assert ride.minutes == 45


def test_ride_reports_whether_it_is_long():
    """Ride - is_long() is True at 30 minutes or more"""
    ada = Member("Ada")
    bike = Bike("A1", "Grand Army", False)

    assert Ride(ada, bike, 30).is_long() is True
    assert Ride(ada, bike, 29).is_long() is False


def test_ride_summary_reaches_through_its_objects():
    """Ride - summary() reads the member's name and the bike's serial through the ride"""
    ada = Member("Ada")
    ride = Ride(ada, Bike("A1", "Grand Army", False), 45)

    assert ride.summary() == "Ada on A1: 45 min"

    ada.name = "Ada L."
    assert ride.summary() == "Ada L. on A1: 45 min", \
        "Read self.member.name when summary() runs, so the ride always shows the member's current name."


# ---------- Question 5: has_attribute ----------

def test_has_attribute_finds_instance_attributes():
    """has_attribute - True for an attribute __init__ stored on the instance"""
    assert has_attribute(Bike("A1", "Grand Army", False), "serial") is True


def test_has_attribute_finds_methods():
    """has_attribute - True for a method, which is stored on the class"""
    assert has_attribute(Bike("A1", "Grand Army", False), "is_rentable") is True, \
        "A method is stored on the class, not on the instance, but the bike can still use it."


def test_has_attribute_reports_a_missing_name():
    """has_attribute - False for a name the object does not have"""
    assert has_attribute(Station("Grand Army", 20), "serial") is False
    assert has_attribute(Bike("A1", "Grand Army", False), "minutes") is False


def test_has_attribute_works_on_any_object():
    """has_attribute - works on built-in values as well as your own classes"""
    assert has_attribute("A1", "upper") is True
    assert has_attribute([], "serial") is False


def test_has_attribute_does_not_call_hasattr():
    """has_attribute - finds the answer without calling hasattr()"""
    assert not calls_hasattr(has_attribute), "Write your own check instead of calling hasattr()."
