# Classes and Instances

Practice building classes that hold their own data, answer for themselves, and keep two instances apart.

**Practicing:** classes, instances, `__init__`, `self`, instance attributes, `__repr__`, collections of objects

- [AI Use on This Assignment](#ai-use-on-this-assignment)
- [Setup](#setup)
- [Before You Start](#before-you-start)
- [From Scratch](#from-scratch)
  - [Question 1: `Shift`](#question-1-shift)
  - [Question 2: `BikeDepot`](#question-2-bikedepot)
  - [Question 3: `Student`, `Course` and `Enrollment`](#question-3-student-course-and-enrollment)
  - [Question 4: `Volunteer` and `build_volunteers`](#question-4-volunteer-and-build_volunteers)
- [Modify](#modify)
  - [Question 5: `PrintShop`](#question-5-printshop)
  - [Question 6: `Sensor`](#question-6-sensor)
  - [Question 7: `Warehouse`](#question-7-warehouse)
- [Debug](#debug)
  - [Question 8: `Locker`](#question-8-locker)
  - [Question 9: `Ledger`](#question-9-ledger)
- [Submitting](#submitting)
- [Good luck!](#good-luck)

## AI Use on This Assignment

Use whichever mode matches where you are with this material. Both are fine,
and most people move between them as a concept clicks.

**Tutor mode.** The AI explains, questions, quizzes, and critiques, and you
write every line you submit. For this assignment that means asking it what
`self` refers to inside a method, or having it quiz you on where an attribute
lives until you can say why two instances stopped sharing one. Ask it a
hundred questions — that is the whole point. What you do not do is ask it for
the class. Paste this at the start of a chat and it will hold for the rest of
the conversation:

> You are acting as a tutor. Your job is to explain what this coding question
> is asking, clarify confusing wording, and highlight the relevant concepts I
> need to know — but do not provide the full solution or code that directly
> answers the question. Instead, rephrase the problem in simpler terms,
> identify what is being tested, and suggest what steps or thought processes
> might help. Ask me guiding questions to make sure I am thinking critically.
> Do not write the final function, algorithm, or code implementation.

**Implementer mode.** You write a specification first, the AI writes code from
it, and then you verify that code line by line. For this assignment your spec
has to say, for every class, which attributes it stores and which questions it
answers about itself. If what comes back does more than you asked for, reject
it — over-delivery is a defect, and catching it is part of the job.

You own every line either way, and you will be asked to explain it.

## Setup

Clone your repository in `development/mod-2` and then `cd` into it. Set up
your virtual environment and make a draft branch before you start.

```sh
git clone [your_repo]
cd [your_repo]
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
git checkout -b draft
```

Run `pytest` to test the entire assignment, or `pytest -k Badge` for one
question. Every push runs the tests on GitHub and reports your score in the
**Actions** tab.

75% of tests passing counts as complete. Submit at that point even if it is
not perfect. Treat submitting as a checkpoint rather than a finish line, and
come back to improve it.

When you are done working on this assignment, turn off your virtual
environment by running:

```sh
deactivate
```

## Before You Start

This assignment has three sections:

1. From Scratch
2. Modify
3. Debug

Functions, loops, f-strings, lists and dictionaries are all assumed here, and
none of them are the new material. The new material is the **class**.

Every question turns on **where a value lives**. A value assigned to `self`
belongs to one instance, and a value assigned in the class body is shared by
every instance. **Most of the bugs here are that one distinction in different
clothes.**

## From Scratch

Write these functions and classes in `src/from_scratch.py`.

### Question 1: `Shift`

A community center schedules volunteers from a spreadsheet, and the
coordinator cannot tell at a glance which shifts are about to run short. Write
a class `Shift` that holds one shift and answers that question.

`__init__` takes a role, a start hour, and a volunteer count, and stores all
three on the instance. `is_short_staffed` returns `True` when the shift has
fewer than 2 volunteers.

```python
morning = Shift("greeter", 9, 3)
morning.role                  # "greeter" — read straight off the instance
morning.is_short_staffed()    # False — 3 volunteers is enough
evening = Shift("kitchen", 17, 1)
evening.is_short_staffed()    # True — 1 volunteer is fewer than 2
```

A shift with exactly 2 volunteers is staffed, so `is_short_staffed` returns
`False` for it.

Tests: `tests/test_from_scratch.py::test_shift_stores_its_own_data`

### Question 2: `BikeDepot`

A bike share has two hundred bikes and a mechanic who needs today's repair
list. Everyone who wants that list writes the loop again, slightly differently,
so the counts disagree. Write `BikeDepot` to own the collection and answer for
it.

**`Bike` is already written for you** in `src/from_scratch.py`. It holds a
serial number, a station name, and whether it needs repair.

`__init__` takes no arguments and starts an empty list on the instance.

| Method | Does | Returns |
| --- | --- | --- |
| `add(bike)` | Puts one `Bike` in the depot | Nothing |
| `at_station(station)` | Finds every bike at that station | A **new** list of the matching `Bike` objects |
| `repair_list()` | Finds every bike needing repair | A **new** list of the matching `Bike` objects |

```python
depot = BikeDepot()
depot.add(Bike("A1", "Grand Army", True))
depot.add(Bike("A2", "Grand Army", False))
depot.add(Bike("B7", "Borough Hall", True))

len(depot.at_station("Grand Army"))   # 2 — both bikes at that station
depot.at_station("Grand Army")[0].serial
# "A1" — the list holds Bike objects, so you can still read their attributes
[bike.serial for bike in depot.repair_list()]
# ["A1", "B7"] — in the order they were added
depot.at_station("Nowhere")           # [] — no match is an empty list, not an error
```

Both methods hand back a **new** list, so a caller who edits the result cannot
change the depot. A `for` loop is allowed to run over an empty list, so a new
depot needs no special case.

Tests: `tests/test_from_scratch.py::test_bikedepot_filters_without_handing_over_its_list`

### Question 3: `Student`, `Course` and `Enrollment`

A tutoring program stores each student's grade on the student record. A
student who takes two courses then has one grade for both, and the second
grade overwrites the first. The grade belongs to the pairing of a student and
a course, not to either one alone. Write all three classes.

| Class | `__init__` takes | Holds |
| --- | --- | --- |
| `Student` | a name | the name |
| `Course` | a title | the title |
| `Enrollment` | a `Student`, a `Course`, and a grade | both objects and the grade |

`Enrollment.summary()` returns `"<student name> — <course title>: <grade>"`.

```python
ada = Student("Ada")
algebra = Course("Algebra")
enrollment = Enrollment(ada, algebra, 92)

enrollment.student.name      # "Ada" — reach through the enrollment to the student
enrollment.summary()         # "Ada — Algebra: 92"

geometry = Enrollment(ada, Course("Geometry"), 78)
enrollment.grade             # 92 — still 92, because the grade is on the enrollment
```

Ada is one object held by two enrollments, so each enrollment keeps its own
grade and neither overwrites the other.

Tests: `tests/test_from_scratch.py::test_enrollment_holds_the_grade_for_the_pair`

### Question 4: `Volunteer` and `build_volunteers`

A program tracks volunteers in three lists lined up by position: name, hours,
role. Someone sorts one list and not the other two, so every volunteer's hours
now belong to someone else. Nothing errors, so the report is wrong for weeks.
Write the class that keeps the three values together.

`Volunteer.__init__` takes a name, hours, and a role, and stores all three.
`Volunteer.is_experienced()` returns `True` at 20 hours or more.

`build_volunteers(names, hours, roles)` returns a list of `Volunteer` objects,
one per position.

```python
names = ["Ada", "Zo", "Maya"]
hours = [40, 12, 20]
roles = ["kitchen", "greeter", "kitchen"]

volunteers = build_volunteers(names, hours, roles)
volunteers[1].name            # "Zo" — name, hours and role travel together now
volunteers[1].hours           # 12
volunteers[2].is_experienced()  # True — 20 hours is experienced
build_volunteers([], [], [])  # [] — three empty lists make no volunteers
```

> Hint: `zip(names, hours, roles)` hands you one tuple per position.

Tests: `tests/test_from_scratch.py::test_build_volunteers_keeps_the_three_values_together`

## Modify

Change the code already in `src/modify.py`.

### Question 5: `PrintShop`

`PrintShop` keeps each order as a dictionary, so a typo like
`order["custmer"]` raises `KeyError` only when that line runs, and the rush rule
is rewritten in every method that needs it. Do the following in
`src/modify.py`:

- Write `Order.__init__` to take a customer, a page count, and whether the order
  is rush.
- Move the rush rule onto `Order` as `is_priority()`. An order is priority when
  it is rush, **or** over 500 pages.
- Change `add_order` to take an `Order` and store it.
- Change `priority_orders` to ask each order rather than read its keys.

```python
shop = PrintShop()
shop.add_order(Order("Ada", 40, True))      # rush, so priority
shop.add_order(Order("Zo", 800, False))     # not rush, but over 500 pages
shop.add_order(Order("Maya", 20, False))    # neither

[order.customer for order in shop.priority_orders()]
# ["Ada", "Zo"] — Maya's small, non-rush order is left out
shop.priority_orders()[0].page_count
# 40 — the list holds Order objects, so you can still read their attributes
```

Tests: `tests/test_modify.py::test_printshop_stores_orders_as_objects`

### Question 6: `Sensor`

A technician debugging a sensor network prints the list of sensors and gets
this:

```text
[<Sensor object at 0x104e2f10>, <Sensor object at 0x104e2f50>]
```

The addresses change on every run, so the technician cannot tell which sensor
reported the bad reading, and ends up printing one attribute at a time to find
out. Add a `__repr__` to `Sensor` in `src/modify.py`.

`__repr__` **returns** a string naming the class and both values:
`Sensor('roof-2', 21.5)`.

```python
roof = Sensor("roof-2", 21.5)
repr(roof)      # "Sensor('roof-2', 21.5)" — says which sensor
print([roof])   # [Sensor('roof-2', 21.5)] — repr is what a list shows
```

Python calls `__repr__` for you whenever an object appears inside a
collection, so the list becomes readable without changing the print.

> Hint: `{self.sensor_id!r}` puts the quotes around a string for you.

Tests: `tests/test_modify.py::test_sensor_repr_names_the_sensor`

### Question 7: `Warehouse`

A company opens a second warehouse. Stock received at the Bronx site now also
shows at Queens, so the Queens manager ships an item that is three boxes away
and the order fails.

`crates` is assigned in the class body, which creates **one** list every
instance shares. Change `Warehouse` in `src/modify.py` so each warehouse owns
its own list.

```python
bronx = Warehouse("Bronx")
queens = Warehouse("Queens")
bronx.receive("widgets")

bronx.crate_count()     # 1 — the crate arrived at the Bronx
queens.crate_count()    # 0 — and only at the Bronx
bronx.crates is queens.crates
# False — each warehouse holds a different list object
```

A name assigned in the class body is created once, when the class is defined. A
name assigned to `self` in `__init__` is created again for every instance.

Tests: `tests/test_modify.py::test_two_warehouses_do_not_share_crates`

## Debug

Fix the code in `src/debug.py`.

### Question 8: `Locker`

`Locker` should hold one member per locker. Every locker in a gym's report shows
the same member instead, and it is always whoever signed up most recently.

```python
first = Locker(101, "Ada")
second = Locker(102, "Zo")

first.assigned_to
# want "Ada"
# "Zo" — creating the second locker changed the first one
first.number
# want 101
# 102
```

`__init__` assigns to `Locker`, the class itself, rather than to `self`, the
instance being created. One value written on the class is shared by every
instance, so each new locker overwrites the last.

Tests: `tests/test_debug.py::test_two_lockers_hold_separate_assignments`

### Question 9: `Ledger`

`overdue` should report every unpaid invoice past its due day. It reports one.
An accounts clerk chases that single invoice, marks it paid, runs the report
again, and finds another — so the list looks like it is one long and never
ends.

```python
ledger = Ledger()
ledger.add(Entry("Ada", 40, True))     # 40 days, unpaid
ledger.add(Entry("Zo", 5, False))      # paid
ledger.add(Entry("Maya", 61, True))    # 61 days, unpaid

[entry.client for entry in ledger.overdue()]
# want ["Ada", "Maya"]
# ["Ada"] — only the first match comes back
```

A `return` inside a loop ends the whole method, not that pass through the
loop. The method has to finish the loop before it hands anything back.

Tests: `tests/test_debug.py::test_ledger_reports_every_overdue_entry`

## Submitting

```sh
git add -A
git commit -m "your message"
git push
```

Pushing runs the tests on GitHub. Check the **Actions** tab for your score,
then open a pull request to your instructor for feedback.

## Good luck!

Every system you build from here is made of classes, so this is the
assignment the rest of the module stands on. You got this!
