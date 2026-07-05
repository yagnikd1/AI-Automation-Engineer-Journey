"""
Phase 1 Completion Project
Employee Management System - Console CRUD Application

Concepts used:
- Variables and data types
- Lists and dictionaries
- Conditions and loops
- Functions
- File handling
- Error handling
- os module
"""

import os

employees = []
FILE_NAME = "employee_records.txt"


def create_employee():
    """Create one employee record from user input."""
    try:
        name = input("Enter employee name: ")
        age = int(input("Enter employee age: "))
        department = input("Enter employee department: ")
        salary = float(input("Enter employee salary: "))

        employee = {
            "name": name,
            "age": age,
            "department": department,
            "salary": salary
        }

        return employee

    except ValueError:
        print("Please enter valid numbers.")
        return None


def add_employee():
    """Add an employee to the employee list."""
    employee = create_employee()

    if employee is not None:
        employees.append(employee)
        print("Employee added successfully.")


def view_employees():
    """Display all employee records."""
    if len(employees) == 0:
        print("No employees found.")
    else:
        count = 1

        for employee in employees:
            print("\nEmployee", count)
            print("=" * 30)
            print("Name:", employee["name"])
            print("Age:", employee["age"])
            print("Department:", employee["department"])
            print("Salary:", employee["salary"])
            count += 1


def search_employee():
    """Search for an employee by name."""
    search_name = input("Enter employee name to search: ")

    for employee in employees:
        if employee["name"].lower() == search_name.lower():
            print("\nEmployee Found")
            print("=" * 30)
            print("Name:", employee["name"])
            print("Age:", employee["age"])
            print("Department:", employee["department"])
            print("Salary:", employee["salary"])
            return

    print("Employee not found.")


def delete_employee():
    """Delete an employee by name."""
    delete_name = input("Enter employee name to delete: ")

    for employee in employees:
        if employee["name"].lower() == delete_name.lower():
            employees.remove(employee)
            print("Employee deleted successfully.")
            return

    print("Employee not found.")


def save_employees():
    """Save all employees to a text file."""
    file = open(FILE_NAME, "w")

    for employee in employees:
        file.write(
            employee["name"] + "," +
            str(employee["age"]) + "," +
            employee["department"] + "," +
            str(employee["salary"])
        )
        file.write("\n")

    file.close()
    print("Employees saved successfully.")


def load_employees():
    """Load employees from a text file if it exists."""
    if os.path.exists(FILE_NAME):
        file = open(FILE_NAME, "r")

        for line in file:
            data = line.strip().split(",")

            if len(data) == 4:
                try:
                    employee = {
                        "name": data[0],
                        "age": int(data[1]),
                        "department": data[2],
                        "salary": float(data[3])
                    }

                    employees.append(employee)

                except ValueError:
                    print("Skipped invalid employee record:", line.strip())

        file.close()


def menu():
    """Run the main employee management menu."""
    load_employees()

    while True:
        print("\n===== Employee Management =====")
        print("1. Add Employee")
        print("2. View Employees")
        print("3. Search Employee")
        print("4. Delete Employee")
        print("5. Save")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_employee()

        elif choice == "2":
            view_employees()

        elif choice == "3":
            search_employee()

        elif choice == "4":
            delete_employee()

        elif choice == "5":
            save_employees()

        elif choice == "6":
            save_employees()
            print("Program closed.")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    menu()
