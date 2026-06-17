# ------------------------------------------------------- List ------------------------------------------

# ------------------------- Accessing Items ----------------

employees = ["Rahul", "Amit", "Neha", "Priya"]

print(employees[0])

print(employees[1])

print(employees[2])

print(employees[3])



# ------------------------------   Replace an Item

cities = [ "Morbi", "Rajkot", "Surat"]

cities [1] = "Ahemdabad"
print(cities)



# ------------------------------   Remove an Item


cities = [ "Morbi", "Rajkot", "Surat"]

cities.remove("Rajkot")

print(cities)



# ------------------------------   Length of List

cities = ["Morbi", "Rajkot", "Surat"]

print(len(cities))


# ------------------------------ Check if Item Exists

cities = ["Morbi", "Rajkot", "Surat"]

if "Morbi" in cities:
    print("Found")
else: 
    print("Not found")



# ------------------------------ User Adds Items

cities = []

city = input("Enter City: ")

cities.append(city)

print(cities)



# ------------------------------ Multiple Appends

cities = []

cities.append("Rajkot")
cities.append("Morbi")
cities.append("Surat")
cities.append("Diu")

print(cities)



# ---------------------------------- List challenges ---------


# ---------------------------- Challenge - 1

cities = ["Morbi", "Rajkot", "Surat"]

print(cities)

print(cities[0])

print(cities[2])

print(cities[2])




# ---------------------------- Challenge - 2

employees = ["Rahul", "Amit", "Neha", "Priya"]

print(employees[0])
print(employees[2])




# ---------------------------- Challenge - 3

employees = ["Rahul", "Amit", "Neha", "Priya"]

for employee in employees:
    print(employee)
    



# ---------------------------- Challenge - 4

cities = ["Morbi", "Rajkot", "Surat"]

cities.append("Ahmedabad")

print(cities)