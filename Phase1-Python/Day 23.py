"""
Day 23 - OOP Inheritance
AI Automation Engineer Journey

Topic:
OOP - Inheritance

Difficulty:
Intermediate

Programs:
1. Single Inheritance
2. Hierarchical Inheritance
3. Method Overriding
4. super() Function
5. Banking System Mini Project

Key Concepts:
- Parent class
- Child class
- Code reuse
- Method overriding
- super()
- Single inheritance
- Hierarchical inheritance
"""


# ============================================================
# Helper Function
# ============================================================

def show_section(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


# ============================================================
# Program 1: Single Inheritance
# ============================================================

show_section("Program 1: Single Inheritance")


class Person:

    def introduce(self):
        print("Hello, I am a person.")

    def walk(self):
        print("I can walk.")


class Student(Person):

    def study(self):
        print("I am studying Python.")


student = Student()

student.introduce()
student.walk()
student.study()


# ============================================================
# Program 2: Hierarchical Inheritance
# ============================================================

show_section("Program 2: Hierarchical Inheritance")


class Employee:

    def login(self):
        print("Employee logged in.")

    def logout(self):
        print("Employee logged out.")


class Developer(Employee):

    def code(self):
        print("Writing code.")


class Tester(Employee):

    def test(self):
        print("Testing software.")


class Manager(Employee):

    def meeting(self):
        print("Attending meeting.")


developer = Developer()
tester = Tester()
manager = Manager()

developer.login()
developer.code()
developer.logout()

tester.login()
tester.test()
tester.logout()

manager.login()
manager.meeting()
manager.logout()


# ============================================================
# Program 3: Method Overriding
# ============================================================

show_section("Program 3: Method Overriding")


class Subscription:

    def show_plan(self):
        print("General subscription plan.")


class BasicPlan(Subscription):

    def show_plan(self):
        print("Basic Plan: 720p video, ads included.")


class PremiumPlan(Subscription):

    def show_plan(self):
        print("Premium Plan: 4K video, no ads.")


class FamilyPlan(Subscription):

    def show_plan(self):
        print("Family Plan: 4 screens, parental control.")


basic_plan = BasicPlan()
premium_plan = PremiumPlan()
family_plan = FamilyPlan()

basic_plan.show_plan()
premium_plan.show_plan()
family_plan.show_plan()


# ============================================================
# Program 4: super() Function
# ============================================================

show_section("Program 4: super() Function")


class Order:

    def confirm_order(self):
        print("Order confirmed successfully.")


class OnlineOrder(Order):

    def confirm_order(self):
        super().confirm_order()
        print("Sending confirmation email.")


online_order = OnlineOrder()

online_order.confirm_order()


# ============================================================
# Program 5: Banking System Mini Project
# ============================================================

show_section("Program 5: Banking System Mini Project")


class BankAccount:

    def open_account(self):
        print("Bank account opened.")

    def show_balance(self):
        print("Current balance: 0")


class SavingsAccount(BankAccount):

    def show_balance(self):
        super().show_balance()
        print("Savings account earns 4% interest.")


class CurrentAccount(BankAccount):

    def show_balance(self):
        super().show_balance()
        print("Current account has overdraft facility.")


savings = SavingsAccount()
current = CurrentAccount()

savings.open_account()
savings.show_balance()

current.open_account()
current.show_balance()


# ============================================================
# Key Learnings - Day 23
# ============================================================

"""
1. Inheritance allows a child class to reuse methods from a parent class.
2. Common behavior should be placed inside the parent class.
3. Child classes should contain only their specific behavior.
4. Method overriding happens when a child class defines a method with the same name as the parent method.
5. super() is used to call the parent class method from inside the child class.
6. Hierarchical inheritance means one parent class has multiple child classes.
7. Clean OOP design avoids unnecessary code repetition.
"""
