import re

class CustomEvaluator:
    def __init__(self):
        # Initializing with default precedence, associativity, and new operators
        self.precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3, '>': 0, '<': 0, '>=': 0, '<=': 0}
        self.associativity = {'+': 'L', '-': 'L', '*': 'L', '/': 'L', '^': 'R', '>': 'L', '<': 'L', '>=': 'L', '<=': 'L'}
        self.global_associativity = None

    def set_associativity(self, operator, assoc):
        if operator in self.associativity:
            self.associativity[operator] = assoc
        else:
            raise ValueError(f"Unknown operator: {operator}")

    def set_precedence(self, operator, prec):
        if operator in self.precedence:
            self.precedence[operator] = prec
        else:
            raise ValueError(f"Unknown operator: {operator}")

    def set_global_associativity(self, assoc):
        if assoc in ['L', 'R']:
            self.global_associativity = assoc
        else:
            raise ValueError("Associativity must be either 'L' (Left) or 'R' (Right)")

    def evaluate(self, expression):
        def apply_operator(operators, values):
            operator = operators.pop()
            right = values.pop()
            left = values.pop()
            if operator == '+':
                values.append(left + right)
            elif operator == '-':
                values.append(left - right)
            elif operator == '*':
                values.append(left * right)
            elif operator == '/':
                values.append(left / right)
            elif operator == '^':
                values.append(left ** right)
            elif operator == '>':
                values.append(left > right)
            elif operator == '<':
                values.append(left < right)
            elif operator == '>=':
                values.append(left >= right)
            elif operator == '<=':
                values.append(left <= right)

        def greater_precedence(op1, op2):
            if self.global_associativity:
                return self.precedence[op1] > self.precedence[op2] or \
                       (self.precedence[op1] == self.precedence[op2] and self.global_associativity == 'L')
            else:
                return self.precedence[op1] > self.precedence[op2] or \
                       (self.precedence[op1] == self.precedence[op2] and self.associativity[op1] == 'L')

        # Improved tokenizer to handle expressions with relational operators
        tokens = re.findall(r'\d+|[+/*^()-]|>=|<=|>|<', expression)
        values = []
        operators = []

        for token in tokens:
            if token.isdigit():
                values.append(int(token))
            elif token == '(':
                operators.append(token)
            elif token == ')':
                while operators and operators[-1] != '(':
                    apply_operator(operators, values)
                operators.pop()  # Remove '('
            else:
                while operators and operators[-1] != '(' and greater_precedence(operators[-1], token):
                    apply_operator(operators, values)
                operators.append(token)

        while operators:
            apply_operator(operators, values)

        return values[0]

# Main function to interact with the user
def main():
    evaluator = CustomEvaluator()
    print("Custom Expression Evaluator")
    print("Enter your expression (e.g., 2 ^ 3 ^ 2):")
    expression = input()

    while True:
        print("\nChoose an option:")
        print("1. Set operator associativity")
        print("2. Set operator precedence")
        print("3. Evaluate expression")
        print("4. Set associativity for the entire expression")
        print("5. Exit")
        choice = input()

        if choice == '1':
            print("Enter operator and associativity (e.g., ^ L):")
            op, assoc = input().split()
            evaluator.set_associativity(op, assoc)
        elif choice == '2':
            print("Enter operator and precedence (e.g., ^ 4):")
            op, prec = input().split()
            evaluator.set_precedence(op, int(prec))
        elif choice == '3':
            print("Evaluating:", expression)
            result = evaluator.evaluate(expression)
            print("Result:", result)
        elif choice == '4':
            print("Enter global associativity (L for Left, R for Right):")
            global_assoc = input().strip()
            evaluator.set_global_associativity(global_assoc)
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
