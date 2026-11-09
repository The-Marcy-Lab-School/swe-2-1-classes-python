# Classes and Instances

Practice building classes that hold their own data, answer for themselves, print and compare themselves, and hold other objects.

**Practicing:** classes, instances, `__init__`, `self`, methods, `__repr__`, `__eq__`, `@dataclass`, lists of objects, objects that hold other objects, `dir()`

- [AI Use on This Assignment](#ai-use-on-this-assignment)
- [Setup](#setup)
- [Before You Start](#before-you-start)
  - [Ideas to look for](#ideas-to-look-for)
  - [Look these up yourself](#look-these-up-yourself)
- [From Scratch](#from-scratch)
  - [Question 1: `Bike`](#question-1-bike)
  - [Question 2: A `Bike` That Prints and Compares](#question-2-a-bike-that-prints-and-compares)
  - [Question 3: `Station`](#question-3-station)
  - [Question 4: `Member` and `Ride`](#question-4-member-and-ride)
  - [Question 5: `has_attribute`](#question-5-has_attribute)
- [Modify](#modify)
  - [Question 6: `Dock`](#question-6-dock)
- [Debug](#debug)
  - [Question 7: `Mechanic`](#question-7-mechanic)
  - [Question 8: `RepairTicket`](#question-8-repairticket)
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

75% of tests passing counts as complete. `commit` and `push` at that point even if it is
not perfect. Treat submitting as a checkpoint rather than a finish line, and
come back to improve it.

When you are done working on this assignment, turn off your virtual
environment by running:

```sh
deactivate
```

## Before You Start

Skim this section before you read the lessons, so you know what to look for in them. Functions, loops, f-strings, lists and dictionaries are assumed. The new material is the **class**.

This assignment has three sections:

1. From Scratch
2. Modify
3. Debug

Every question follows the same order: a short story about Boro Bikes, a table that names everything you write, and examples to check your work against.

### Ideas to look for

Each question depends on one or more of these ideas. Part of the work is deciding which.

| Idea                                                                                                                                                                                                 | Lesson |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| A class is a blueprint for making objects. Calling it, as in `Bike("A1", "Grand Army", False)`, makes an object called an instance, and `__init__` stores the values you passed in on that instance. | 2.1    |
| When you call `bike.is_rentable()`, Python passes `bike` into the method as its first parameter, `self`.                                                                                             | 2.1    |
| Keep a rule and the data it is about within the same class: a bike answers whether _it_ can be rented.                                                                                               | 2.1    |
| A value assigned to `self`, as in `self.serial = serial`, belongs to one instance. A value assigned to the class itself is shared by every instance.                                                 | 2.2    |
| An object can hold other objects as attributes, and you reach the inner object's data with more dots: `ride.member.name`.                                                                            | 2.2    |
| A method that reports on an object's data should return a new list and leave the object's own list unchanged.                                                                                        | 2.2    |
| `__repr__`, the method Python calls to show an object as text, must return a string, not print one.                                                                                                  | 2.2    |
| `==` calls `__eq__`. Without one, `==` only asks whether two names refer to the same object, which is what `is` asks.                                                                                | 2.2    |
| `@dataclass`, written on the line above a class, writes `__init__`, `__repr__`, and `__eq__` for you from the attributes you list.                                                                   | 2.2    |
| A method is stored on the class, not on each instance. `dir()` lists every attribute and method an object can use, including the ones stored on its class.                                           | 2.2    |

### Look these up yourself

No lesson teaches this built-in function, and this assignment needs it:

- `hasattr()`. Read about it on [W3Schools](https://www.w3schools.com/python/ref_func_hasattr.asp).

## From Scratch

Write these classes and functions in `src/from_scratch.py`. The questions build one system, so do them in order: Questions 2 to 5 use your `Bike` from Question 1.

### Question 1: `Bike`

Boro Bikes is a public bike ride-share. It rents out bikes from stations around the city. Each bike has a serial number, is parked at one station, and either needs a repair or does not.

Write a class called `Bike` that has a serial, a station name, and whether it needs repair. It should also answer the question "can this bike be rented?"

| Write           | Takes                                                       | Does                                                                   |
| --------------- | ----------------------------------------------------------- | ---------------------------------------------------------------------- |
| `__init__`      | a serial, a station name, and whether the bike needs repair | Stores them on the instance as `serial`, `station`, and `needs_repair` |
| `is_rentable()` | nothing                                                     | Returns `True` when the bike does **not** need repair                  |

```python
good = Bike("A1", "Grand Army", False)
good.serial            # "A1"
good.is_rentable()     # True — nothing is wrong with it

broken = Bike("B7", "Borough Hall", True)
broken.is_rentable()   # False — it needs repair, so nobody can take it
```

### Question 2: A `Bike` That Prints and Compares

When you print a bike, Python shows something like `<from_scratch.Bike object at 0x104e2f10>`, which does not say which bike it is.

Separately, two `Bike` objects with the same serial describe the same bike, but `==` reports that they are different.

Add two methods to your `Bike` so that printing a bike shows its three values, and `==` answers the question "do these two bikes have the same serial?"

| Write           | Takes          | Does                                                                              |
| --------------- | -------------- | --------------------------------------------------------------------------------- |
| `__repr__()`    | nothing        | Returns the class name and all three values, as `Bike('A1', 'Grand Army', False)` |
| `__eq__(other)` | another `Bike` | Returns `True` when the two bikes have the same serial                            |

```python
bike = Bike("A1", "Grand Army", False)
print(bike)       # Bike('A1', 'Grand Army', False)
print([bike])     # [Bike('A1', 'Grand Army', False)]

first_bike = Bike("A1", "Grand Army", False)
second_bike = Bike("A1", "Borough Hall", True)
first_bike == second_bike   # True — the same serial means the same bike
second_bike is second_bike   # False — they are still two separate objects so this is expected
```

### Question 3: `Station`

Boro Bikes has forty stations and needs a way to represent them. A station has a number of docks, its capacity, and each dock holds one bike.

Write a class called `Station` that has a name, a capacity of docks, and a list of bikes currently docked. It should also answer the questions "which bikes are rentable from this station?" and "which bikes need a repair from this station?"

| Write           | Takes                         | Does                                                                               |
| --------------- | ----------------------------- | ---------------------------------------------------------------------------------- |
| `__init__`      | a station name and a capacity | Stores them as `name` and `capacity`, and starts an empty list of bikes as `bikes` |
| `dock(bike)`    | one `Bike`                    | Adds the bike to `bikes`                                                           |
| `rentable()`    | nothing                       | Returns a **new** list of the bikes that can be rented                             |
| `repair_list()` | nothing                       | Returns a **new** list of the bikes that cannot be rented                          |

Ask each bike whether it is rentable, with `bike.is_rentable()`, rather than checking its `needs_repair` yourself.

```python
station = Station("Grand Army", 20)
station.dock(Bike("A1", "Grand Army", True))
station.dock(Bike("A2", "Grand Army", False))

station.rentable()               # [Bike('A2', 'Grand Army', False)]
station.repair_list()            # [Bike('A1', 'Grand Army', True)]
Station("Empty", 8).rentable()   # [] — a new station has no bikes
```

### Question 4: `Member` and `Ride`

Users must sign up to be a member of Boro Bikes in order to take "rides". Each ride is one member on one bike for some number of minutes.

Write a class called `Member` that has a name and a separate class called `Ride` that has a member, a bike, and the number of minutes the ride lasted. A ride should answer the questions "was this a long ride?" and "who rode which bike, and for how long?"

| Class    | Write       | Takes                                         | Does                                                                                                                    |
| -------- | ----------- | --------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| `Member` | `__init__`  | a name                                        | Stores it as `name`                                                                                                     |
| `Ride`   | `__init__`  | a `Member`, a `Bike`, and a number of minutes | Stores them as `member`, `bike`, and `minutes`. `member` and `bike` hold the whole objects, not just a name or a serial |
| `Ride`   | `is_long()` | nothing                                       | Returns `True` when the ride lasted 30 minutes or more                                                                  |
| `Ride`   | `summary()` | nothing                                       | Returns `"<member's name> on <bike's serial>: <minutes> min"`                                                           |

```python
ada = Member("Ada")
ride = Ride(ada, Bike("A1", "Grand Army", False), 45)

ride.member.name   # "Ada" — reach through the ride to its member
ride.bike.serial   # "A1"
ride.is_long()     # True
ride.summary()     # "Ada on A1: 45 min"
```

### Question 5: `has_attribute`

Bikes have a serial, but stations and members do not. Asking a station for its serial raises an `AttributeError`.

Write a stand-alone function called `has_attribute` that answers the question "does this object have an attribute or a method with this name?" Python's built-in `hasattr()` already does this. Read about it first (see Look these up yourself above), then write your own version without calling it.

| Write                      | Takes                              | Does                                                                                                                             |
| -------------------------- | ---------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| `has_attribute(obj, name)` | any object, and a name as a string | Returns `True` when `obj` has an attribute or a method called `name`, and `False` when it does not. **Do not call `hasattr()`.** |

```python
bike = Bike("A1", "Grand Army", False)
station = Station("Grand Army", 20)

has_attribute(bike, "serial")         # True — __init__ stored it on the bike
has_attribute(bike, "is_rentable")    # True — a method counts too
has_attribute(station, "serial")      # False — a station has no serial
has_attribute("A1", "upper")          # True — it works on any object, not only yours
```

## Modify

Change the code in `src/modify.py`. Its class is separate from your From Scratch answers, so you can start here before From Scratch is finished.

### Question 6: `Dock`

`Dock` records where a bike is parked: a station and a dock number. Its three hand-written methods, `__init__`, `__repr__`, and `__eq__`, only store, print, and compare those two values.

Rewrite `Dock` with `@dataclass`, so that `@dataclass` writes all three methods and none of them is left in the class. The section [Writing Less with `@dataclass`](https://marcylabschool.gitbook.io/swe-python/mod-2-oop-python/2-instances-repr-eq-dataclass#writing-less-with-dataclass) in lesson 2.2 shows how.

These lines must give the same results before and after your change:

```python
dock = Dock("Grand Army", 4)
print(dock)                     # Dock(station='Grand Army', number=4)
dock == Dock("Grand Army", 4)   # True
dock == Dock("Grand Army", 5)   # False
```

## Debug

Fix the code in `src/debug.py`.

### Question 7: `Mechanic`

`Mechanic` should hold one mechanic's name and the shift they work. Every mechanic on the repair schedule shows the same name and shift instead, and it is always whoever was added most recently.

```python
rosa = Mechanic("Rosa", "morning")
dev = Mechanic("Dev", "evening")

rosa.name
# want "Rosa"
# "Dev" — creating the second mechanic changed the first one
rosa.label()
# want "Rosa (morning shift)"
# "Dev (evening shift)"
```

> Hint: check where `__init__` stores each value.

### Question 8: `RepairTicket`

A repair ticket should describe the bike it is for. Calling `describe()` raises an error instead:

```python
ticket = RepairTicket("A1", "flat tire")
ticket.describe()
# want "A1: flat tire"
# TypeError: RepairTicket.describe() takes 0 positional arguments but 1 was given
```

> Hint: read the message in two parts: what the method's definition lists, and what the call passed in.

## Submitting

```sh
git add -A
git commit -m "your message"
git push
```

Then open a pull request to your instructor for feedback.

## Good luck!

Every system you build from here is made of classes, so this is the
assignment the rest of the module stands on. You got this!
