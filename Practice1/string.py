print("It's alright")
print("He is called 'Johnny'")
print('He is called "Johnny"')

a = """Lorem ipsum dolor sit amet,
consectetur adipiscing elit,
sed do eiusmod tempor incididunt
ut labore et dolore magna aliqua."""
print(a)

#string is array of chars
a = "Hello, World!"
print(a[1])

#loop
for x in "banana":
  print(x)

#len
a = "Hello, World!"
print(len(a))

#check string
txt = "The best things in life are free!"
print("free" in txt)

txt = "The best things in life are free!"
if "free" in txt:
  print("Yes, 'free' is present.")

#check string if not in 
txt = "The best things in life are free!"
print("expensive" not in txt)

txt = "The best things in life are free!"
if "expensive" not in txt:
  print("No, 'expensive' is NOT present.")




#SLICING
b = "Hello, World!"
print(b[2:5])
#slice from the start
b = "Hello, World!"
print(b[:5])
#slice to the end
b = "Hello, World!"
print(b[2:])

#negative indexing
b = "Hello, World!"
print(b[-5:-2])



#Modifying
a = "Hello, World!"
print(a.upper())
a = "Hello, World!"
print(a.lower())

#Remove whitespace
#Whitespace is the space before and/or after the actual text, and very often you want to remove this space.
a = " Hello, World! "
print(a.strip()) # returns "Hello, World!"

a = "Hello, World!"
print(a.replace("H", "J"))

a = "Hello, World!"
print(a.split(",")) # returns ['Hello', ' World!']




#Concatenateion
a = "Hello"
b = "World"
c = a + b
print(c)


a = "Hello"
b = "World"
c = a + " " + b #to add space between a and b
print(c)


#Format
a = 36
txt = f"My name is John, I am {a}"
print(txt)

#Placeholders and Modifier
price = 59
txt = f"The price is {price} dollars"
print(txt)

price = 59
txt = f"The price is {price:.2f} dollars"
print(txt)

txt = f"The price is {20 * 59} dollars"
print(txt)


#Escape character
txt = "We are the so-called \"Vikings\" from the north."

txt = "Hello\nWorld!"
print(txt) 

txt = "Hello\rWorld!"
print(txt) 



#String Methods
txt = "banana"

x = txt.center(20, "O")

print(x)