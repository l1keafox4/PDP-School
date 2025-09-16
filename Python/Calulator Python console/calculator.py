import math

def add(a, b): return a + b
def subtract(a, b): return a - b
def multiply(a, b): return a * b
def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero!")
    return a / b
def power(a, b): return a ** b

def sqrt(a): return math.sqrt(a)
def log(a, base=10): return math.log(a, base)
def sin(a): return math.sin(math.radians(a))
def cos(a): return math.cos(math.radians(a))
def tan(a): return math.tan(math.radians(a))

def calculate(expr):
    allowed_names = {"__builtins__": None, "add": add, "sub": subtract, "mul": multiply, "div": divide, "pow": power,
                     "sqrt": sqrt, "log": log, "sin": sin, "cos": cos, "tan": tan, "math": math}
    try:
        return eval(expr, {"__builtins__": None}, allowed_names)
    except Exception as e:
        return f"Error: {e}"

def main():
    print("Welcome to the Professional Python Calculator!")
    print("Type 'q' to quit.")
    print("Available operations: add, sub, mul, div, pow, sqrt, log, sin, cos, tan")
    print("Usage Instructions:")
    print("- Use add(a, b) for addition")
    print("- Use sub(a, b) for subtraction")
    print("- Use mul(a, b) for multiplication")
    print("- Use div(a, b) for division")
    print("- Use pow(a, b) for power")
    print("- Use sqrt(a) for square root")
    print("- Use log(a, base) for logarithm")
    print("- Use sin(a) for sine")
    print("- Use cos(a) for cosine")
    print("- Use tan(a) for tangent")
    print("Python Calculator ")
    while True:
        expr = input("Enter expression (or 'q' to quit): ")
        if expr.lower() == 'q':
            break
        try:
            result = calculate(expr)
            print("Result:", result)
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    main()
