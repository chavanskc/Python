from math_lib import add, subtract, multiply, divide, evaluate_expression

MENU = """
1) Add
2) Subtract
3) Multiply
4) Divide
5) Evaluate Expression (e.g. 5+3*(2-1))
6) Quit
"""


def read_number(prompt: str) -> float:
    return float(input(prompt))


def main():
    while True:
        print(MENU)
        choice = input("Choose an option (1-6): ").strip()

        if choice == "6":
            print("Goodbye!")
            break

        if choice not in ("1", "2", "3", "4", "5"):
            print("Invalid option. Please choose 1-6.")
            continue

        try:
            if choice == "5":
                expression = input("Enter expression: ")
                result = evaluate_expression(expression)
            else:
                num1 = read_number("Enter the first number: ")
                num2 = read_number("Enter the second number: ")

                if choice == "1":
                    result = add(num1, num2)
                elif choice == "2":
                    result = subtract(num1, num2)
                elif choice == "3":
                    result = multiply(num1, num2)
                else:
                    result = divide(num1, num2)

            print(f"Result: {result}")
        except ValueError as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
