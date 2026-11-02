from modify import Bike, Member, Ride, Station, total_minutes


TEST_SUITE_NAME = "Modify Tests"


def stocked_station():
    station = Station("Grand Army", 20)
    station.dock(Bike("A1", "Grand Army", True))
    station.dock(Bike("A2", "Grand Army", False))
    station.dock(Bike("B7", "Grand Army", True))
    return station


def test_repair_list_finds_the_broken_bikes():
    """Station - repair_list returns the Bike objects needing repair"""
    station = stocked_station()
    broken = station.repair_list()

    assert [bike.serial for bike in broken] == ["A1", "B7"]
    assert all(isinstance(bike, Bike) for bike in broken)


def test_repair_list_can_be_called_twice():
    """Station - repair_list leaves the station alone, so it answers the same twice"""
    station = stocked_station()

    first = [bike.serial for bike in station.repair_list()]
    second = [bike.serial for bike in station.repair_list()]

    assert first == second, "The first call removed the bikes, so the second found none."
    assert len(station.bikes) == 3, "Nothing should leave the station when reporting."


def test_repair_list_returns_a_new_list():
    """Station - the returned list is not the station's own list"""
    station = stocked_station()
    broken = station.repair_list()

    assert broken is not station.bikes
    broken.clear()
    assert len(station.repair_list()) == 2, \
        "Clearing the result changed the station, so the same list was handed over."
    assert Station("Empty", 5).repair_list() == []


def stocked_member():
    ada = Member("Ada", 3)
    bike = Bike("A1", "Grand Army", False)
    ada.take(Ride(ada, bike, 45))
    ada.take(Ride(ada, bike, 10))
    ada.take(Ride(ada, bike, 30))
    return ada


def test_ride_owns_the_long_ride_rule():
    """Ride - is_long is True at 30 minutes or more"""
    ada = Member("Ada", 2)
    bike = Bike("A1", "Grand Army", False)

    assert Ride(ada, bike, 45).is_long() is True
    assert Ride(ada, bike, 30).is_long() is True
    assert Ride(ada, bike, 29).is_long() is False


def test_member_stores_rides_as_objects():
    """Member - take accepts a Ride and stores the object itself"""
    ada = Member("Ada", 2)
    ride = Ride(ada, Bike("A1", "Grand Army", False), 45)
    ada.take(ride)

    assert ada.rides[0] is ride, \
        "Store the Ride that was passed in, rather than building a dictionary from it."
    assert isinstance(ada.rides[0], Ride)


def test_long_rides_asks_each_ride():
    """Member - long_rides returns Ride objects chosen by their own rule"""
    ada = stocked_member()
    long = ada.long_rides()

    assert [ride.minutes for ride in long] == [45, 30]
    assert long[0].bike.serial == "A1", "The list holds Ride objects, so the bike is reachable."

    for ride in ada.rides:
        ride.minutes = 1
    assert ada.long_rides() == [], \
        "long_rides has to ask each ride, not keep its own copy of the rule."


def test_total_minutes_takes_ride_objects():
    """total_minutes - takes one list of Ride objects and totals their minutes"""
    ada = Member("Ada", 2)
    bike = Bike("A1", "Grand Army", False)

    assert total_minutes([Ride(ada, bike, 45), Ride(ada, bike, 10)]) == 55
    assert total_minutes([]) == 0


def test_total_minutes_skips_a_member_at_their_limit():
    """total_minutes - reaches the limit through each ride's member"""
    ada = Member("Ada", 2)
    zo = Member("Zo", 0)
    bike = Bike("A1", "Grand Army", False)

    assert total_minutes([Ride(ada, bike, 45), Ride(zo, bike, 10)]) == 45
    assert total_minutes([Ride(zo, bike, 10)]) == 0
