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


from debug import Bike, Member, Ride


TEST_SUITE_NAME = "Debug Tests"


def test_member_stores_its_name_and_limit():
    """Member - a member reports the name and limit it was created with"""
    ada = Member("Ada", 2)

    assert ada.name == "Ada"
    assert ada.limit == 2
    assert ada.label() == "Ada (2 rides)"


def test_two_members_hold_separate_values():
    """Member - creating a second member leaves the first one unchanged"""
    ada = Member("Ada", 2)
    zo = Member("Zo", 5)

    assert ada.name == "Ada", \
        "The second member overwrote the first, so the values are on the class."
    assert ada.limit == 2
    assert zo.name == "Zo"
    assert zo.limit == 5


def test_member_values_live_on_the_instance():
    """Member - the name and limit are stored on each instance"""
    ada = Member("Ada", 2)

    assert attributes_set_on(ada) >= {"name", "limit"}, \
        "Assign to self inside __init__, so each member carries its own values."


def test_ride_repr_returns_a_string():
    """Ride - __repr__ returns the string rather than printing it"""
    ride = Ride(Member("Ada", 2), Bike("A1", "Grand Army", False), 45)
    text = repr(ride)

    assert isinstance(text, str), "__repr__ has to return the string, not print it."
    assert "Ada" in text
    assert "A1" in text
    assert "45" in text


def test_ride_list_prints_without_raising():
    """Ride - a list of rides can be turned into a string"""
    ada = Member("Ada", 2)
    bike = Bike("A1", "Grand Army", False)
    text = repr([Ride(ada, bike, 45), Ride(ada, bike, 10)])

    assert "45" in text
    assert "10" in text
