"""
====================================================================
AI Automation Engineer Journey
Day 25 - Object-Oriented Programming: Abstraction
====================================================================

Topic:
    OOP Abstraction in Python

Purpose:
    GitHub-ready lesson file and future revision/reference file.

Main Concepts:
    - Abstraction
    - ABC
    - @abstractmethod
    - Abstract classes
    - Child class implementation
    - Abstraction vs Encapsulation
    - All four OOP pillars together
    - Professional AutomationBot Framework
"""


# ====================================================================
# SECTION 1: ABSTRACTION OVERVIEW
# ====================================================================

"""
Abstraction means showing only essential features while hiding
unnecessary implementation details.

Simple meaning:
    - Show what an object can do.
    - Hide how it works internally.

Example:
    bot.login()

The user knows the bot logs in.
The user does not need to know the internal browser/session/cookie logic.
"""


# ====================================================================
# SECTION 2: WHY ABSTRACTION IS NEEDED
# ====================================================================

"""
Abstraction is useful when multiple classes must follow the same rules.

Example:
    GmailBot, LinkedInBot, WhatsAppBot, OutlookBot

Every bot should have:
    login()
    run()
    logout()

Without abstraction:
    One class may use login()
    Another may use sign_in()
    Another may use authenticate()

With abstraction:
    The parent class defines a common contract.
    Every child class must implement the required methods.
"""


# ====================================================================
# SECTION 3: BASIC ABSTRACT CLASS EXAMPLE
# ====================================================================

from abc import ABC, abstractmethod


class BasicAutomationBot(ABC):
    """
    Basic abstract parent class.
    """

    @abstractmethod
    def login(self):
        pass

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def logout(self):
        pass


class BasicGmailBot(BasicAutomationBot):
    """
    Concrete child class.

    This class can create objects because it implements all abstract methods.
    """

    def login(self):
        print("Logging in to Gmail")

    def run(self):
        print("Running Gmail automation tasks")

    def logout(self):
        print("Logging out of Gmail")


basic_bot = BasicGmailBot()
basic_bot.login()
basic_bot.run()
basic_bot.logout()


# ====================================================================
# SECTION 4: SINGLE ABSTRACT METHOD EXAMPLE
# ====================================================================

class SingleActionBot(ABC):
    """
    Abstract class with one required method.
    """

    @abstractmethod
    def login(self):
        pass


class SimpleGmailBot(SingleActionBot):
    def login(self):
        print("Logging into Gmail")


simple_bot = SimpleGmailBot()
simple_bot.login()


# ====================================================================
# SECTION 5: IMPORTANT RULES
# ====================================================================

"""
Rule 1:
    ABC stands for Abstract Base Class.

Rule 2:
    @abstractmethod forces child classes to implement a method.

Rule 3:
    A child class must implement all abstract methods.

Rule 4:
    If even one abstract method is missing, Python raises TypeError.

Rule 5:
    Abstract classes can contain:
        - normal methods
        - constructors
        - attributes
        - shared reusable logic
"""


# ====================================================================
# SECTION 6: ABSTRACTION VS ENCAPSULATION
# ====================================================================

"""
Abstraction:
    - Hides implementation details.
    - Focuses on what an object does.
    - Example: login(), run(), logout()

Encapsulation:
    - Protects data inside a class.
    - Focuses on how data is controlled.
    - Example: self.__password

Interview-ready answer:
    Abstraction hides implementation details and shows essential behavior.
    Encapsulation hides/protects data inside a class.
"""


# ====================================================================
# SECTION 7: PROFESSIONAL MINI PROJECT
# MULTI-BOT AUTOMATION FRAMEWORK
# ====================================================================

class AutomationBot(ABC):
    """
    Professional abstract parent class for automation bots.

    OOP pillars used here:

    Encapsulation:
        self.__password protects password data.

    Inheritance:
        Child bots inherit username, constructor, and log() method.

    Abstraction:
        login(), run(), logout() are required methods.

    Polymorphism:
        Different child bots implement the same methods differently.
    """

    def __init__(self, username, password):
        self.username = username
        self.__password = password

    def log(self, message):
        """
        Shared reusable logging method.
        """
        print(f"[LOG] {message}")

    def get_password(self):
        """
        Controlled access method for password.

        Child classes should not directly access self.__password.
        """
        return self.__password

    @abstractmethod
    def login(self):
        pass

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def logout(self):
        pass


class GmailBot(AutomationBot):
    def login(self):
        self.log(f"Logging in to Gmail with username: {self.username}")

    def run(self):
        self.log("Running Gmail automation tasks")

    def logout(self):
        self.log("Logging out of Gmail")


class LinkedInBot(AutomationBot):
    def login(self):
        self.log(f"Logging in to LinkedIn with username: {self.username}")

    def run(self):
        self.log("Running LinkedIn automation tasks")

    def logout(self):
        self.log("Logging out of LinkedIn")


class WhatsAppBot(AutomationBot):
    def login(self):
        self.log(f"Logging in to WhatsApp with username: {self.username}")

    def run(self):
        self.log("Running WhatsApp automation tasks")

    def logout(self):
        self.log("Logging out of WhatsApp")


class OutlookBot(AutomationBot):
    def login(self):
        self.log(f"Logging in to Outlook with username: {self.username}")

    def run(self):
        self.log("Running Outlook automation tasks")

    def logout(self):
        self.log("Logging out of Outlook")


# ====================================================================
# SECTION 8: POLYMORPHISM LOOP
# ====================================================================

"""
This is polymorphism.

Same method calls:
    bot.login()
    bot.run()
    bot.logout()

Different object behavior:
    GmailBot logs into Gmail.
    LinkedInBot logs into LinkedIn.
    WhatsAppBot logs into WhatsApp.
    OutlookBot logs into Outlook.
"""

bots = [
    GmailBot("gmail_username", "gmail_password"),
    LinkedInBot("linkedin_username", "linkedin_password"),
    WhatsAppBot("whatsapp_username", "whatsapp_password"),
    OutlookBot("outlook_username", "outlook_password"),
]

for bot in bots:
    bot.login()
    bot.run()
    bot.logout()
    print()


# ====================================================================
# SECTION 9: ADDING A NEW BOT
# ====================================================================

"""
If we need TelegramBot tomorrow, we do not modify existing classes.

We only:
    1. Create TelegramBot.
    2. Implement login(), run(), logout().
    3. Add TelegramBot object to the bots list.

This follows the Open/Closed Principle:
    Open for extension, closed for modification.
"""


class TelegramBot(AutomationBot):
    def login(self):
        self.log(f"Logging in to Telegram with username: {self.username}")

    def run(self):
        self.log("Running Telegram automation tasks")

    def logout(self):
        self.log("Logging out of Telegram")


telegram_bot = TelegramBot("telegram_username", "telegram_password")
telegram_bot.login()
telegram_bot.run()
telegram_bot.logout()


# ====================================================================
# SECTION 10: COMMON MISTAKES
# ====================================================================

"""
Mistake 1:
    Forgetting to implement all abstract methods.

Mistake 2:
    Case mismatch:
        login() and Login() are different methods.

Mistake 3:
    Forgetting self:
        def log(message)        # wrong
        def log(self, message)  # correct

Mistake 4:
    Trying to create an object of an incomplete abstract class.

Mistake 5:
    Trying to access self.__password directly from child class.

Mistake 6:
    Using abstraction when there is only one simple class and no need
    for multiple implementations.
"""


# ====================================================================
# SECTION 11: DEBUGGING NOTES
# ====================================================================

"""
Common Error:
    TypeError: Can't instantiate abstract class GmailBot
    with abstract method run

Meaning:
    GmailBot did not implement all required abstract methods.

Fix:
    Add the missing method exactly as defined in the parent class.

Example:
    Parent has:
        def run(self):

    Child must also have:
        def run(self):

    Not:
        def Run(self):
        def running(self):
"""


# ====================================================================
# SECTION 12: INTERVIEW QUESTIONS
# ====================================================================

"""
Q1. What is abstraction?
A. Abstraction shows essential behavior and hides implementation details.

Q2. What is ABC?
A. ABC stands for Abstract Base Class.

Q3. What does @abstractmethod do?
A. It forces child classes to implement the required method.

Q4. Can an abstract class have normal methods?
A. Yes. Normal methods are useful for shared reusable behavior.

Q5. Can an abstract class have a constructor?
A. Yes. It is useful for initializing common data.

Q6. What is the difference between abstraction and encapsulation?
A. Abstraction hides implementation details.
   Encapsulation protects data inside a class.

Q7. Why use abstraction in an automation framework?
A. It enforces a common structure for all bots, such as login(), run(),
   and logout(), while allowing each bot to implement those methods differently.

Q8. If we add TelegramBot, do we need to modify GmailBot?
A. No. We create a new TelegramBot class and add it to the bots list.
"""


# ====================================================================
# SECTION 13: SENIOR ENGINEER NOTES
# ====================================================================

"""
1. Do not use abstraction everywhere.
   Use it only when multiple implementations are expected.

2. Abstract classes are useful when you want a common contract.

3. Keep shared reusable logic in the parent class.

4. Keep child classes focused on their own specific behavior.

5. Avoid long if-else chains for different bot types.
   Use polymorphism instead.

6. Good software design is not about adding complexity.
   It is about solving the current problem cleanly while allowing
   reasonable future growth.

7. The AutomationBot project follows a clean extensible design:
       - Parent defines contract.
       - Children implement behavior.
       - Loop runs all bots through the same interface.
"""


# ====================================================================
# SECTION 14: DAY 25 SUMMARY
# ====================================================================

"""
Day 25 Summary:

Today we completed OOP Abstraction in Python.

We learned:
    - What abstraction is
    - Why abstraction is needed
    - How to use ABC
    - How to use @abstractmethod
    - How child classes complete abstract contracts
    - How abstraction differs from encapsulation
    - How all four OOP pillars work together

Professional Project:
    Built a Multi-Bot Automation Framework using:
        - AutomationBot abstract parent class
        - GmailBot
        - LinkedInBot
        - WhatsAppBot
        - OutlookBot
        - TelegramBot example

Most Important Takeaway:
    Abstraction is not just "hiding complexity".
    In professional software design, abstraction defines a contract
    that child classes must follow.

End of Day 25.
"""
