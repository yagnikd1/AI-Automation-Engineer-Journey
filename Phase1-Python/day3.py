
# ---------------------- f-strings and embed variables


name = "bob"
age = 27
height = 1.68

print(f"{name} is {age} years old and {height}m tall")


name = "Alice"
age = 45
height = 1.93
print(f'{name} is {age} years old and {height}m tall')



# ------------------------ float - Int

score = 7.69
score_int = int(score)

print(f"Float: {score}")
print(f"int: {score_int}")
print(type(score_int))

# --------------- swapping values with tuple unpacking 

x, y, z = 32, 42, 23

print(f"x={z}, y={y}, z={x}")


amu, bachu, chimpala = 155, 200, 35200

print(f"amu={bachu}, bachu={chimpala}, chimpala{bachu}")



jack, merry, johnson, king, slave = 15, 50, 75, 100, 150

print(f"merry={king}, slave={jack}, jack={johnson}, johnson={merry}, king={slave}")


# -------------------- Integers -----------------------

total = 0
total += 39
total += 15
total += 35
total += 43
total += 24

print(f"Total: {total}")

# --------------------

base = 3
exp = 2

result = base ** exp

print(f"{base} to the power of {exp} = {result}")

# ---------------------


a = 97
b = 9

quotient = a // b
remainder = a % b

print(f"Quotient: {quotient}")
print(f"Remainder: {remainder}")

# ---------------------------

n = 77
divisor = 5

remainder = n % divisor
is_divisible = (remainder == 0)

print(f"Remainder: {remainder}")
print(f"Divisible: {is_divisible}")

# ------------------

a = 52
b = 6

quotient = a // b
remainder = a % b 

print(f"Quotient: {quotient}")
print(f"Remainder: {remainder}")

# ----------------- 

total = 0
total += 48
total += 9
total += 44
total += 45
total += 10

print(f"Total: {total}")

# -------------------


base = 2
exp = 8

result = base ** exp

print(f"{base} to the power of {exp} == {result}")

# -------------------

n = 75
divisor = 3

remainder = n % divisor
is_divisible = (remainder == 0)

print(f"Remainder: {remainder}")
print(f"Divisible: {is_divisible}")



# ---------------------------- Floats -----------------

celsius = 31.4
fehrenheit = (celsius * 9/5) +32

print(f"{celsius}°C = {fehrenheit}°F")


# ----------------------------

price = 2.67
qty = 3

total = price * qty
print(f"Total: £{total:.2f}")


# ------------------------

principal = 3148
rate = 5
years = 1

interest = principal * rate/100 * years
total = principal + interest

print(f"Interest: £{interest: .2f}")
print(f"Total: £{total: .2f}")

# ------------------------

radius = 6.8
pi = 3.14159

area = pi * radius ** 2
circumference = 2 * pi * radius

print(f"Area: {area: .2F}")
print(f" Circumference: {circumference : .2F}")


# ---------------------- Operators --------------------------------

#----------------------- Order Operation ( how brackets change the result)

a = 20
b = 2
c = 4

result1 = a + b * c
result2 = (a + b) * c

print(f"Without Brackets: {result1}")
print(f"With Bracket: {result2}")

# ------------------- compound calculation

n = 5
power = 4

step1 = n ** power
step2 = step1 // n
step3 = step2 % 10

print(f"Step1: {step1}")
print(f"Step2: {step2}")
print(f"Step3: {step3}")

# ----------------- unit conversion chain


km = 38.2

miles = km * 0.621371
metres = km * 1000
cm = metres * 100

print(f"Miles: {miles:.2f}")
print(f"Metres: {metres:.2f}")
print(f"Cm: {cm:.2f}")

# ------------------------------- CONVERSION ---------------------

# -------------- Mixed-Type Calculation

salary  = 27336
tax_rate = 0.37

net_pay = salary * (1 - tax_rate)
net_pay = round(net_pay, 2)

print(f"Net Pay: £{net_pay}")


# -------------- Stringer to Integer

num_str = "247"
num_int = int(num_str)

print(type(num_int))
print(num_int + 100)


# -------------- int() truncation

score = 7.49
score_int = int(score)

print(f"Float: {score}")
print(f"Int : {score_int}")
print(type(score_int))





 # ---------------------------  All Topic ( Variables, Integers, Floats, Operators, Conveersion)  Challenges ------------------------------



# ------------------ Shopping Bill Calculator

bread = 1.32
milk = 1.2
eggs = 2.38

subtotal = bread + milk + eggs
discount = subtotal * 0.10
after_discount = subtotal - discount
vat = after_discount * 0.20
total = after_discount + vat

print(f"Subtotal: £{subtotal:.2f}")
print(f"Discount: -£{discount:.2f}")
print(f"VAT: +£{vat:.2f}")
print(f"Total: £{total:.2f}")



# ------------------ Speed, Distance & Time

speed_kmh = 82
time_hrs = 0.8

distance_km = speed_kmh * time_hrs
distance_m = int(distance_km * 1000)

print(f"Distance: {distance_km:.2f}km")
print(f"Distance: {distance_m}m")




# ----------------- Exam Results Calculator

s1 = 61
s2 = 96
s3 = 54
s4 = 86

total = s1 + s2 + s3 + s4
average = total / 4
passed = (average >= 50)

print(f"Total: {total}")
print(f"Average: {average:.2f}")
print(f"Passed: {passed}")




# --------------- Compound Intrest

p = 2425   # principal
r = 3.7    # annual rate
n = 6      # years

amount = p * ( 1 + r/100) ** n
profit = amount - p 

print(f"Final_amount: £{amount:.2f}")
print(f"profit: £{profit:.2f}")


