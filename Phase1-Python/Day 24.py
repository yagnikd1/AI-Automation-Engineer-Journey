# =====================================================================
# Day 24 - OOP Polymorphism
# AI Automation Engineer Journey
# =====================================================================
#
# Topics covered:
# 1. What is Polymorphism?
# 2. Method Overriding and Runtime Polymorphism
# 3. Duck Typing
# 4. Polymorphism in AI Automation Projects
# 5. Common Debugging Mistake
# 6. Mini Project: Notification System
#
# Simple definition:
# Polymorphism means the same method name can behave differently
# depending on the object that is using it.
#
# Example:
# dog.speak()  -> Bark
# cat.speak()  -> Meow
#
# Same method name: speak()
# Different behavior: Bark / Meow
# =====================================================================

class Dog:
    def speak(self):
        print("Dog says: Bark")

class Cat:
    def speak(self):
        print("Cat says: Meow")

def make_sound(animal):
    animal.speak()

print("----- Basic Polymorphism Example -----")
dog=Dog(); cat=Cat(); make_sound(dog); make_sound(cat)
