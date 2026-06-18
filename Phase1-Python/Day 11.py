# -------------------------------------------------------- Dictionaries -------------------------------------------------------------------------------------------------

# ---------------- First dictionary program

employee = {
    "name": "Rahul",
    "age": 25 }

print(employee)



# ---------------- Challenge - 1 Access Value

employee = {
    "name": "Rahul",
    "age": 25}

print(employee["name"])



# ---------------- Challenge - 2 Access Age

employee = {
    "name": "Rahul",
    "age": 25}

print(employee["age"])



# ---------------- Change Existing Information

employee = {"Name": "Rahul", "age": "25"}
employee["age"] = 26
print(employee)

# ----------

employee = {
    "name": "Rahul",
    "age": 25 }

employee["city"] = "Rajkot"

print(employee)



# ---------------- Multiple Employees

employees = [{"name": "Rahul", "age": 25}, {"name": "Amit", "age": 30}]
print(employees[1]["age"])


# --------------------

employees = [{"name" : "Rahul", "city" :"Rajkot"}, {"name": "Amit", "city": "Morbi"}, {"name": "Neha", "city": "Surat"}]

print(employees[2]["name"])



# ---------------- Add New Information

employee = {"name": "Neha", "age": 25}

employee["city"] = "Surat"

print(employee)



# ---------------- Create and print this entire dictionary

employee = {"name":"Yagnik", "city":"Morbi", "Job":"Ceramic Supervisor"}

print(employee)
print(employee["city"])
print(employee["Job"])






#------------------------------------------------------------- Exercises -------------------------------------------------
#-----------------------------------------------------------
#-----------------------------------------------------
# -------------------  Exercise 1 - Print One Value

employee = {"name":"Rahul", "city":"Rajkot"}
print(employee["name"])


print("\n")
# -------------------  Exercise 2 - Print age

employee = {"name": "Amit", "age": 30}
print(employee["age"])


print("\n")
# -------------------  Exercise 3 - Add new information

employee = {"name": "Rahul", "age":25}

employee["age"] = 26

print(employee["age"])


print("\n")
# -------------------  Exercise 5 - Predict Output (No Coding)

employee = {"name": "piya", "city": "Ahmedabad"}

print(employee["city"])


print("\n")
# -------------------  Exercise 6 - Multiple Employees

employees = [{"name": "Rahul", "age":25}, {"name":"Amit", "age":30}]

print(employees[1]["name"])


print("\n")
# -------------------  Exercise 7 - Print age - 25

employees = [{"name": "Rahul", "age":25}, {"name":"Amit", "age":30}]

print(employees[0]["age"])


print("\n")
# -------------------  Exercise 8 - Predict the output

employees = [{"name":"Rahul", "city":"Rajkot"}, {"name":"Amit", "city":"Morbi"}]

print(employees[1]["city"])


print("\n")
# -------------------  Exercise 9 real automation style

employee = {"name":"Yagnik", "city":"Morbi", "Job":"Ceramic Supervisor"}
print(employee)


print("\n")
# -------------------  Exercise 10 Using Exercise 9 dictionary print only Morbi 


employee = {"name":"Yagnik", "city":"Morbi", "Job":"Ceramic Supervisor"}
print(employee["city"])


print("\n")
# -------------------  Bonus Challenge

employee = {"name":"Rahul", "age": 25}

employee["age"]=35

print(employee["age"])