# --------------------------------------------------– Functions ----------------------------------------------------

def show_name():
    print("Amit")

show_name()

print("\n")

# ----------------------------------- New Concept: Functions with Input

#name = input("Enter Name: ")

#    print(name)

#show_name()


print("\n")


# ----------------------------------- write fucntion and call it 3 times

city = "Morbi"

def show_city():
    print(city)

show_city()
show_city()
show_city()



print("\n")

# ----------------------------------- write fucntion to check bonu eligiblity

salary = 25000

def check_bonus():
    if salary > 20000:
        print("Bonus Eligible")

check_bonus()

print("\n")


# --------------------------------------------------– Functions + Parameters ----------------------------------------------------

def show_city(city):
    print(city)

show_city("Morbi")
show_city("Rajkot")



print("\n")

# ----------------------------------- print product then call it tiles

def show_product(product):
    print(product)

show_product("Tiles")



print("\n")


# ----------------------------------- print salary > 2000  then call it 25000


def check_bonus(salary):
    if salary > 20000:
        print("Bonus Eligible")
    else:
        print("No Bonus")

check_bonus(25000)
check_bonus(18000)

print("\n")


# --------------------------------------------------– Functions + Return ----------------------------------------------------


# -----------------------------------  Example 1 

def get_city():
    return "Morbi"

city = get_city()

print(city)


print("\n")

# ----------------------------------- Example 2 

def get_salary():
    return 25000

salary = get_salary()

print(salary)



print("\n")

# ----------------------------------- Predict the output

def get_name():
    return "Amit"

print(get_name())



print("\n")

# ----------------------------------- Write A function that returns tiles

def get_product():
    return "Tiles"

product = get_product()

print(product)

print("\n")


# ----------------------------------- Write A function that returns 250000

def get_salary():
    return 25000

salary =  get_salary()

print(salary)


print("\n")




# --------------------------------------------------– Functions + If\ELse ----------------------------------------------------


# ----------------------------------- Example 1 


def check_bonus(salary):
    if salary > 20000:
        return " Bonus Eligible"
    else:
        return "No Bonus"
    
result = check_bonus(25000)

print(result)


print("\n")


# ----------------------------------- Example 2 

def check_age(age):
    if age >= 18:
        return "Adult"
    else:
        return "Minor"
    
print(check_age(25))

print("\n")

# ----------------------------------- Exercise 

def check_mark(marks):
    if marks >= 35:
        return "Pass"
    else:
        return "Fail"

print(check_mark(20))
print(check_mark(50))


print("\n")


# --------------------------------------------------–------------------------ Functions + Mini Project ----------------------------------------------------


# ----------------------------------- Employee Status Checker

def check_employee(salary):

    if salary >= 20000:
        return "Bonus Eligible"
    else:
        return "No Bonus"
        
print(check_employee(15000))
print(check_employee(25000))
print(check_employee(30000))

