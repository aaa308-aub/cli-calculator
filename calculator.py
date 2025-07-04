class Calculator:
    def calculate(self, expression):  #calculate user-input expression
        tokens, stackSubExpressions = self.tokenize(expression)
        #tokenize the input and get each sub-expression start and end indices (parentheses excluded)
        #the whole expression is also in stackSubExpressions (start = 0, end = len(tokens)-1)

        for arr in reversed(stackSubExpressions):
            for subExpression in arr:   #parse each sub-expression
                self.parse(tokens, subExpression)

        for token in tokens:  #return last remaining token
            if token is not None:
                #must handle edge-case where the input expression is 1 integer only
                return int(token) if type(token) == str else token

    def parse(self, tokens, subExpression):  #parse sub-expression (or entire expression)

        def parse_terms(index, operation):  #helper function to evaluate terms (+, -, *, /)
            left, right = index-1, index+1
            while tokens[left] is None: left -= 1
            while tokens[right] is None: right += 1
            x, y = float(tokens[left]), float(tokens[right])
            # x and y must be cast to type float not int. If x (the left value) was a
            # division term recently evaluated, it may not be a whole number.

            if operation == '*':
                term = x*y
            elif operation == '+':
                term = x+y
            elif operation == '-':
                term = x-y
            elif operation == '/':
                term = x/y
            term = round(term, 10)
            if term.is_integer():
                tokens[index] = int(term)
            else: tokens[index] = term
            tokens[left] = tokens[right] = None

        start, end = subExpression

        if subExpression != (0, len(tokens)-1):
            tokens[start-1] = tokens[end+1] = None  #remove the parentheses using placeholder None

        if tokens[start] in ['+','-']:  #handle leading + or - explicitly at the start
            tokens[start+1] = tokens[start] + tokens[start+1]
            tokens[start] = None
            start += 1

        for index in range(start, end+1): #first pass: evaluate the terms (*, /), left to right
            if tokens[index] in ['*','/']:
                parse_terms(index, tokens[index])
        
        for index in range(start, end+1): #second pass: evaluate the terms (+, -), left to right
            if tokens[index] in ['+','-']:
                parse_terms(index, tokens[index])

    def tokenize(self, expression):
        tokens = []
        stackOpenParentheses = []
        currentDepth = 0
        stackSubExpressions = [[]]

        for index, char in enumerate(expression):
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

                case '*'|'/':
                    if tokens == [] or tokens[-1] == '(':
                        raise SyntaxError(f"Leading '*' or '-' Found -- raised at index {index}")
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
    print("Please enter your math expression. Currently,\nonly integers, parentheses, and basic operators (+,-,*,/)\nare allowed. If you wish to exit the calculator, type 'Q'")
    while True:
        expression = input("> ")
        if expression == 'Q': break
        try:
            result = calc.calculate(expression)
            print(result)
            print(type(result), end='\n\n')
        except SyntaxError as s:
            print(f"SYNTAX-ERROR: {s}", end='\n\n')
        except ZeroDivisionError:
            print("ZERO DIVISION ERROR: Cannot divide by zero!", end='\n\n')
if __name__ == "__main__":
    main()