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


from from_scratch import Bike, BikeDepot, Course, Enrollment, Shift, Student, Volunteer, build_volunteers


TEST_SUITE_NAME = "From Scratch Tests"


def test_shift_stores_its_own_data():
    """Shift - __init__ stores the role, start hour and volunteer count on the instance"""
    morning = Shift("greeter", 9, 3)

    assert morning.role == "greeter"
    assert morning.start_hour == 9
    assert morning.volunteer_count == 3
    assert attributes_set_on(morning) >= {"role", "start_hour", "volunteer_count"}, \
        "Assign all three to self inside __init__, so each Shift carries its own."


def test_shift_reports_short_staffing():
    """Shift - is_short_staffed is True below 2 volunteers and False at 2 or more"""
    assert Shift("kitchen", 17, 1).is_short_staffed() is True
    assert Shift("kitchen", 17, 0).is_short_staffed() is True
    assert Shift("greeter", 9, 2).is_short_staffed() is False
    assert Shift("greeter", 9, 3).is_short_staffed() is False


def test_two_shifts_hold_separate_data():
    """Shift - two instances do not share attribute values"""
    morning = Shift("greeter", 9, 3)
    evening = Shift("kitchen", 17, 1)

    assert morning.role == "greeter"
    assert evening.role == "kitchen"


def stocked():
    depot = BikeDepot()
    depot.add(Bike("A1", "Grand Army", True))
    depot.add(Bike("A2", "Grand Army", False))
    depot.add(Bike("B7", "Borough Hall", True))
    return depot


def test_bikedepot_stores_the_bikes_it_is_given():
    """BikeDepot - add stores Bike objects, not copies of their data"""
    depot = BikeDepot()
    first = Bike("A1", "Grand Army", True)
    depot.add(first)

    found = depot.at_station("Grand Army")
    assert len(found) == 1
    assert isinstance(found[0], Bike), \
        "The depot holds Bike objects, so what comes back is a Bike."
    assert found[0] is first


def test_bikedepot_filters_without_handing_over_its_list():
    """BikeDepot - at_station returns a new list and leaves the depot's list alone"""
    depot = stocked()

    grand_army = depot.at_station("Grand Army")
    assert [bike.serial for bike in grand_army] == ["A1", "A2"]
    assert grand_army is not depot.bikes, \
        "Build a new list. Handing back the depot's own list lets a caller edit the depot."

    grand_army.clear()
    assert len(depot.at_station("Grand Army")) == 2, \
        "Clearing the returned list emptied the depot, so the same list was handed over."


def test_bikedepot_handles_no_matches_and_the_repair_list():
    """BikeDepot - repair_list finds the broken bikes, and no match returns []"""
    depot = stocked()

    assert depot.at_station("Nowhere") == []
    assert BikeDepot().repair_list() == []
    assert [bike.serial for bike in depot.repair_list()] == ["A1", "B7"]


def test_enrollment_holds_both_objects():
    """Enrollment - stores the Student and the Course themselves, not their values"""
    ada = Student("Ada")
    algebra = Course("Algebra")
    enrollment = Enrollment(ada, algebra, 92)

    assert enrollment.student is ada, \
        "Store the Student object, so a change to the student shows up here."
    assert enrollment.course is algebra
    assert enrollment.student.name == "Ada"


def test_enrollment_holds_the_grade_for_the_pair():
    """Enrollment - two enrollments for one student keep separate grades"""
    ada = Student("Ada")
    algebra = Enrollment(ada, Course("Algebra"), 92)
    geometry = Enrollment(ada, Course("Geometry"), 78)

    assert algebra.grade == 92
    assert geometry.grade == 78
    assert not hasattr(ada, "grade"), \
        "The grade belongs to the enrollment. A student taking two courses has two."


def test_enrollment_summary_reaches_through_both():
    """Enrollment - summary names the student and the course"""
    enrollment = Enrollment(Student("Zo"), Course("Physics"), 88)
    text = enrollment.summary()

    assert "Zo" in text
    assert "Physics" in text
    assert "88" in text


NAMES = ["Ada", "Zo", "Maya"]
HOURS = [40, 12, 20]
ROLES = ["kitchen", "greeter", "kitchen"]


def test_volunteer_stores_its_three_values():
    """Volunteer - __init__ stores name, hours and role, and is_experienced reads hours"""
    ada = Volunteer("Ada", 40, "kitchen")

    assert ada.name == "Ada"
    assert ada.hours == 40
    assert ada.role == "kitchen"
    assert ada.is_experienced() is True
    assert Volunteer("New", 19, "greeter").is_experienced() is False
    assert Volunteer("Edge", 20, "greeter").is_experienced() is True


def test_build_volunteers_keeps_the_three_values_together():
    """build_volunteers - returns one Volunteer per position, with matching values"""
    volunteers = build_volunteers(NAMES, HOURS, ROLES)

    assert len(volunteers) == 3
    assert all(isinstance(person, Volunteer) for person in volunteers), \
        "Return Volunteer objects, not tuples or dictionaries."
    assert volunteers[1].name == "Zo"
    assert volunteers[1].hours == 12
    assert volunteers[1].role == "greeter"


def test_build_volunteers_survives_sorting():
    """build_volunteers - sorting the result moves all three values together"""
    volunteers = build_volunteers(NAMES, HOURS, ROLES)
    volunteers.sort(key=lambda person: person.hours)

    assert [person.name for person in volunteers] == ["Zo", "Maya", "Ada"]
    assert volunteers[0].hours == 12
    assert volunteers[0].role == "greeter"
    assert build_volunteers([], [], []) == []
