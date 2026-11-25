# Notation Converter Tool
# Compiler Design Lab Project
# Syntax-Directed Translation using Synthesized Attributes

class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

        # Synthesized Attributes
        if left is None and right is None:
            self.infix = str(value)
            self.prefix = str(value)
            self.postfix = str(value)
            self.result = int(value)
        else:
            self.infix = f"({left.infix} {value} {right.infix})"
            self.prefix = f"{value} {left.prefix} {right.prefix}"
            self.postfix = f"{left.postfix} {right.postfix} {value}"

            if value == '+':
                self.result = left.result + right.result
            elif value == '-':
                self.result = left.result - right.result
            elif value == '*':
                self.result = left.result * right.result
            elif value == '/':
                if right.result == 0:
                    raise ZeroDivisionError("Division by zero!")
                self.result = left.result / right.result


class Parser:
    def __init__(self, expression):
        self.tokens = []
        i = 0

        # Lexical Analysis
        while i < len(expression):
            if expression[i].isspace():
                i += 1
            elif expression[i].isdigit():
                number = ''
                while i < len(expression) and expression[i].isdigit():
                    number += expression[i]
                    i += 1
                self.tokens.append(number)
            elif expression[i] in '+-*/()':
                self.tokens.append(expression[i])
                i += 1
            else:
                raise ValueError(
                    f"Invalid character: {expression[i]}"
                )

        self.tokens.append('EOF')
        self.pos = 0

    def current(self):
        return self.tokens[self.pos]

    def eat(self, expected):
        if self.current() == expected:
            self.pos += 1
        else:
            raise ValueError(
                f"Expected '{expected}', found '{self.current()}'"
            )

    # E -> T {(+ | -) T}
    def expression(self):
        node = self.term()

        while self.current() in ('+', '-'):
            op = self.current()
            self.eat(op)
            right = self.term()
            node = Node(op, node, right)

        return node

    # T -> F {(* | /) F}
    def term(self):
        node = self.factor()

        while self.current() in ('*', '/'):
            op = self.current()
            self.eat(op)
            right = self.factor()
            node = Node(op, node, right)

        return node

    # F -> integer | ( E )
    def factor(self):
        token = self.current()

        if token.isdigit():
            self.eat(token)
            return Node(token)

        elif token == '(':
            self.eat('(')
            node = self.expression()
            self.eat(')')
            return node

        else:
            raise ValueError(
                f"Invalid expression near '{token}'"
            )

    def parse(self):
        root = self.expression()

        if self.current() != 'EOF':
            raise ValueError(
                f"Unexpected token: {self.current()}"
            )

        return root


# Display Expression Tree
def print_tree(node, level=0, prefix="Root: "):
    if node is not None:
        print("    " * level + prefix + str(node.value))
        print_tree(node.left, level + 1, "Left: ")
        print_tree(node.right, level + 1, "Right: ")


# Main Program
print("=" * 40)
print("       NOTATION CONVERTER TOOL")
print("=" * 40)

expression = input("Enter arithmetic expression: ")

try:
    parser = Parser(expression)
    root = parser.parse()

    print("\n---------- OUTPUT ----------")
    print("Infix:   ", expression)
    print("Prefix:  ", root.prefix)
    print("Postfix: ", root.postfix)
    print("Value:   ", root.result)

    print("\n------- EXPRESSION TREE -------")
    print_tree(root)

except (ValueError, ZeroDivisionError) as error:
    print("\nError:", error)
