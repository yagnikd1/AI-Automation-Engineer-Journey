# ==========================================
# Day 22 - OOP Practice: Employee Management
# AI Automation Engineer Journey
# ==========================================

# Goal:
# Build a small Employee Management System using OOP.
# This file continues from Day 21 and avoids repeating basic OOP examples.


# ==========================================
# Employee Class
# ==========================================

class Employee:

    def __init__(self, name, age, department, role, salary, employee_code):
        self.name = name
        self.age = age
        self.department = department
        self.role = role
        self.salary = salary
        self.employee_code = employee_code

    def show_details(self):
        print("Employee Name:", self.name)
        print("Employee Age:", self.age)
        print("Department:", self.department)
        print("Role:", self.role)
        print("Salary:", self.salary)
        print("Employee Code:", self.employee_code)

    def yearly_salary(self):
        return self.salary * 12

    def increase_salary(self, amount):
        if amount > 0:
            self.salary += amount
        else:
            print("Invalid increment amount.")

    def change_department(self, new_department):
        self.department = new_department

    def change_role(self, new_role):
        self.role = new_role


# ==========================================
# Section 1 - Create One Employee
# ==========================================

employee1 = Employee("Jordan", 30, "Automation", "Developer", 50000, "EMP001")

print("=" * 45)
print("SECTION 1 - Employee Details")
print("=" * 45)

employee1.show_details()


# ==========================================
# Section 2 - Department and Role Change
# ==========================================

print("\n" + "=" * 45)
print("SECTION 2 - Department & Role Change")
print("=" * 45)

print("Before Department and Role Change:")
employee1.show_details()

employee1.change_department("AI Research")
employee1.change_role("AI Automation Engineer")

print()
print("After Department and Role Change:")
employee1.show_details()


# ==========================================
# Section 3 - Salary Increment with Validation
# ==========================================

print("\n" + "=" * 45)
print("SECTION 3 - Salary Increment")
print("=" * 45)

print("Before Increment:")
employee1.show_details()

employee1.increase_salary(5000)

print()
print("After Valid Increment:")
employee1.show_details()

print()
employee1.increase_salary(-5000000)

print()
print("After Invalid Increment Attempt:")
employee1.show_details()


# ==========================================
# Section 4 - Yearly Salary
# ==========================================

print("\n" + "=" * 45)
print("SECTION 4 - Yearly Salary")
print("=" * 45)

print("Yearly Salary:", employee1.yearly_salary())


# ==========================================
# Section 5 - Multiple Employee Objects
# ==========================================

employee2 = Employee("Jenny", 25, "Machine Learning", "ML Engineer", 40000, "EMP002")
employee3 = Employee("Pedro", 30, "Automation", "AI Engineer", 45000, "EMP003")

employees = [employee1, employee2, employee3]

print("\n" + "=" * 45)
print("SECTION 5 - Multiple Employees")
print("=" * 45)

for employee in employees:
    employee.show_details()
    print()


# ==========================================
# Mini Project - Employee Management System
# ==========================================

print("\n" + "=" * 45)
print("MINI PROJECT - Employee Management System")
print("=" * 45)

# Update one employee only.
employee2.increase_salary(5000)
employee2.change_department("AI Engineering")
employee2.change_role("AI Automation Engineer")

print("Updated Employee Details:")
employee2.show_details()
print("Yearly Salary:", employee2.yearly_salary())


print("\n" + "=" * 45)
print("MINI PROJECT - Final Employee List")
print("=" * 45)

for employee in employees:
    employee.show_details()
    print()


# ==========================================
# Day 22 Summary
# ==========================================

# Today we practiced:
# 1. Creating a class.
# 2. Creating objects from a class.
# 3. Using __init__ to set object data.
# 4. Writing methods that display object data.
# 5. Writing methods that return calculated values.
# 6. Writing methods that modify object data.
# 7. Adding validation before changing object data.
# 8. Storing multiple objects in a list.
# 9. Looping through object lists.
# 10. Building a small Employee Management System.
