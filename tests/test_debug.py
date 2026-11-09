def attributes_set_on(instance):
    """The attribute names stored on this instance rather than on its class.

    An attribute assigned to the class itself is shared by every instance, so it
    does not appear here. One assigned to self in __init__ does.
    """
    return set(vars(instance))


from debug import Mechanic, RepairTicket


TEST_SUITE_NAME = "Debug Tests"


# ---------- Question 7: Mechanic ----------

def test_mechanic_stores_its_own_name_and_shift():
    """Mechanic - each mechanic reports the name and shift it was created with"""
    rosa = Mechanic("Rosa", "morning")
    dev = Mechanic("Dev", "evening")

    assert rosa.name == "Rosa", "Creating a second mechanic should not change the first."
    assert rosa.shift == "morning"
    assert dev.name == "Dev"
    assert attributes_set_on(rosa) >= {"name", "shift"}


def test_mechanic_label():
    """Mechanic - label() shows that mechanic's own name and shift"""
    rosa = Mechanic("Rosa", "morning")
    Mechanic("Dev", "evening")

    assert rosa.label() == "Rosa (morning shift)"


# ---------- Question 8: RepairTicket ----------

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
