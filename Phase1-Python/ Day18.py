# ---------------------------------------------------------------------------------------------------- Modules & Import ------------------------------------------------

# -------------------------------------------- Create a folder

import os

os.mkdir("Files")

print("\n")


# -------------------------------------------- Create a folder but only if it doesn't already exist

import os

if not os.path.exists("Employees"):
    os.mkdir("Employee")

print("\n")

# -------------------------------------------- Create a folder but only if already exist print exists other create folder and print Folder Created

import os

if os.path.exists("Reports"):
    print("Folder Already Exists")

else:
    
    os.mkdir("Reports")
    print("Folder Created")

    print("\n")


# -------------------------------------------- Modules + File Handling + IF/ELSE

import os

if os.path.exists("report.txt"):
    
    file = open("report.txt", "r")
    
    content = file.read()
    
    print(content)
   
    file.close()

else:

    print("File Not Found")

print("\n")



# -------------------------------------------- Random Module Program

import random

print(random.randint(1,10))

print("\n")


# -------------------------------------------- Random + If\else

import random

number = random.randint(1,5)

print(number)

if number == 5:
    
    print("Jackpot")

else:
    print("Try Again")

print("\n")


# -------------------------------------------- Random + While + Break

import random

while True:
 

    number = random.randint(1, 5)

    print(number)

    if number == 5:
        print("Jackpot")
        break
    

print("\n")


# -------------------------------------------- Random + Functions

import random

def lottery():
    
   number = random.randint(1,5)

   print(number)

    if number == 5:
        print("Jackpot")
        return 1 
    else:
        print("Try Again")
        return 0 
        
result = lottery()

print(lottery())

print("\n")

# -------------------------------------------- Lottery Counter Program 

import random

def lottery():

    number = random.randint(1,5)

    print("Number: ", number)

    if number == 5:
        print("Jackpot")
        return 1 
    else:
        print("Try Again")
        return 0


count = 0

while True:
    
    result = lottery()

    if result == 1 :
        count += 1 

    if count == 3:
        print(count, "Jackpots Found")
        break

print("\n")


