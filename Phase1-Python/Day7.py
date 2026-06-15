# ------------------  For Loop - If/Else  ------------------------------------------

# --------------- Exercise - 1

for number in range(1, 11):
    print(number)

print('\n')
# --------------- Exercise - 2

for name in range(5):
    print("Hello")


print('\n')
# --------------- Exercise - 3

for employee in range(1, 6):
   print('Employee', employee)


print('\n')
# --------------- Exercise - 4

cities = ["Morbi", "Rajkot", "Ahmedabad"]

for city in cities:
   print(city)


print('\n')
# --------------- Mini Challenge 

for box in range(1,21):
   print('Pcking box',box)
    

print('\n')
# --------------  Print only Even Numbers

for number in range(1, 11):
   if number % 2 == 0:
       print(number)


print('\n')
# -------------  Pass or Fail List

marks = [25, 40, 30, 80, 50]

for mark in marks:
   if mark >= 35:
       print(mark, "Pass")
   else:
       print(mark, "Fail")


print('\n')
# -------------  Employee Age Check

ages = [17, 20, 16, 25, 18]

for age in ages:
   if age >= 18:
       print(age,"Adult")
   else:
       print(age, "Minor")


print('\n')
# -------------  Ceramic Box Inspection

for box in range(1,11):
   if box == 5:
       print("Broken box")
   else:
       print("Box", box, "OK")


print('\n')
# ------------  Password Attempts

passwords = ["hello", "123", "python123"]

for password in passwords:
   if password == "python123":
       print("Access Granted")
   else:
       print("Wrong Password")


print('\n')
# ------------  Challenge 1

for number in range(1, 21):
   if number % 2 == 0:
       print("Even", number)
   else:
       print("Odd", number)



print('\n')
# ------------  Challange 2

employees = ["Ravi", "Amit", "Neha", "Priya"]

for employee in employees:
   print ("Employee:", employee)



print('\n')
# ------------  Challenge 3

salaries = [12000, 18000, 25000, 10000]

for salary in salaries:
   if salary >= 15000:
       print(salary,"Eligible")
   else:
       print(salary, "Not Eligible")
        


print('\n')
# ------------  Memory Challenge

for number in range(1, 11):
    if number >5:
        print(number, "High")
    else:
        print(number,"Low")


print("\n")





# -------------------------- while Loop -------------------------------------------------------------------------------------------------------



# ------------- Exercise - 1 Print 1 to 5 using while

count = 1

while count <= 5:
   print(count)
   count += 1


print("\n")
# ------------- Excercise - 2 Print your name 5 times

count = 1

while count <= 5:
    print("Aahana")
    count += 1


print("\n")
# ------------- Exercise - 3 Countdown

count = 10

while count >= 1:
    print(count)
    count -= 1

print("GO!")


print("\n")
# ------------- Exercise - 4 Keep asking age until is 18 or more

age = 0

while age < 18:
    age = int(input("Enter Age: "))

print("Allowed")


print("\n")
# ------------ Exercise - 5 Automation Style

boxes = 1

while boxes <= 10:
    print("Checking Box", boxes)
    boxes += 1


print("\n")



# --------------------------------  While Loop Mastery ------------------------------------



# --------------------------------------------- Exercise - 1 print 1 ro 10

count = 1

while count <= 10:
    print(count)
    count += 1




print('\n')
# --------------------------------------------- Exercise - 2 Print your name 10 times



count = 1

while count <= 10:
    print("Aahana")
    count += 1    


print('\n')
# --------------------------------------------- Exercise - 3 Print 10 to 1 GO!

count = 10

while count >= 1:
    print(count)
    count -= 1
print("GO!")


print('\n')
# --------------------------------------------- Exercise - 4 Print only even number form 2 to  20

count = 1

while count < 21:
    if count % 2 == 0:
        print(count) 
    count += 1



print('\n')
# --------------------------------------------- Exercise - 5 Print only Odd numbers from 1 to 19

count = 1

while count <= 20:
    if count % 2 != 0:
        print(count)
    count += 1


    print("\n")




# --------------------------------------------- while + if/else ---------------------


# --------------------------------  Exercise - 6 print 1 to 20 with even and odd

count = 1

while count <= 20:
   if count % 2 == 0:
       print(count, "Even")
   else:
       print(count,"Odd")
   count += 1


print('\n')
# --------------------------------  Exercise - 7 ask age repeatedly

age = 0

while age < 18:
   age = int(input("Enter Age: "))

print("Allowed")


print('\n')
# --------------------------------  Exercise - 8 Password system

# ---------------- int pass

password = ""

while password != 1545:
   password = int(input("Enter Password: "))

print("Access Granted")


print('\n')
# ----------------- str pass

password = ""

while password !='python123':
   password = input("Enter Password: ")

print("Access Granted")
                   


print('\n')
# --------------------------------  Exercise - 9 Keep asking Marks

marks = 0

while marks != -1:
    marks = int(input("Enter marks: "))
    if marks > 35:
       print("Pass")
    else:
        print("Fail")



print('\n')
# --------------------------------  Exercise - 10 Damaged Box number

boxes = 1

while boxes < 20:
   print("Checking Box", boxes)
   if boxes == 13:
       print("Damaged Box Found")
   boxes += 1



print('\n')
# ----------------------------------------  Project - 1 - Employee Entery System 
  

employee_name = ""

while employee_name != 'Aahana':
    employee_name = input("Employee Name: ")

print("STOP")


print('\n')
# ----------------------------------------  Project - 2 - Salary Eligiblity Checker 

salary = ""

while salary !=0:
        salary = int(input("Enter Salary: "))
        if salary > 50000:
            print("Eligible")
        else:
            print("Not Eligible")



print('\n')
# ----------------------------------------  Project - 3 - Tile Box Inspection

boxes = 1

while boxes < 16:
    boxes = int(input("how many boxes? "))
    print("Inspecting box", boxes)
    if boxes == 16:
       print("Damaged Box Found")
    boxes += 1

print("Inspection complete")


print('\n')
# ----------------------------------------  Project - 4 - Secre Number Game

secret_number = ""

while secret_number != 1:
    secret_number = int(input("Enter Secret Number: "))
    if secret_number == 1:
        print("Correct")
    else:
        print("try Again!")


print('\n')
# ----------------------------------------  Project - 5 - Login System

username = ""
password = ""

while username != 'admin' and password != 'python123':
    username = input("Enter Username: ")
    password = input("Enter Password: ")
    if username == 'admin':
        if password == 'python123':
            print("login Successful")
    else:
            print("Error! Username or Password Might be wrong Try")