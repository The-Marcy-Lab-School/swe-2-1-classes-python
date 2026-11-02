# Classes and Instances

Practice building classes that hold their own data, answer for themselves, and keep two instances apart.

**Practicing:** classes, instances, `__init__`, `self`, instance attributes, `__repr__`, collections of objects

- [AI Use on This Assignment](#ai-use-on-this-assignment)
- [Setup](#setup)
- [Before You Start](#before-you-start)
- [From Scratch](#from-scratch)
  - [Question 1: `Bike`](#question-1-bike)
  - [Question 2: `Station`](#question-2-station)
  - [Question 3: `Ride`](#question-3-ride)
  - [Question 4: `build_bikes`](#question-4-build_bikes)
- [Modify](#modify)
  - [Question 5: `Station.repair_list`](#question-5-stationrepair_list)
  - [Question 6: `Member` and `Ride`](#question-6-member-and-ride)
  - [Question 7: `total_minutes`](#question-7-total_minutes)
- [Debug](#debug)
  - [Question 8: `Member`](#question-8-member)
  - [Question 9: `Ride`](#question-9-ride)
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

Run `pytest` to test the entire assignment. To run one question, pass part of
its name: `pytest -k Bike`. Every push runs the tests on GitHub and reports
your score in the **Actions** tab.

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

A value assigned to `self` belongs to one instance. A value assigned in the
class body is shared by every instance that will ever exist. **Most of the
bugs in this assignment are a value stored in the wrong one of those two
places**, so when something reports the wrong data, start by asking which of
the two it was assigned to.

## From Scratch

Write these functions and classes in `src/from_scratch.py`.

### Question 1: `Bike`

Boro Bikes tracks its fleet in a spreadsheet, and a mechanic who wants today's
repair list reads it by eye. Start the system that replaces it. Write a class
`Bike` that holds one bike.

`__init__` takes a serial, a station name, and whether the bike needs repair,
and stores all three on the instance. `is_rentable` returns `True` when the
bike does **not** need repair.

```python
good = Bike("A1", "Grand Army", False)
good.serial            # "A1" — read straight off the instance
good.is_rentable()     # True — nothing wrong with it
broken = Bike("B7", "Borough Hall", True)
broken.is_rentable()   # False — it needs repair, so nobody can take it
```

### Question 2: `Station`

Boro Bikes has forty docks and a mechanic who needs one station's repair list.
Everyone who wants that list writes the loop again, slightly differently, so
the counts disagree. Write a class `Station` that owns its bikes and answers
for them.

**`Bike` is already written for you** in `src/from_scratch.py`.

`__init__` takes a station name and a capacity, and starts an empty list of
bikes on the instance.

| Method | Does | Returns |
| --- | --- | --- |
| `dock(bike)` | Puts one `Bike` at this station | Nothing |
| `rentable()` | Finds every bike that can be rented | A **new** list of the matching `Bike` objects |
| `repair_list()` | Finds every bike needing repair | A **new** list of the matching `Bike` objects |

```python
station = Station("Grand Army", 20)
station.dock(Bike("A1", "Grand Army", True))
station.dock(Bike("A2", "Grand Army", False))

[bike.serial for bike in station.repair_list()]   # ["A1"] — only the broken one
station.rentable()[0].serial
# "A2" — the list holds Bike objects, so you can still read their attributes
Station("Empty", 8).rentable()                    # [] — a new station has no bikes
```

Both methods hand back a **new** list, so a caller who edits the result cannot
change the station. A `for` loop is allowed to run over an empty list, so a
new station needs no special case.

### Question 3: `Ride`

Boro Bikes stores each ride's length on the member record. A member who takes
two rides then has one length for both, and the second overwrites the first.
The minutes belong to the pairing of a member and a bike, not to either one
alone. Write `Member` and `Ride`.

**`Bike` is already written for you** in `src/from_scratch.py`.

| Class | `__init__` takes | Holds |
| --- | --- | --- |
| `Member` | a name and a ride limit | the name, the limit, and an empty list of rides |
| `Ride` | a `Member`, a `Bike`, and minutes | both objects and the minutes |

`Member.take(ride)` adds one ride to that member's list. `Ride.is_long()`
returns `True` at 30 minutes or more, and `Ride.summary()` returns
`"<member name> on <bike serial>: <minutes> min"`.

```python
ada = Member("Ada", 2)
ride = Ride(ada, Bike("A1", "Grand Army", False), 45)

ride.member.name    # "Ada" — reach through the ride to the member
ride.bike.serial    # "A1"
ride.is_long()      # True — 45 minutes is a long ride
ride.summary()      # "Ada on A1: 45 min"

short = Ride(ada, Bike("A2", "Grand Army", False), 10)
ride.minutes        # 45 — still 45, because the minutes are on the ride
```

Ada is one object held by two rides, so each ride keeps its own minutes and
neither overwrites the other.

### Question 4: `build_bikes`

The fleet arrives from the vendor as three lists lined up by position:
serials, stations, repair flags. Someone sorted the serials to find a bike and
did not sort the other two, so every bike's station was wrong by one row and a
van spent a morning at the wrong docks. Nothing errored, because all three
lists were still the right length.

**`Bike` is already written for you** in `src/from_scratch.py`.

Write `build_bikes(serials, stations, flags)`, which returns a list of `Bike`
objects, one per position.

```python
serials = ["A1", "A2", "B7"]
stations = ["Grand Army", "Grand Army", "Borough Hall"]
flags = [True, False, False]

fleet = build_bikes(serials, stations, flags)
fleet[2].serial              # "B7" — serial, station and flag travel together now
fleet[2].station             # "Borough Hall"
fleet[0].is_rentable()       # False — A1 needs repair
build_bikes([], [], [])      # [] — three empty lists make no bikes
```

Sorting the list now moves all three values at once, so they cannot come
apart.

> Hint: `zip(serials, stations, flags)` hands you one tuple per position.

## Modify

Change the code already in `src/modify.py`.

### Question 5: `Station.repair_list`

`repair_list` is meant to tell a mechanic which bikes to collect. It removes
each broken bike from the station while reporting it, so the second call
returns nothing and the station's own records no longer hold those bikes. A
mechanic who refreshes the page sees an empty list and goes home.

Change `repair_list` in `src/modify.py` so that it **returns a new list** of
the broken `Bike` objects and leaves `self.bikes` exactly as it found it.

```python
station = Station("Grand Army", 20)
station.dock(Bike("A1", "Grand Army", True))
station.dock(Bike("A2", "Grand Army", False))

[bike.serial for bike in station.repair_list()]   # ["A1"]
[bike.serial for bike in station.repair_list()]   # ["A1"] — same answer twice
len(station.bikes)                                # 2 — nothing left the station
```

A method that reports should answer a question without changing what it was
asked about, so calling it twice gives the same answer.

### Question 6: `Member` and `Ride`

`Member` keeps each ride as a dictionary, so a typo like `ride["minuts"]`
raises `KeyError` only when that line runs, and the long-ride rule is
rewritten in every method that needs it.

**`Bike` is already written for you.** Do the following in `src/modify.py`:

- Write `Ride.__init__` to take a member, a bike, and the minutes.
- Move the long-ride rule onto `Ride` as `is_long()`. A ride is long at 30
  minutes or more.
- Change `take` to accept a `Ride` and store it.
- Change `long_rides` to ask each ride rather than read its keys.

```python
ada = Member("Ada", 2)
bike = Bike("A1", "Grand Army", False)
ada.take(Ride(ada, bike, 45))
ada.take(Ride(ada, bike, 10))

[ride.minutes for ride in ada.long_rides()]
# [45] — the 10-minute ride is left out
ada.long_rides()[0].bike.serial
# "A1" — the list holds Ride objects, so you can reach the bike through one
```

With the rule on `Ride`, changing 30 to 45 later is one edit in one class.

### Question 7: `total_minutes`

`total_minutes` bills members for their riding time. It takes two lists lined
up by position, names and minutes. A caller who passes them in the wrong order
gets a total and no error, because both lists are still the right length, and
a member is billed for somebody else's ride.

**`Bike`, `Member` and `Ride` are already written for you.**

Change `total_minutes(rides)` to take **one list of `Ride` objects** and
return the total minutes, counting only rides by a member who is still within
their limit.

```python
ada = Member("Ada", 2)
zo = Member("Zo", 0)
bike = Bike("A1", "Grand Army", False)

total_minutes([Ride(ada, bike, 45), Ride(zo, bike, 10)])
# 45 — Zo's limit is 0, so that ride is not billed
total_minutes([])
# 0 — no rides means nothing to bill
```

Each ride already knows its member, so the function reaches the limit through
the ride rather than being handed a second list that has to stay in step.

## Debug

Fix the code in `src/debug.py`.

### Question 8: `Member`

`Member` should hold one rider's name and limit. Every member in the roster
shows the same name instead, and it is always whoever signed up most recently.

```python
ada = Member("Ada", 2)
zo = Member("Zo", 5)

ada.name
# want "Ada"
# "Zo" — creating the second member changed the first one
ada.limit
# want 2
# 5
```

`__init__` assigns to `Member`, the class itself, rather than to `self`, the
instance being created. One value written on the class is shared by every
instance, so each new member overwrites the last.

### Question 9: `Ride`

Printing one ride looks right. Printing a list of them raises, and the ride
details appear on screen before the traceback does, in a different order than
the list.

```python
ride = Ride(Member("Ada", 2), Bike("A1", "Grand Army", False), 45)
print(ride)
# Ride('Ada', 'A1', 45)  — looks correct
print([ride])
# Ride('Ada', 'A1', 45)
# TypeError: __repr__ returned non-string (type NoneType)
```

A function that prints and never returns hands back `None`. Python needs
`__repr__` to **give** it a string so that the caller can place it inside the
list's own output.

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
