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


from modify import Order, PrintShop, Sensor, Warehouse


TEST_SUITE_NAME = "Modify Tests"


def stocked():
    shop = PrintShop()
    shop.add_order(Order("Ada", 40, True))
    shop.add_order(Order("Zo", 800, False))
    shop.add_order(Order("Maya", 20, False))
    return shop


def test_order_owns_the_priority_rule():
    """Order - is_priority is True when rush, or over 500 pages"""
    assert Order("Ada", 40, True).is_priority() is True
    assert Order("Zo", 800, False).is_priority() is True
    assert Order("Maya", 20, False).is_priority() is False
    assert Order("Edge", 500, False).is_priority() is False, \
        "Exactly 500 pages is not over 500."


def test_printshop_stores_orders_as_objects():
    """PrintShop - add_order takes an Order and stores the object itself"""
    shop = PrintShop()
    first = Order("Ada", 40, True)
    shop.add_order(first)

    assert shop.orders[0] is first, \
        "Store the Order that was passed in, rather than building a dictionary from it."
    assert isinstance(shop.orders[0], Order)


def test_printshop_asks_each_order():
    """PrintShop - priority_orders returns Order objects chosen by their own rule"""
    shop = stocked()
    priority = shop.priority_orders()

    assert [order.customer for order in priority] == ["Ada", "Zo"]
    assert all(isinstance(order, Order) for order in priority)

    for order in shop.orders:
        order.rush = False
        order.page_count = 1
    assert shop.priority_orders() == [], \
        "priority_orders has to ask each order, not keep its own copy of the rule."


def test_sensor_repr_names_the_sensor():
    """Sensor - __repr__ returns a string naming the class and both values"""
    roof = Sensor("roof-2", 21.5)
    text = repr(roof)

    assert isinstance(text, str), "__repr__ has to return the string, not print it."
    assert "object at" not in text, \
        "Python's default repr is still being used, so __repr__ is not being found."
    assert "Sensor" in text
    assert "roof-2" in text
    assert "21.5" in text


def test_sensor_repr_shows_up_inside_a_list():
    """Sensor - a list of sensors prints readably, and is_freezing still works"""
    sensors = [Sensor("roof-2", 21.5), Sensor("cellar", -3)]
    text = repr(sensors)

    assert "roof-2" in text
    assert "cellar" in text
    assert sensors[1].is_freezing() is True
    assert sensors[0].is_freezing() is False


def test_warehouse_still_stores_its_site_and_receives():
    """Warehouse - a warehouse keeps its site name and counts what it receives"""
    bronx = Warehouse("Bronx")
    bronx.receive("widgets")
    bronx.receive("bolts")

    assert bronx.site == "Bronx"
    assert bronx.crate_count() == 2


def test_two_warehouses_do_not_share_crates():
    """Warehouse - a crate received at one site does not appear at the other"""
    bronx = Warehouse("Bronx")
    queens = Warehouse("Queens")
    bronx.receive("widgets")

    assert bronx.crate_count() == 1
    assert queens.crate_count() == 0, \
        "The crate reached Queens, so both warehouses are reading one shared list."
    assert bronx.crates is not queens.crates


def test_crates_is_created_per_instance():
    """Warehouse - crates is assigned in __init__ rather than in the class body"""
    assert "crates" not in assigns_in_class_body(Warehouse), \
        "Move crates out of the class body. A list there is made once and shared."
    assert "crates" in attributes_set_on(Warehouse("Bronx"))
