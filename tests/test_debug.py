def attributes_set_on(instance):
    """The attribute names stored on this instance rather than on its class.

    A value assigned to a plain variable in __init__ is gone once __init__
    returns, so it does not appear here. One assigned to self does.
    """
    return set(vars(instance))


from debug import Mechanic, RepairTicket


TEST_SUITE_NAME = "Debug Tests"


# ---------- Question 8: Mechanic ----------

def test_mechanic_stores_its_own_name_and_shift():
    """Mechanic - each mechanic reports the name and shift it was created with"""
    rosa = Mechanic("Rosa", "morning")
    dev = Mechanic("Dev", "evening")

    assert attributes_set_on(rosa) >= {"name", "shift"}, "__init__ should store both values on self."
    assert rosa.name == "Rosa"
    assert rosa.shift == "morning"
    assert dev.name == "Dev"


def test_mechanic_label():
    """Mechanic - label() shows that mechanic's own name and shift"""
    rosa = Mechanic("Rosa", "morning")
    Mechanic("Dev", "evening")

    assert rosa.label() == "Rosa (morning shift)"


# ---------- Question 9: RepairTicket ----------

def test_repair_ticket_describes_itself():
    """RepairTicket - describe() returns the serial and the problem"""
    ticket = RepairTicket("A1", "flat tire")

    assert ticket.describe() == "A1: flat tire"


def test_two_repair_tickets_describe_different_bikes():
    """RepairTicket - each ticket describes its own bike"""
    first = RepairTicket("A1", "flat tire")
    second = RepairTicket("B7", "loose chain")

    assert first.describe() == "A1: flat tire"
    assert second.describe() == "B7: loose chain"
