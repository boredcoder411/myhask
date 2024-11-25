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
    def parse_expression():
        if tokens[index[0]] == "let":
            return parse_let()
        elif tokens[index[0]] == "fn":
            return parse_function()
        elif re.match(r"\w+", tokens[index[0]]):  # Variable or function call
            return ASTNode("identifier", tokens[index[0]])
        elif tokens[index[0]].isdigit():
            return ASTNode("literal", int(tokens[index[0]]))
        raise SyntaxError(f"Unexpected token: {tokens[index[0]]}")

    def parse_let():
        match("let")
        name = consume()
        match("=")
        expr = parse_expression()
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

    def consume():
        token = tokens[index[0]]
        index[0] += 1
        return token

    def match(expected):
        if tokens[index[0]] != expected:
            raise SyntaxError(f"Expected '{expected}', got '{tokens[index[0]]}'")
        index[0] += 1

    index = [0]
    return parse_expression()

# Test the parser
code = """
fn add(x, y) = x + y
let result = add(5, 7)
"""
tokens = tokenize(code)
print("Tokens:", tokens)
ast = parse(tokens)
print("AST:", ast)

