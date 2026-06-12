
#------- Integers are whole numbers without decimal points, either positive or negative  -----------

my_int_1 = 56
my_int_2 = -4

print(type(my_int_1))
print(type(my_int_2))


#------ Here's how to perform an addition operation with integers: --------
my_int_1 = 56
my_int_2 = 12

sum_ints = my_int_1 + my_int_2
print('Interger Addition:', sum_ints)

a = 100
b = 100

sum_ints = a + b
print('Integer Addition 2:', sum_ints)

hexa = 185
beta = 21556

sum_ints = hexa + beta
print('Integer Addition 3:', sum_ints)




#--------------- Here's how to perform a subtraction with integers:---------------------


my_int_1 = 56
my_int_2 = 12

diff_ints = my_int_1 - my_int_2
print('Integer Substraction', diff_ints)


Amu = 35500
bachu = 12200

diff_ints = Amu - bachu
print('Integer Substraction', diff_ints)


credit = 1000
debit = 457

diff_ints = credit - debit
print("Integer Substraction", diff_ints)



#--------------------- Here's how to perform a multiplication operation with integers:-----------------------------


my_int_1 = 12
my_int_2 = 4


product_ints = my_int_1 * my_int_2
print('Integer Multiplication:', product_ints)


apple = 99
bananna = 96

product_ints = apple * bananna
print('Integer Multiplication:', product_ints)


a = 100
b = 10

product_ints = a * b
print(f'Integer Multiplication:', "a * b", product_ints)




#---------------------- And here's how to perform a division operation with integers: ------------------------------------

my_int_1 = 56
my_int_2 = 12

div_ints = my_int_1 / my_int_1
print('Division:', div_ints)


a = 100
b = 78
c = 52
d = 32
e = 12

div_ints = a / b / c / d / e
print('Division:', div_ints)


cherry = 1000
lichi = 561

div_ints = cherry / lichi
print('Division:', div_ints)



#-------------------- Here's an addition operation with floats: -----------------------------

my_float_1 = -12.0
my_float_2 = 4.9

float_addition = my_float_1 + my_float_2
print('Float Addition:', float_addition)


a = -1995
b = 1855

float_addition = a + b
print('float addition:', float_addition)

k = 88.66
d = -66.87

float_addition = k + d
print('Float Addition:', float_addition)



# ---------------------- Here's a subtraction operation with floats: ---------------------


a = 100
b = -75.31

float_substraction = a - b
print('Float Substraction:', float_substraction)


# ---------------------- Here's a multiplication operation with floats: -----------------

k = 35
d = 12

float_multiplication = k * d
print('Float Multiplication:', float_multiplication)



# --------------------- And here's a division operation with floats:------------------

bread = 100
butter = 23

float_division = bread / butter
print('Float division:', float_division)


#--------------- If you add an integer and a float, the result is automatically converted to a float: ------------

my_int = 15
my_float = 12

sum_int_and_float = my_int + my_float

print(sum_int_and_float)
print(type(sum_int_and_float))



# ------------------------- The modulo operator (%) returns the remainder when the value on the left is divided by the value on the right:------------------------

a = 56
b = 12

c = 5.4
d = 12.0

mod_ints = a % b 
mod_floats = d % c

print('Integer Modulo:', mod_ints)
print('Float Modulo:', mod_floats)



#-------------------- Floor division divides two numbers and returns the greatest integer less than or equal to the result.
#  This is done with the double forward slash operator (//):---------------


my_int_1 = 56
my_int_2 = 12

my_float_1 = 5.4
my_float_2 = 12.0

floor_div_ints = my_int_1 // my_int_2
floor_div_floats = my_float_2 // my_float_1

print('Integer floor division:', floor_div_ints)
print('float floor division:', floor_div_floats)


#----------- Exponentiation raises a number to the power of another, and is done with the double asterisk operator (**): -----------------



my_int_1 = 56
my_int_2 = 12

my_float_1 = 5.4
my_float_2 = 12.0

exp_ints = my_int_1 ** my_int_2
exp_floats = my_float_1 ** my_float_2

print('Integer Exponentiation:', exp_ints)
print('Float Exponentiation:', exp_floats)





# ------------------------ The float() function returns a floating-point number constructed from the given number:  -----------------

a = 56  
b = float(a)

print(b)
print(type(b))



# --------------------- The int() function returns an integer constructed from the given number: -------------------


my_float = 12.9253
my_int = int(my_float)


print(my_int)

print(type(my_int))



# ------------------------- Also, you can use the same built-in functions to convert a string into either a float or integer:------------------

my_str_int = '45'
my_str_float = '7.8'

converted_int = int(my_str_int)
converted_float = float(my_str_float)

print(converted_int, type(converted_int))
print(converted_float, type(converted_float))



# ------------------------- round(): Rounds a number to the specified number of decimal places.
#  By default this function rounds to the nearest integer, and returns a whole number with no decimal places: ----------------


my_int_1 = 4.798
my_int_2 = 4.253

rounded_int_1 = round(my_int_1)
rounded_int_2 = round(my_int_2,1)

print(rounded_int_1)
print(rounded_int_2)


#--------------------------------------- abs(): returns the absolute value of a number,-----------------------

num = -15

absolute_value = abs(num)
print(absolute_value)
 


float = 156.253

absolute_value = abs(float)
print(absolute_value)



#----------------- pow(): raises a number to the power of another or performs modular exponentiation. -------------------------------------

result_1 = pow(2,3)
print(result_1)

result_2 = pow(2, 3, 5)
print(result_2)



# -----------------   (+=) here's an example of using augmented assignment to add 5 to an existing variable:---------

my_var = 10
my_var += 5

print(my_var)


# ----------- And here is the same thing, but without augmented assignment:-----------------


my_var = 10
my_var = my_var + 5
print(my_var)



# --------------- The subtraction assignment operator (-=) subtracts the right operand from the left variable and stores the difference in the left variable: ---------

count = 14
count -= 3

print(count)


# ----------------------  The multiplication assignment operator (*=) 

product = 65
product *= 7

print(product)


# ----------------------  The division assignment operator (/=) 

price = 100
price /= 4

print(price)


# ----------------------- The floor division operator (//=) 

total_pages = 23
total_pages //= 5

print(total_pages)


# ----------------------- The modulo assignment operator (%=) 

bits = 35
bits %= 2

print(bits)


# ----------------------- The exponentiation assignment operator (**=)

power = 2
power **= 3

print(power)



#  ------------------------ the addition assignment operator makes it easy to concatenate strings:

greet = 'hello'
greet += ' world'

print(greet)




# ------------------------- And the multiplication assignment operator can be used to repeat a string:

greet = 'hello'
greet *= 3

print(greet) 



#  ------------------------ Other augmented assignments throw a TypeError when you use them with strings: 


greet = 'hello'
greet -= 'world'

print(greet)

# -------------------------- Bill Spliter -------------------------

running_total = 0

num_of_friends = 4

appetizers = 37.89
main_courses = 57.34
desserts = 39.39
drinks = 64.21

running_total += appetizers + main_courses + desserts + drinks
print('Total bill so far:', running_total)

tip = running_total * 0.25
print('Tip amount:', tip)

running_total += tip
print('Total with tip:', running_total)

final_bill = running_total / num_of_friends
print('Bill per person:', final_bill)

each_pays = round(final_bill,2)
print('Each person pays:', each_pays)