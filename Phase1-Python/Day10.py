# ---------------------------- List  -----------------------


# ---------------------------- List Program - 1  -----------------------

cities = [ "Morbi", "Rajkot", "Surat"]

cities.append("Ahmedabad")

for city in cities:
    print(city)

print(len(cities))

cities[2] = "Vadodara" 

print(cities)

cities.remove("Rajkot")

print(cities)



# ---------------------------- List - Append, Remove, replace, length  -----------------------

cities = ["Morbi", "Rajkot", "Surat", "Vadodra", "Ahmedabad"]
print(cities)

print("\n")

cities.remove("Morbi")
cities.remove("Surat")
cities.remove("Ahmedabad")

print(cities)
print("\n")

cities.append("Junagadh")
cities.append("Jamnagar")
cities.append("Veraval")

print(cities)
print("\n")

cities[2] = "Sasan Gir"
print(cities)
print("\n")

print(len(cities))