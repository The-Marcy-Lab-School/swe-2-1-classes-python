import ast
import inspect
import textwrap


def attributes_set_on(instance):
    """The attribute names stored on this instance rather than on its class.

    An attribute written in the class body is shared by every instance, so it
    does not appear here. One assigned to self in __init__ does.
    """
    return set(vars(instance))


def assigns_in_class_body(cls):
    """The names assigned directly in a class body, read with the ast module.

    The source is parsed rather than searched as text, so a name mentioned in a
    comment or a docstring never counts.
    """
    source = textwrap.dedent(inspect.getsource(cls))
    body = ast.parse(source).body[0].body
    names = set()
    for node in body:
        if isinstance(node, ast.Assign):
            names.update(t.id for t in node.targets if isinstance(t, ast.Name))
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            names.add(node.target.id)
    return names


from from_scratch import Bike, Member, Ride, Station, build_bikes


TEST_SUITE_NAME = "From Scratch Tests"


def test_bike_stores_its_own_data():
    """Bike - __init__ stores the serial, station and repair flag on the instance"""
    bike = Bike("A1", "Grand Army", False)

    assert bike.serial == "A1"
    assert bike.station == "Grand Army"
    assert bike.needs_repair is False
    assert attributes_set_on(bike) >= {"serial", "station", "needs_repair"}, \
        "Assign all three to self inside __init__, so each bike carries its own."


def test_bike_reports_whether_it_can_be_rented():
    """Bike - is_rentable is False when the bike needs repair"""
    assert Bike("A1", "Grand Army", False).is_rentable() is True
    assert Bike("B7", "Borough Hall", True).is_rentable() is False


def test_two_bikes_hold_separate_data():
    """Bike - two instances do not share attribute values"""
    good = Bike("A1", "Grand Army", False)
    broken = Bike("B7", "Borough Hall", True)

    assert good.serial == "A1"
    assert broken.serial == "B7"
    assert good.is_rentable() != broken.is_rentable()


def stocked_dock():
    station = Station("Grand Army", 20)
    station.dock(Bike("A1", "Grand Army", True))
    station.dock(Bike("A2", "Grand Army", False))
    station.dock(Bike("A3", "Grand Army", False))
    return station


def test_station_stores_the_bikes_it_is_given():
    """Station - dock stores Bike objects, not copies of their data"""
    station = Station("Grand Army", 20)
    first = Bike("A1", "Grand Army", False)
    station.dock(first)

    found = station.rentable()
    assert len(found) == 1
    assert isinstance(found[0], Bike), \
        "The station holds Bike objects, so what comes back is a Bike."
    assert found[0] is first


def test_station_filters_without_handing_over_its_list():
    """Station - rentable returns a new list and leaves the station's list alone"""
    station = stocked_dock()

    rentable = station.rentable()
    assert [bike.serial for bike in rentable] == ["A2", "A3"]
    assert rentable is not station.bikes, \
        "Build a new list. Handing back the station's own list lets a caller edit it."

    rentable.clear()
    assert len(station.rentable()) == 2, \
        "Clearing the returned list emptied the station, so the same list was handed over."


def test_station_handles_an_empty_dock_and_the_repair_list():
    """Station - repair_list finds the broken bikes, and a new station returns []"""
    station = stocked_dock()

    assert [bike.serial for bike in station.repair_list()] == ["A1"]
    assert Station("Empty", 8).rentable() == []
    assert Station("Empty", 8).repair_list() == []


def test_ride_holds_both_objects():
    """Ride - stores the Member and the Bike themselves, not their values"""
    ada = Member("Ada", 2)
    bike = Bike("A1", "Grand Army", False)
    ride = Ride(ada, bike, 45)

    assert ride.member is ada, \
        "Store the Member object, so a change to the member shows up here."
    assert ride.bike is bike
    assert ride.member.name == "Ada"
    assert ride.bike.serial == "A1"


def test_ride_holds_the_minutes_for_the_pair():
    """Ride - two rides by one member keep separate minutes"""
    ada = Member("Ada", 2)
    long_ride = Ride(ada, Bike("A1", "Grand Army", False), 45)
    short_ride = Ride(ada, Bike("A2", "Grand Army", False), 10)

    assert long_ride.minutes == 45
    assert short_ride.minutes == 10
    assert not hasattr(ada, "minutes"), \
        "The minutes belong to the ride. A member taking two rides has two."


def test_ride_reports_its_length_and_summary():
    """Ride - is_long starts at 30 minutes, and summary names both objects"""
    ada = Member("Ada", 2)
    assert Ride(ada, Bike("A1", "X", False), 30).is_long() is True
    assert Ride(ada, Bike("A1", "X", False), 29).is_long() is False

    text = Ride(Member("Zo", 2), Bike("B7", "Borough Hall", False), 12).summary()
    assert "Zo" in text
    assert "B7" in text
    assert "12" in text


SERIALS = ["A1", "A2", "B7"]
STATIONS = ["Grand Army", "Grand Army", "Borough Hall"]
FLAGS = [True, False, False]


def test_build_bikes_returns_one_bike_per_position():
    """build_bikes - returns Bike objects with the matching three values"""
    fleet = build_bikes(SERIALS, STATIONS, FLAGS)

    assert len(fleet) == 3
    assert all(isinstance(bike, Bike) for bike in fleet), \
        "Return Bike objects, not tuples or dictionaries."
    assert fleet[2].serial == "B7"
    assert fleet[2].station == "Borough Hall"
    assert fleet[2].needs_repair is False


def test_build_bikes_survives_sorting():
    """build_bikes - sorting the result keeps each bike's values together"""
    fleet = build_bikes(SERIALS, STATIONS, FLAGS)
    fleet.sort(key=lambda bike: bike.serial, reverse=True)

    assert fleet[0].serial == "B7"
    assert fleet[0].station == "Borough Hall"


def test_build_bikes_handles_empty_lists():
    """build_bikes - three empty lists make no bikes"""
    assert build_bikes([], [], []) == []
    assert len(build_bikes(["A1"], ["Grand Army"], [True])) == 1
