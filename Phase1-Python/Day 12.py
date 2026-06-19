# ------------------------------------  Dictionary Practice ----------------

# --------------- print only city

employee = {"name": "amit", "age": "30", "city": "Morbi"}

print(employee["city"])


print("\n")

# --------------- print Tiles - 250

product = {"name": "Tiles", "price": 250}

print(product["name"])
print(product["price"])


print("\n")

# --------------- Write Code  - Create a dictionary

employee = {"name": "Neha", "Age": 28, "City": "Ahmedabad"}

print(employee["name"])
print(employee["City"])


print("\n")

# --------------- Mini Project 1 (Real World) Ceramic Company Employee Card

employee = {"Employee": "Rahul", "Department": "Production", "Salary": 25000}

print("Employee:",  (employee["Employee"])) 
print("Department:", (employee["Department"]))
print("Salary:", (employee["Salary"]))


print("\n")

# ---------------  Dictionary + FOR Loop --------------------------------------------------------------------------------

# New concept. -----------------------------------------------------------------------------------------

employee = {
    "Rahul": 25000,
    "Amit": 18000,
    "Neha": 30000

}

print(employee)


print("\n")

# ---------------  predict the output

employees = {
    "Rahul": 25000,
    "Amit": 18000,
    "Neha": 30000
}

for employee in employees:
    print(employee)



print("\n")

# ---------------  Print Ceramic City - Engineering City 

cities = { 
    "Morbi": "Ceramic City",
    "Surat": "Diamond City",
    "Rajkot": "Engineering City"
}

print(cities["Morbi"])
print(cities["Rajkot"])


print("\n")

# ---------------   Mini Project 2 Create a dictionary:

product = {
    "Tiles": 250,
    "Sanitary Price": 500,
    "Adhesive Price" : 100
}

print("Tiles:",(product["Tiles"]))
print("Sanitary Price:",(product['Sanitary Price']))
print("Adhesive Price:",(product["Adhesive Price"]))



print("\n")

# --------------------------------------------------------  New Concept: Dictionary + FOR Loop + IF/ELSE

employees = {
    "Rahul": 25000,
    "Amit": 18000,
    "Neha": 30000
}

for employee in employees:
    if employees[employee] > 20000:
        print(employee, "Bnous Eligible") 




print("\n")

# --------------- Mini Project 3 -- Ceramic Inventory Checker

products = {
    "Tiles": 250,
    "Adhesive": 100,
    "Sanitary": 500,
    "Cement": 150
}

for product in products:
    if products[product] > 200:
        print(product)




print("\n")

# --------------- Dictionary + Input      

name = input("Enter your Name: ")
city = input("Enter City: ")

employee = {
    "name" : name,
    "city" : city
}

print("Name:", employee["name"])
print("City:", employee["city"])

print("\n")

# --------------- Mini Database Project

employee = {
    "name": "Rahul",
    "department": "Production",
    "salary": 25000 }

if employee["salary"] > 20000:
    print("Bonus Eligible")
else:
    print("No Bonus")



print("\n")


# --------------------------------------- Larger Projects ---------------------------


# --------------- Employee Bonus System


employees = {
    "Rahul": 25000,
    "Amit": 18000,
    "Neha": 30000,
    "Priya": 15000
}

for employee in employees:
    if employees[employee] > 20000:
        print(employee, "Bonus Eligible")