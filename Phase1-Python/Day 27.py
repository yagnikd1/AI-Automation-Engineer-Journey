# ============================================================
# Day 27 - Employee Management System (Console Application)
# AI Automation Engineer Journey - Phase 1 (Python)
#
# Concepts Used:
# - Classes & Objects
# - Inheritance
# - Encapsulation
# - Polymorphism
# - Magic Methods
# - Functions
# - Lists
# - Loops
# - Conditional Statements
# ============================================================

class Person:

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def display(self):
        print("Name:", self.name)
        print("Age:", self.age)


class Employee(Person):

    def __init__(self, name, age, employee_id, department, salary):
        super().__init__(name, age)
        self.employee_id = employee_id
        self.department = department
        self.__salary = salary

    def display(self):
        super().display()
        print("Employee ID:", self.employee_id)
        print("Department:", self.department)
        print("Salary:", self.__salary)

    def get_salary(self):
        return self.__salary

    def set_salary(self, salary):
        self.__salary = salary

    def __str__(self):
        return f"ID: {self.employee_id}, Name: {self.name}, Department: {self.department}, Salary: {self.__salary}"

    def __eq__(self, other):
        return self.employee_id == other.employee_id


# ----------------------------
# Employee Storage
# ----------------------------
employees = []


# ----------------------------
# Menu Functions
# ----------------------------

def show_menu():
    print("\n===== Employee Management System =====")
    print("1. Add Employee")
    print("2. View Employees")
    print("3. Search Employee")
    print("4. Update Salary")
    print("5. Delete Employee")
    print("6. Exit")


# ----------------------------
# Employee Functions
# ----------------------------

def add_employee():
    name = input("Enter name: ")
    age = int(input("Enter age: "))
    employee_id = input("Enter employee ID: ")
    department = input("Enter department: ")
    salary = float(input("Enter salary: "))

    emp = Employee(name, age, employee_id, department, salary)
    employees.append(emp)

    print("Employee added successfully.")


def view_employees():
    if len(employees) == 0:
        print("No employees found.")
    else:
        for emp in employees:
            print(emp)


def search_employee():
    search_id = input("Enter employee ID to search: ")

    for emp in employees:
        if emp.employee_id == search_id:
            print("Employee found:")
            emp.display()
            return

    print("Employee not found.")


def update_salary():
    search_id = input("Enter employee ID to update salary: ")

    for emp in employees:
        if emp.employee_id == search_id:
            new_salary = float(input("Enter new salary: "))
            emp.set_salary(new_salary)
            print("Salary updated successfully.")
            return

    print("Employee not found.")


def delete_employee():
    search_id = input("Enter employee ID to delete: ")

    for emp in employees:
        if emp.employee_id == search_id:
            employees.remove(emp)
            print("Employee deleted successfully.")
            return

    print("Employee not found.")


# ----------------------------
# Main Program
# ----------------------------

if __name__ == "__main__":

    while True:
        show_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            add_employee()

        elif choice == "2":
            view_employees()

        elif choice == "3":
            search_employee()

        elif choice == "4":
            update_salary()

        elif choice == "5":
            delete_employee()

        elif choice == "6":
            print("Exiting program...")
            break

        else:
            print("Invalid choice. Please try again.")
