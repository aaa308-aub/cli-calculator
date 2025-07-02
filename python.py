class Calculator:
    def add(self, x, y): return x + y
    def subtract(self, x, y): return x - y
    def multiply(self, x, y): return x * y
    def divide(self, x, y): return round(x / y, 5)

def main():
    calc = Calculator()
    while True:
        x = input("Please enter the first integer, or type 'q' to quit: ")
        if x == 'q': break
        try: x = int(x)
        except ValueError:
            print("Please enter integers only.")
            continue

        y = input("Please enter the second integer, or type 'q' to quit: ")
        if y == 'q': break
        try: y = int(y)
        except ValueError:
            print("Please enter integers only.")
            continue
        
        op = input("Please enter the operation (+, -, *, /), or type 'q' to quit: ")
        match op:
            case '+': print(f'{x} + {y} = {calc.add(x,y)}')
            case '-': print(f'{x} - {y} = {calc.subtract(x,y)}')
            case '*': print(f'{x} * {y} = {calc.multiply(x,y)}')
            case '/':
                if y == 0: print(f'Sorry, we can\'t divide by 0!')
                else: print(f'{x} / {y} = {calc.divide(x,y)}')
            case 'q': break
            case _: print("Please enter valid operations only (+, -, *, /)")

if __name__ == "__main__":
    main()

#this comment is for testing commits and tags on gitHub.