import ast
import dataclasses
import inspect
import textwrap


def methods_defined_in(cls):
    """The names of the methods written directly in a class body, read with the ast module."""
    source = textwrap.dedent(inspect.getsource(cls))
    body = ast.parse(source).body[0].body
    return {node.name for node in body if isinstance(node, ast.FunctionDef)}


from modify import Dock


TEST_SUITE_NAME = "Modify Tests"


# ---------- Question 7: Dock ----------

def test_dock_is_a_dataclass():
    """Dock - is written with @dataclass"""
    assert dataclasses.is_dataclass(Dock), "Put @dataclass on the line above class Dock."
    assert [field.name for field in dataclasses.fields(Dock)] == ["station", "number"]


def test_dock_has_no_hand_written_methods():
    """Dock - no longer writes __init__, __repr__ or __eq__ by hand"""
    leftover = methods_defined_in(Dock) & {"__init__", "__repr__", "__eq__"}
    assert not leftover, f"@dataclass writes these for you, so delete them: {sorted(leftover)}"


def test_dock_prints_and_compares_as_before():
    """Dock - prints and compares exactly as the hand-written version did"""
    dock = Dock("Grand Army", 4)

    assert dock.station == "Grand Army"
    assert dock.number == 4
    assert repr(dock) == "Dock(station='Grand Army', number=4)"
    assert dock == Dock("Grand Army", 4)
    assert dock != Dock("Grand Army", 5)
