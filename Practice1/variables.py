#Creating Variables
x = 5
y = "John"
print(x)
print(y)

#Casting
x = str(3)    # x will be '3'
y = int(3)    # y will be 3
z = float(3)  # z will be 3.0

#Get the Type
x = 5
y = "John"
print(type(x))
print(type(y))

#Case-Sensitive
a = 4
A = "Sally"
#A will not overwrite a



#MULTIPLE VALUES
#Many Values to Multiple Variables
x, y, z = "Orange", "Banana", "Cherry"
print(x)
print(y)
print(z)

#One value to multiple varibles
x = y = z = "Orange"
print(x)
print(y)
print(z)

#Unpack a collection
fruits = ["apple", "banana", "cherry"]
x, y, z = fruits
print(x)
print(y)
print(z)



#OUTPUT VARIABLES
x = "Python"
y = "is"
z = "awesome"
print(x, y, z)

x = "Python "
y = "is "
z = "awesome"
print(x + y + z)

x = 5
y = 10
print(x + y)

x = 5
y = "John"
print(x, y)



#GLOBAL VARIABLES
x = "awesome"

def myfunc():
  print("Python is " + x)

myfunc()

#If you create a variable with the same name inside a function, this variable will be local, and can only be used inside the function. The global variable with the same name will remain as it was, global and with the original value.
x = "awesome"

def myfunc():
  x = "fantastic"
  print("Python is " + x)

myfunc()

print("Python is " + x)

#The global Keyword
def myfunc():
  global x
  x = "fantastic"

myfunc()

print("Python is " + x)