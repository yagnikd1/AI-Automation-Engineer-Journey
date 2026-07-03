"""
Day 26 - Python Special (Magic/Dunder) Methods
AI Automation Engineer Journey - Phase 1

Topics covered:
1. __init__()  -> automatically runs when an object is created
2. __str__()   -> user-friendly string representation
3. __repr__()  -> developer/debugging representation
4. __len__()   -> supports len(object)
5. __add__()   -> supports object1 + object2
6. __eq__()    -> supports object1 == object2
"""


# =============================================================================
# Section 1: __init__() and __str__()
# =============================================================================

class BasicEmployee:
    """Employee class without __str__()."""

    def __init__(self, name):
        self.name = name


basic_employee = BasicEmployee("Rahul")
print("Without __str__():")
print(basic_employee)
# Output will look like:
# <__main__.BasicEmployee object at 0x...>


class PrintableEmployee:
    """Employee class with __str__()."""

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"Employee Name: {self.name}"


printable_employee = PrintableEmployee("Rahul")
print("\nWith __str__():")
print(printable_employee)
# Output:
# Employee Name: Rahul


# =============================================================================
# Section 2: __len__()
# =============================================================================

class Team:
    """Team class that supports len(team)."""

    def __init__(self, members):
        self.members = members

    def __len__(self):
        return len(self.members)


team = Team(["Rahul", "Amit", "Neha"])

print("\nUsing __len__():")
print(len(team))
# Output:
# 3


# =============================================================================
# Section 3: __add__()
# =============================================================================

class SalaryEmployee:
    """Employee class that supports adding salaries."""

    def __init__(self, salary):
        self.salary = salary

    def __add__(self, other):
        return self.salary + other.salary


employee1 = SalaryEmployee(30000)
employee2 = SalaryEmployee(40000)

print("\nUsing __add__():")
print(employee1 + employee2)
# Output:
# 70000


# =============================================================================
# Section 4: __eq__()
# =============================================================================

class IDBasedEmployee:
    """Employee class that compares objects by employee_id."""

    def __init__(self, employee_id):
        self.employee_id = employee_id

    def __eq__(self, other):
        return self.employee_id == other.employee_id


emp1 = IDBasedEmployee(101)
emp2 = IDBasedEmployee(101)
emp3 = IDBasedEmployee(102)

print("\nUsing __eq__():")
print(emp1 == emp2)
print(emp1 == emp3)
# Output:
# True
# False


# =============================================================================
# Section 5: Practice Exercise - __str__()
# =============================================================================

class SimpleBook:
    """Book class with user-friendly printing."""

    def __init__(self, title, pages):
        self.title = title
        self.pages = pages

    def __str__(self):
        return f"Book: {self.title} ({self.pages} pages)"


simple_book = SimpleBook("Python Programming", 350)

print("\nPractice Exercise - __str__():")
print(simple_book)
# Output:
# Book: Python Programming (350 pages)


# =============================================================================
# Section 6: __repr__() - Developer Version of __str__()
# =============================================================================

class DebugBook:
    """Book class with both __str__() and __repr__()."""

    def __init__(self, title, pages):
        self.title = title
        self.pages = pages

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"DebugBook(title='{self.title}', pages={self.pages})"


debug_book = DebugBook("Python", 350)

print("\nUsing __str__() and __repr__():")
print(debug_book)
print([debug_book])
# Output:
# Python
# [DebugBook(title='Python', pages=350)]


# =============================================================================
# Section 7: Mini Project - Library Management System
# =============================================================================

class Book:
    """Represents a book in a small library management system."""

    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages

    def __str__(self):
        """Returns a user-friendly description of the book."""
        return f"Book: {self.title}\nAuthor: {self.author}\nPages: {self.pages}"

    def __repr__(self):
        """Returns a developer-friendly representation of the book."""
        return f"Book(title='{self.title}', author='{self.author}', pages={self.pages})"


book1 = Book("Atomic Habits", "James Clear", 320)
book2 = Book("The Power of Habit", "Charles Duhigg", 400)

library = [book1, book2]

print("\nMini Project - print(book1):")
print(book1)
# Output:
# Book: Atomic Habits
# Author: James Clear
# Pages: 320

print("\nMini Project - print(library):")
print(library)
# Output:
# [Book(title='Atomic Habits', author='James Clear', pages=320),
#  Book(title='The Power of Habit', author='Charles Duhigg', pages=400)]


# =============================================================================
# Day 26 Summary
# =============================================================================

"""
Key learning:
- Dunder methods are special methods with double underscores before and after.
- __init__() runs automatically when an object is created.
- __str__() controls what users see when printing an object.
- __repr__() controls what developers see during debugging or inside containers.
- __len__() allows len(object).
- __add__() allows object1 + object2.
- __eq__() allows object1 == object2.

Roadmap importance:
These methods help us understand how Python objects behave internally.
They are useful when debugging, reading professional libraries, and building clean OOP-based automation projects.
"""
