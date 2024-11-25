import re

class ASTNode:
    def __init__(self, type, value=None, children=None):
        self.type = type
        self.value = value
        self.children = children or []

    def __repr__(self):
        return f"ASTNode(type='{self.type}', value={self.value}, children={self.children})"

# Tokenize the input
def tokenize(code):
    tokens = re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*|\d+|[()\[\],=]|->|[+\-*/]|fn|let|if|then|else|match|->|\.\.\.|[{}]", code)
    return tokens

# Recursive descent parser
def parse(tokens):
    def parse_program():
        nodes = []
        while index[0] < len(tokens):
            nodes.append(parse_expression())
        return nodes

    def parse_expression():
        """Parse an expression, starting with a primary expression."""
        left = parse_primary_expression()
        while index[0] < len(tokens) and tokens[index[0]] in "+-*/":
            operator = consume()  # Consume the operator
            right = parse_primary_expression()
            left = ASTNode("binary_op", operator, [left, right])  # Chain operations
        return left

    def parse_primary_expression():
        """Parse a primary expression (e.g., literal, variable, or function call)."""
        token = tokens[index[0]]
        if token == "let":
            return parse_let()
        elif token == "fn":
            return parse_function()
        elif token.isdigit():
            return ASTNode("literal", int(consume()))
        elif re.match(r"\w+", token):  # Variable or function call
            return parse_identifier_or_call()
        else:
            raise SyntaxError(f"Unexpected token: {token}")

    def parse_let():
        match("let")
        if not re.match(r"\w+", tokens[index[0]]):
            raise SyntaxError(f"Expected variable name after 'let', got '{tokens[index[0]]}'")
        name = consume()  # Consume variable name
        match("=")        # Ensure '=' follows
        expr = parse_expression()  # Parse the expression after '='
        return ASTNode("let", name, [expr])

    def parse_function():
        match("fn")
        name = consume()
        match("(")
        params = []
        while tokens[index[0]] != ")":
            params.append(consume())
            if tokens[index[0]] == ",":
                match(",")
        match(")")
        match("=")
        body = parse_expression()
        return ASTNode("function", name, [ASTNode("params", params), body])

    def parse_identifier_or_call():
        identifier = consume()
        if index[0] < len(tokens) and tokens[index[0]] == "(":
            match("(")
            args = []
            while tokens[index[0]] != ")":
                args.append(parse_expression())
                if tokens[index[0]] == ",":
                    match(",")
            match(")")
            return ASTNode("call", identifier, args)
        return ASTNode("identifier", identifier)

    def parse_binary_operation():
        left = parse_expression()
        operator = consume()
        right = parse_expression()
        return ASTNode("binary_op", operator, [left, right])

    def consume():
        token = tokens[index[0]]
        index[0] += 1
        return token

    def match(expected):
        if tokens[index[0]] != expected:
            raise SyntaxError(f"Expected '{expected}', got '{tokens[index[0]]}'")
        index[0] += 1

    index = [0]
    return parse_program()

class Interpreter:
    def __init__(self):
        self.environment = {}

    def interpret(self, nodes):
        results = []
        for node in nodes:
            result = self.interpret_node(node)
            results.append(result)
        return results

    def interpret_node(self, node):
        if node.type == "let":
            # Process 'let' statements
            name = node.value
            value = self.interpret_node(node.children[0])
            self.environment[name] = value
            return value

        elif node.type == "function":
            # Process function definitions
            name = node.value
            params = node.children[0].value  # List of parameter names
            body = node.children[1]
            self.environment[name] = (params, body)
            return f"Function {name} defined"

        elif node.type == "identifier":
            # Process variable or function calls
            if node.value in self.environment:
                return self.environment[node.value]
            else:
                raise NameError(f"Undefined identifier: {node.value}")

        elif node.type == "literal":
            # Process literals (numbers)
            return node.value

        elif node.type == "call":
            # Process function calls
            func_name = node.value
            if func_name not in self.environment or not isinstance(self.environment[func_name], tuple):
                raise NameError(f"Undefined function: {func_name}")
            params, body = self.environment[func_name]
            args = [self.interpret_node(child) for child in node.children]
            if len(params) != len(args):
                raise TypeError(f"Function {func_name} expects {len(params)} arguments, got {len(args)}")
            # Temporary scope for function execution
            old_env = self.environment.copy()
            self.environment.update(zip(params, args))
            result = self.interpret_node(body)
            self.environment = old_env  # Restore previous environment
            return result

        elif node.type == "binary_op":
            # Process binary operations
            left = self.interpret_node(node.children[0])
            right = self.interpret_node(node.children[1])
            if node.value == "+":
                return left + right
            elif node.value == "-":
                return left - right
            elif node.value == "*":
                return left * right
            elif node.value == "/":
                return left / right
            else:
                raise ValueError(f"Unknown operator: {node.value}")

        else:
            raise ValueError(f"Unknown node type: {node.type}")

# Example usage
if __name__ == "__main__":
    code = """
    let x = 10
    
    fn add(a, b) = a + b
    fn sub(a, b) = a - b
    
    add(x, 5)
    sub(x, 3)
    """
    tokens = tokenize(code)
    ast = parse(tokens)
    print("AST:", ast)

    interpreter = Interpreter()
    result = interpreter.interpret(ast)
    print(f"Result: {result}")
