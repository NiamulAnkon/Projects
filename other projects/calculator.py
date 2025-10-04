num1 = float(input("Enter first number: "))
op = input("Enter operator(+,-,*,/): ")
num2 = float(input("Enter second number: "))

def do_operation(num1, op, num2):
    if op == "+":
        print(num1 + num2)
    elif op == "-":
        print(num1 - num2)
    elif op == "*":
        print(num1 * num2)
    elif op == "/":
        print(num1 / num2)
    elif op == "%":
        print(num1 % num2)
    else:
        print("Invalid operator")

do_operation(num1, op, num2)