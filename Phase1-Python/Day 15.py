# ----------------------------------------------------------------------------------- File Handling ---------------------------------------------------------------------

# ------------------------ Concept 1 - Writing to a File

file = open("notes.txt", "w")
file.write("hello world")
file.close


# ------------------------ Concept 1 - Reading a File

file = open("notes.txt", "r")

content = file.read()

print(content)

file.close()

print("\n")
# ------------------------ First Real File Project - Employee File Saver  - "w"

file = open("employee.txt", "w")
file.write("Rahul")
file.close()



# ------------------------ File Reader Project - "r"
 
file = open("employee.txt", "r")

content = file.read()

print(content)

file.close()

print("\n")
# ---------------------------------------------------------------------------------------- Overwriting Files

file = open("employee.txt", "w")

file.write("Morbi")

file.close


file = open("employee.txt", "w")

file.write("Surat")

file.close


file = open("employee.txt", "r")

content = file.read()

print(content)

file.close()


print("\n")
# ---------------------------------------------------------------------------------------- Append Mode - "a"

file = open("city.txt", "w")

file.write("Morbi")

file.close()

file = open("city.txt", "a")

file.write(" Surat")

file.close()

file = open("city.txt", "r")

content = file.read()

print(content)

file.close()


print("\n")

# ---------------------------------------------------------------------------------------- File Handling + Input

name = input("Enter Name: ")

file = open("employee.txt", "w")

file.write(name)

file.close()

file = open("employee.txt", "r")

content = file.read()

print(content)

file.close()

print("\n")

# ------------   Example 2 

city = input("Enter City: ")

file = open("city.txt", "w")

file.write(city)

file.close()

file = open("city.txt", "r")

content = file.read()

print(content)

file.close()


print("\n")

# ------------   Exercise 

name = input("Enter Name: ")

file = open("employee.txt", "w")

file.write(name)

file.close

print("\n")



# ------------   Exercise 2

name = input("Enters Name: ")
city = input("Enter City: ")

file = open("employee.txt", "w")

file.write(name)
file.write("\n")
file.write(city)

file.close()


file = open("employee.txt", "r")

content = file.read()

print(content)

file.close()


print("\n")