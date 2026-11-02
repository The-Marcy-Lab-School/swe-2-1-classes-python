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


from debug import Entry, Ledger, Locker


TEST_SUITE_NAME = "Debug Tests"


def test_locker_stores_its_number_and_member():
    """Locker - a locker reports the number and member it was created with"""
    locker = Locker(101, "Ada")

    assert locker.number == 101
    assert locker.assigned_to == "Ada"
    assert locker.label() == "101: Ada"


def test_two_lockers_hold_separate_assignments():
    """Locker - creating a second locker leaves the first one unchanged"""
    first = Locker(101, "Ada")
    second = Locker(102, "Zo")

    assert first.assigned_to == "Ada", \
        "The second locker overwrote the first, so the values are on the class."
    assert first.number == 101
    assert second.assigned_to == "Zo"
    assert second.number == 102


def test_locker_values_live_on_the_instance():
    """Locker - the number and member are stored on each instance"""
    locker = Locker(101, "Ada")

    assert attributes_set_on(locker) >= {"number", "assigned_to"}, \
        "Assign to self inside __init__, so each locker carries its own values."


def stocked():
    ledger = Ledger()
    ledger.add(Entry("Ada", 40, True))
    ledger.add(Entry("Zo", 5, False))
    ledger.add(Entry("Maya", 61, True))
    return ledger


def test_ledger_reports_every_overdue_entry():
    """Ledger - overdue returns all the matches, not just the first"""
    ledger = stocked()

    assert [entry.client for entry in ledger.overdue()] == ["Ada", "Maya"]


def test_ledger_leaves_out_paid_and_recent_entries():
    """Ledger - overdue skips paid entries and anything 30 days or newer"""
    ledger = Ledger()
    ledger.add(Entry("Paid", 90, False))
    ledger.add(Entry("Edge", 30, True))

    assert ledger.overdue() == []
    assert Ledger().overdue() == []


def test_ledger_keeps_its_own_entries():
    """Ledger - overdue returns a new list and leaves the ledger alone"""
    ledger = stocked()
    found = ledger.overdue()

    assert len(ledger.entries) == 3
    assert found is not ledger.entries
