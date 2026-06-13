# ---------------- Loops ----------------


# ------------ First for Loop ---------------

for number in range (1, 6):
    print(number)


print("\n")


# ------------ Print Your Name 5 Times 

for number in range(5):
    print('Aahana')

print("\n")


# ------------- Ceramic Factory Example

for box in range (1,11):
    print("Cheaking Tile Box", box)

print("\n") 


# ------------- Multiplication Table

number = int(input("Enter a number: "))

for i in range(1, 11):
    print(number, 'x', i, '=', number * i)

print("\n")


# ------------- Countdown

for count in range(10, 0, -1):
    print(count)

print('Launch!')

print('\n')


# ------------- Frist while Loop ------------------

count = 1

while count <= 5:
    print(count)
    count+= 1

print("\n")


# -------------- Password Retry Stytem

password = ""

while password != "python123":
    password = input("Enter Password: ")

    print("Access Granted")

print("\n")


# -------------- Memory Challenge 

for number in range( 1, 8):
    print(number)


