from decimal import Decimal, ROUND_HALF_UP
class Calculator:
    def calculate(self, expression): #caller function.
        tokens, stackSubExpressions = self.tokenize(expression)

        for arr in reversed(stackSubExpressions):
            for subExpression in arr:   #parse from deepest sub-expression to shallowest.
                self.parse(tokens, subExpression)

        for token in tokens:
            if token is None: continue
            integerPart = token.to_integral()
            token -= integerPart
            #for input validation in the .quantize() method, remove the whole part of
            #the last token/value if it is very large. must also format its decimal string
            #to be greater in length of digits than the .quantize() format (15 digits of precision).
            formatted = Decimal(f'{token:.30f}')
            decimalPart = formatted.quantize(Decimal('1e-15'), rounding=ROUND_HALF_UP).normalize()
            rounded = integerPart + decimalPart
            result = int(rounded) if rounded == rounded.to_integral() else float(rounded)
            return result

    def parse(self, tokens, subExpression):  #parse sub-expression (or entire expression).

        def parse_terms(index, operation):  #helper function to evaluate terms (+, -, *, /).
            nonlocal start
            left, right = index-1, index+1
            while tokens[left] is None: left -= 1
            while tokens[right] is None: right += 1
            x = Decimal(tokens[left]) if type(tokens[left]) == str else tokens[left]
            y = Decimal(tokens[right]) if type(tokens[right]) == str else tokens[right]
            # x and y must be Decimal objects to solve floating point imprecision.
            if operation == '*':
                term = x*y
            elif operation == '+':
                term = x+y
            elif operation == '-':
                term = x-y
            elif operation == '/':
                term = x/y
            tokens[index] = term
            tokens[left] = tokens[right] = None

        start, end = subExpression

        if subExpression != (0, len(tokens)-1):
            tokens[start-1] = tokens[end+1] = None  #remove the parentheses using placeholder None.

        if tokens[start] == '+': #handle leading + or - explicitly at the start.
            tokens[start] = None
            start += 1
        elif tokens[start] == '-':
            tokens[start] = None
            while tokens[start] is None: start += 1
            tokens[start] = -Decimal(tokens[start]) if type(tokens[start]) == str else -tokens[start]
            start += 1

        for index in range(start, end+1): #first pass: evaluate the terms (*, /), left to right.
            if type(tokens[index]) == str and tokens[index] not in ['+','-','*','/']:
            #must be done early to handle edge-case of input expression being just one integer.
                tokens[index] = Decimal(tokens[index])
            if tokens[index] in ['*','/']:
                parse_terms(index, tokens[index])

        for index in range(start, end+1): #second pass: evaluate the terms (+, -), left to right.
            if tokens[index] in ['+','-']:
                parse_terms(index, tokens[index])

    def tokenize(self, expression):  #get array of tokens and sub-expressions' start and end indices.
        tokens = []
        stackOpenParentheses = []
        currentDepth = 0
        stackSubExpressions = [[]]

        for index, char in enumerate(expression): #tokenize each character if valid; raise error if not.
            match char:
                case '(':
                    if tokens != [] and (tokens[-1].isdigit() or tokens[-1] == ')'):
                        tokens.append('*')
                    tokens.append('(')
                    currentDepth += 1
                    stackOpenParentheses.append((len(tokens), currentDepth))

                case ')':
                    if stackOpenParentheses == []:
                        raise SyntaxError(f"Unmatched Parentheses -- raised at index {index}")
                    if tokens[-1] == '(':
                        raise SyntaxError(f"Empty Parentheses -- raised at index {index}")
                    if tokens[-1] in ['+','-','*','/']:
                        raise SyntaxError(f"Trailing Operator Found -- raised at index {index}")
                    end = len(tokens)-1
                    tokens.append(')')
                    start, depth = stackOpenParentheses.pop()
                    while len(stackSubExpressions) < depth+1:
                        stackSubExpressions.append([])
                    stackSubExpressions[depth].append((start, end))
                    currentDepth -= 1

                case '0'|'1'|'2'|'3'|'4'|'5'|'6'|'7'|'8'|'9':
                    if tokens == []:
                        tokens.append(char)
                    elif char == '0' and tokens[-1] == '/':
                        raise ZeroDivisionError()
                    elif tokens[-1].isdigit():
                        tokens[-1] += char
                    elif tokens[-1] == ')':
                        tokens.append('*')
                        tokens.append(char)
                    else:
                        tokens.append(char)

                case '+'|'-':
                    if tokens != [] and tokens[-1] in ['+','-','*','/']:
                        raise SyntaxError(f"Adjacent Operators Found -- raised at index {index}")
                    if index == len(expression)-1:
                        raise SyntaxError(f"Trailing Operator Found -- raised at index {index}")
                    tokens.append(char)

                case '*'|'/': # * and / cannot be leading, while + and - can
                    if tokens == [] or tokens[-1] == '(':
                        raise SyntaxError(f"Leading '*' or '-' Found -- raised at index {index}")
                    if tokens[-1] in ['+','-','*','/']:
                        raise SyntaxError(f"Adjacent Operators Found -- raised at index {index}")
                    if index == len(expression)-1:
                        raise SyntaxError(f"Trailing Operator Found -- raised at index {index}")
                    tokens.append(char)

                case ' ': pass
                case _: raise SyntaxError(f"Invalid Character Found -- raised at index {index}")

        if tokens == []:
            raise SyntaxError("Empty Expression")
        if stackOpenParentheses != []:
            raise SyntaxError("Unmatched Parentheses -- raised at end of expression")
        stackSubExpressions[0].append((0, len(tokens)-1))
        return (tokens, stackSubExpressions)

def main():
    calc = Calculator()
    print("Please enter your math expression. Currently,\nonly integers, parentheses, and basic operators (+,-,*,/)\nare allowed. If you wish to quit the calculator, type 'q'")
    while True:
        expression = input("> ")
        if expression == 'q': break
        try:
            result = calc.calculate(expression)
            print(result, end='\n\n')
        except SyntaxError as s:
            print(f"SYNTAX-ERROR: {s}", end='\n\n')
        except ZeroDivisionError:
            print("ZERO DIVISION ERROR: Cannot divide by zero!", end='\n\n')

if __name__ == "__main__":
    main()