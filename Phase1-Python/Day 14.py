# ----------------------------------------------------------   Functions + Lists  ---------------------------------------

# ----------------------- predict the output

def show_fruits():
    fruits = ["Apple", "Banana"]

    for fruit in fruits:
        print(fruit)
    
show_fruits()



print("\n")

# ----------------------- predict the output

def show_employees():
    employees = ["Rahul", "Amit", "Neha"]

    for employee in employees:
        print(employee)

show_employees()

print("\n")



# ----------------------------------------------------------   Functions + Lists + IF/ELSE  ---------------------------------------


# ---------------------- Example

def check_number():
    numbers = [5, 15, 25]

    for number in numbers:
        if number > 10:
            print(number)

check_number()


print("\n")

# ---------------------- Predict the output

def check_numbers():
    numbers =  [3, 12, 8, 20]

    for number in numbers:
        if number >10:
            print(number)

check_numbers()

print("\n")


# ---------------------- Predict the output

def check_marks():
    marks = [20, 50, 30, 80]

    for mark in marks:
        if mark >= 35:
            print("Pass")

check_marks()

print("\n")

# ---------------------- Write function

def show_big_numbers():

    numbers = [2, 8, 15, 25, 5]

    for number in numbers:
        if number > 10:
            print(number)

show_big_numbers()

print("\n")



# ----------------------------------------------------------   Functions + Return + Lists   ---------------------------------------

def get_biggest():

    numbers = [5, 10, 25]

    return max(numbers)

print(get_biggest())


print("\n")


# ---------------------- Predict the output

def get_city():

    cities = [ "Morbi", "Rajkot"]
    
    return cities[0]

print(get_city())

print("\n")

# ---------------------- Predict the output

def get_number():
    numbers = [ 5, 10, 20]

    return numbers[2]

print(get_number())

print("\n")

# ---------------------- Write function

def get_first_employee():

    employee = ["Rahul", "Amit", "Neha"]

    return employee[0]

print(get_first_employee())

print("\n")


# ----------------------------------------------------------   Mini Project  ---------------------------------------


# ---------------------- Employee Salary Checker

def count_bonus_employees():

    salaries = [ 15000, 25000, 18000, 30000, 22000]
    count = 0

    for salary in salaries:

        if salary >= 20000:
            count += 1

    return count
     
        
print(count_bonus_employees())


print("\n")

# ----------------------------------------------------------   Functions + Dictionaries  ---------------------------------------------------------------------------

# ---------------------- Example 1 

def show_employee():
    
    employee = {
        "name" : "Rahul",
        "salary": 25000
    }

    print(employee["name"])

show_employee()



print("\n")

# ---------------------- Example 2


def show_salary():

    employee = {
        "name": "Rahul",
        "salary": 25000
    }

    return employee["salary"]

print(show_salary())

print("\n")

# ---------------------- Predict Output

def show_city():

    employee = {
        "name": "Amit",
        "city": "Morbi"
    }

    print(employee["city"])

show_city()

print("\n")

# ---------------------- Predict Output


def get_name():

    employee = {

        "name": "Neha",
        "salary": 30000
    }
    return (employee["name"])

print(get_name())


print("\n")



# ---------------------- Write function - print name

def show_products():

    product = {
        "name": "Tiles",
        "price": 250
    }

    print(product["name"])

show_products()

print("\n")


# ---------------------- Write function - return price

def show_products():

    products = {
        "name": "Tiles",
        "price": 250
    }

    return(products["price"])

print(show_products())

print("\n")


# ----------------------------------------------------------   Real Mini Project  ---------------------------------------


# ---------------------- Employee Bonus Checker

def check_employee_bonus():
    
    employee = {

        "name": "Rahul",
        "salary": 25000
    }

    if employee["salary"] >= 20000:
        return "Bonus Eligible"
    else:
        return "No Bonus"
    
    

print(check_employee_bonus())


print("\n")



# ----------------------------------------------------------   Functions + Dictionaries + FOR Loops  -----------------------------------------------------------------------

# ---------------------- Example 1 


def show_employees():

    employees = {
        "Rahul": 25000,
        "Amit": 18000,
        "Neha": 30000
    }

    for employee in employees:
        print(employee)

show_employees()

print("\n")



# ---------------------- Example 2


def show_salaries():

    employees = {
        "Rahul": 25000,
        "Amit": 18000,
        "Neha": 30000
    }

    for employee in employees:
        print(employees[employee])

show_salaries()

print("\n")


# ---------------------- predict output

def show_products():

    products = {
        "Tiles": 250,
        "Adhesive": 100,
        "Sanitary" : 500
    }

    for product in products:
        print(product)

show_products()

print("\n")


# ---------------------- predict output

def show_prices():

    products = {
        "Tiles": 250,
        "Adhesive": 100,
        "Sanitary": 500
    }

    for product in products:
        print(products[product])
    
show_prices()


print("\n")


# ---------------------- write fucntion

def show_cities():

    cities = {
        "Morbi": "Ceramic City",
        "Surat": "Diamond City",
        "Rajkot": "Engineerinf City"
    }

    for city in cities:
        print(city)

show_cities()

print("\n")


# ---------------------- write fucntion


def show_cities():

    cities = {
        "Morbi": "Ceramic City",
        "Surat": "Diamond city",
        "Rajkot": "Engineering City"
    }

    for city in cities:
        print(cities[city])

show_cities()

print("\n")




# ----------------------------------------------------------   Real Employee Bonus Project -----------------------------------------------------------------------


def check_bonus_eligible():

    employees = {
        "Rahul": 25000,
        "Amit": 18000,
        "Neha": 30000,
        "Priya": 15000
    }

    for employee in employees:
        if employees[employee] >= 20000:
            print(employee, "Bouns Eligible")

check_bonus_eligible()

print("\n")

    