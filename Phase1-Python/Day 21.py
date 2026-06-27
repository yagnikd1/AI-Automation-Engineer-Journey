# --------------------------------------------------------------------  Introduction to OOP Classes and Objects ------------------------------------------------------------

# -------------------------- Syntax ---------------------------------

class Employee:
    pass

# -------------------------- Example --------------------------------

class Employee:
    pass

emp1 = Employee()

emp1.name = "John"
emp1.age = 25
emp1.salary = 30000

print(emp1.name)
print(emp1.age)
print(emp1.salary)


# -------------------------- Exercise 1  ---------------------------------

class Student:
    pass

student1 = Student()

student1.name = "Jenny"
student1.age = 30
student1.course = "Automation"

print(student1.name)
print(student1.age)
print(student1.course)

print("\n")


# -------------------------- Exercise 2  ---------------------------------

class Car:
    pass

car1 = Car()

car1.brand = "BMW"
car1.model = "X1"
car1.price = "$10000"

print(car1.brand)
print(car1.model)
print(car1.price)

print("\n")


# -------------------------- Exercise 3  ---------------------------------

class Book:
    pass

book1 = Book()
book2 = Book()
book3 = Book()

book1.title = "Psychology"
book1.author = "socrates"
book1.price = "$ 12"

book2.title = "Atomic Habits"
book2.author = "James clear"
book2.price = "$ 40"

book3.title = "YOU CAN"
book3.author =  "George Matthew Adams"
book3.price = "$ 9"

print(book1.title)
print(book1.author)
print(book1.price)
print("\n")

print(book2.title)
print(book2.author)
print(book2.price)
print("\n")

print(book3.title)
print(book3.author)
print(book3.price)
print("\n")


# -------------------------- Exercise 4  ---------------------------------



class Book:
   pass

book1 = Book()
book2 = Book()
book3 = Book()
book4 = Book()
book5 = Book()

book1.title = "Psychology"
book1.author = "Socrates"
book1.price = 12

book2.title = "Atomic Habits"
book2.author = "James Clear"
book2.price = 40

book3.title = "YOU CAN"
book3.author = "George Matthew Adams"
book3.price = 9

book4.title = "Metamorphosis"
book4.author = "Franz Kafka"
book4.price = 8

book5.title = "The Alchemist"
book5.author = "Paulo Coelho"
book5.price = 20 

books = [book1, book2, book3, book4, book5]

for book in books:
    print(book.title)
    print(book.author)
    print(book.price)
    print()
    
print("\n")


# -------------------------- Constructor __init__ & Self (Current object) ---------------------------------

# -------------------------- Syntax ---------------------------------

# book1 = Book("Psychology", "Socrates", 12)

# How do we make that work?

class Book:

    def __init__(self, title, author, price):
        self.title = title
        self.author = author
        self.price = price


# -------------------------- Example ---------------------------------

class Book:
    pass

    def __init__(self, title, author, price):
        self.title = title
        self.author = author
        self.price = price


book1 = Book("Psychology", "Socrates", 12)

print(book1.title)
print(book1.author)
print(book1.price)

print("\n")

# -------------------------- Example ---------------------------------

class student:

    def __init__(self, name, age, course):
        self.name = name
        self.age = age
        self.course = course

student1 = student("Jenny", 30, "Automation")

print(student1.name)
print(student1.age)
print(student1.course)

print("\n")



# -------------------------- Methods (Functions Inside a Class) ---------------------------------

# ---- In OOP, actions are called methods.

# ---- Syntax

class Student:

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def introduce(self):
        print("Hello")


# ---- introduce() looks almost identical to a normal function.
# ---- It is a function just belongs to the class


# -------------------------- Example ---------------------------------

class Student:

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def introduce(self):
        print("My name is", self.name)
        print("My age is", self.age)

student1 = Student("Jenny",30)

student1.introduce()

print("\n")


# -------------------------- Exercise  1 ---------------------------------

class Car:

    def __init__(self, brand, model, price):
        self.brand = brand
        self.model = model
        self.price = price

    def show_details(self):
        print("This is a", self.brand)
        print("\n")
        print("its the recent Model", self.model)
        print("\n")
        print("The current Price is", self.price,)
        print("\n")

car1 = Car("BMW", "X1", 10000)
car2 = Car("Mazda", "RX-7", 25000)
car3 = Car("Nissan", "R34 GTR", 50000)

car1.show_details()
car2.show_details()
car3.show_details()


print("\n")


# -------------------------- Exercise  2 ---------------------------------

class Book:

    def __init__(self, title, author, price):
        self.title = title
        self.author = author
        self.price = price

    def book_info(self):
            print("The Title of this book is", self.title)
            print("The Author of this book is", self.author)
            print("The Price of this book is", self.price)
            

book1 = Book("Metamorphosis", "Franz Kafka", 10)
book2 = Book("Atomic Habits", "James Clear", 15)
book3 = Book("You CAN", "George Matthew Adams", 12)        
book4 = Book("The Alchemist", "Paulo Coelho", 9) 
book5 = Book("Meditations", "Marcus Aurelius", 8) 

books = [book1, book2, book3, book4, book5]

for book in books:
    book.book_info()
    print() 

print("\n")

# -------------------------- Methods Can Return Values ---------------------------------

# -------------------------- Example --------------------------------

class Book:

    def __init__(self, title, price):
        self.title = title
        self.price = price

    def discount(self):
        return self.price * 0.9
    
book1 = Book("Atomic Habits", 100)

print(book1.discount())


# -------------------------- Exercise 1  --------------------------------

class Book:

    def __init__(self, title, price):
        self.title = title
        self.price = price

    def discount_price(self):
        return self.price - (self.price * 0.10)

book1 = Book("Metamorphois", 50)

print(book1.discount_price())

# -------------------------- Exercise 2  --------------------------------

class Employee:

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def yearly_salary(self):
        return self.salary * 12 

employee1 = Employee("John", 50000)

print(employee1.name,"earns", employee1.yearly_salary(), "per year")

print("\n")


# ----------------------------------------------------------------------- Mini Project -------------------------------------------------------

class Book:

    def __init__(self, title, author, price):
        self.title = title
        self.author = author
        self.price = price

    def book_info(self):
        print("The Title of this book is", self.title)
        print("The Author of this book is", self.author)
        print("The Price of this book is", self.price)

    def discount_price(self):
        if self.price > 20:
            return self.price - (self.price * 0.15)
        else:
            return self.price - (self.price * 0.10)


book1 = Book("Metamorphois","Franz Kafka", 50)
book2 = Book("Atomic Habit","James Clear", 15)
book3 = Book("The Alchemist","Paulo Coelho", 10)
book4 = Book("You Can", "George Matthew Adams", 9)    
book5 = Book("Meditation","Marcus Aurelius", 20)

books = [book1, book2, book3, book4, book5]

for book in books:
    book.book_info()
    print("Discount Price: ₹", book.discount_price())
    print()



