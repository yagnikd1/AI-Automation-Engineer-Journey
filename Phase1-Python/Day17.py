# ----------------------------------------------------------------------------------------------------------- Error Handling -------------------------------------------


# ------------------------------------------------------------------------------ Why Error Handling Exists

# ----------------------- Example

try:

    number = int(input("Enter NUmber: "))
    print(number)

except: 
    print("please enter valid number")


print("\n")

# ----------------------- Exercise

try:

    age = int(input("Enter Age: "))
    print("You Entered:",   age)

except:
    print("please enter valid number")

print("\n")

# ----------------------- Project - Enter Valid Salary

try:
    
    salary = int(input("ENter Salary: "))

    if salary  >= 20000:
        print("Bonus Eligible")
    else:
        print("No Bonus")

except:
    print("Please enter a valid salary")

print("\n")

# ----------------------- File Error Project

try:
    
    file = open("report.txt", "r")
    content = file.read()
    print(content)
    file.close()

except:
    print("Report file not found")

print("\n")



# ----------------------- Enter File Name Project

try:

    filename = input("Enter Filename: ")

    file = open(input(filename, "r"))

    content = file.read()

    print(content)
    
    file.close()

except:
    print("File not found")

print("\n")



# ----------------------------------------------------------------------------------------------------  Specific Error Handling ---------------------------------------


# ----------------------- Example ValueError

try:

    number = int(input("Enter Number: "))

except ValueError:
    print("Please enter a valid number")

print("\n")

# ----------------------- Another Example FileNotFoundError

try:

    file = open("report.txt", "r")

except FileNotFoundError:
    print("File Not Found")

print("\n")


# ----------------------- Professional Error Program

try:
    age = int(input("Enter Age: "))
    if age >= 18:
        print("Adult")
    else:
        print("Minor")

except ValueError:
    print("Please enter a valid age")

print("\n")


# ----------------------- Combined Mini Project

try:

    employee = {
        "Employee name": input("Enter Name: "),
        "Salary": int(input("Enter Salary: "))
    }

    if employee["Salary"] >=20000:
        employee["result"] = "Bonus Eligible"
    else:
        employee["result"] = "No Bonus"
    
    print(employee)

except ValueError:
    print("Please enter a valid salary")

print("\n")



# ------------------------------------------------------- Employee Report Automation

try:

    employee = {
         "Employee name": input("Enter Name: "),
        "Salary": int(input("Enter Salary: ")),
        "City": input("Enter City: ")
    }

    if employee["Salary"] >= 20000:
        employee["result"] = "Bonus Eligible"
    else:
        employee["result"] = "No Bonus"

    print(employee)

    file = open("employee_report.txt", "w")
    file.write("Employee Name: ")
    file.write(employee["Employee name"])
    file.write("\n")
    file.write("Salary: ")
    file.write(str(employee["Salary"]))
    file.write("\n")
    file.write("City: ")
    file.write(employee["City"])
    file.write("\n")
    file.write("Result: ")
    file.write(employee["result"])
    file.write("\n")
    file.close()

except ValueError:
    print("please Enter valid Salary")

print("\n")



# ----------------------------------------------------------------------------------------------------  Specific Error Handling ---------------------------------------

# ----------------------- Example


try: 

    age = int(input("Enter Age: "))
    
    file = open("report.txt", "r")

except ValueError:
    print("Invalid Age")

except FileNotFoundError:
    print("File Not Found")

print("\n")


# ----------------------- final Project of the day

try:
    
    employee = {
        "Employee Name": input("Enter Name: "),
        "Salary": int(input("Enter Salary: "))

    }

    file = open("company_rules.txt","r")
    content = file.read()
    file.close()


    if employee["Salary"] >= 20000:
        employee["result"] = "Bonus Eligible"
    else:
        employee["result"] = "No Bonus"

    print(employee)

   
except ValueError:
    print("Invalid Salary")

except FileNotFoundError:
    print("File not found")

print("\n")