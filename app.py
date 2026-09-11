"""
Simple menu-driven calculator.
Combines all the small programs from before into one that keeps running
until you choose to quit.
"""


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        return "Cannot divide by zero"
    return a / b


def power(a, b):
    return a ** b


def remainder(a, b):
    if b == 0:
        return "Cannot divide by zero"
    return a % b


def get_number(prompt):
    """Keep asking until the user types a valid number."""
    while True:
        text = input(prompt)
        try:
            return float(text)
        except ValueError:
            print("That's not a number, try again.")


def show_menu():
    print("\n===== CALCULATOR =====")
    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")
    print("5. Power")
    print("6. Remainder")
    print("7. Quit")


def main():
    operations = {
        "1": ("+", add),
        "2": ("-", subtract),
        "3": ("×", multiply),
        "4": ("÷", divide),
        "5": ("^", power),
        "6": ("%", remainder),
    }

    history = []

    while True:
        show_menu()
        choice = input("Choose an option (1-7): ").strip()

        if choice == "7":
            print("\nHistory of this session:")
            if not history:
                print("  (nothing calculated)")
            for line in history:
                print("  " + line)
            print("Goodbye!")
            break

        if choice not in operations:
            print("Invalid choice, pick a number from 1 to 7.")
            continue

        symbol, func = operations[choice]
        a = get_number("Enter first number: ")
        b = get_number("Enter second number: ")

        result = func(a, b)
        line = f"{a} {symbol} {b} = {result}"
        print(line)
        history.append(line)


if __name__ == "__main__":
    main()
