a = float(input("Enter first number: "))
b = float(input("Enter second number: "))

average = (a + b) / 2
print(f"Average of {a} and {b} = {average}")

if a > b:
    print(f"{a} is the larger number")
elif b > a:
    print(f"{b} is the larger number")
else:
    print("Both numbers are equal")
