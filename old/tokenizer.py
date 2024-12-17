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
    tokens = re.findall(
        r'"[^"]*"|'                # Match strings in double quotes
        r"[a-zA-Z_][a-zA-Z0-9_]*|" # Match identifiers
        r"\d+|"                    # Match numbers
        r"[(){}\[\],=:]|"          # Match parentheses, braces, brackets, commas, colons, equals
        r"->|"                     # Match arrow operator
        r"match|_|"                # Add match and wildcard keywords
        r"[+\-*/<>!]=?|=="         # Match comparison operators (>, <, >=, <=, ==, !=)
        r""
    , code)
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
        # Handle comparison operators like >, <, >=, <=, ==, !=
        while index[0] < len(tokens) and tokens[index[0]] in [">", "<", ">=", "<=", "==", "!="]:
            operator = consume()  # Consume the operator
            right = parse_primary_expression()
            left = ASTNode("comparison_op", operator, [left, right])  # Chain comparisons
        # Handle arithmetic operators
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
        elif token == "if":
            return parse_if()
        elif token == "match":
            return parse_match()
        elif token.isdigit():  # Numeric literal
            return ASTNode("literal", int(consume()))
        elif token.startswith('"') and token.endswith('"'):  # String literal
            return ASTNode("string", consume()[1:-1])  # Remove quotes
        elif re.match(r"\w+", token):  # Variable or function call
            return parse_identifier_or_call()
        else:
            raise SyntaxError(f"Unexpected token: {token}")

    def parse_function():
        """Parse a function definition with static typing."""
        match("fn")                      # Consume 'fn'
        name = consume()                 # Consume function name
        match("(")                       # Match '('
        
        params = []
        while tokens[index[0]] != ")":   # Parse typed parameters
            param_name = consume()       # Parameter name
            match(":")                   # Match ':'
            param_type = consume()       # Parameter type
            params.append(ASTNode("param", param_name, [ASTNode("type", param_type)]))
            
            if tokens[index[0]] == ",":
                match(",")
        match(")")                       # Match ')'
        
        # Parse return type
        match("->")
        return_type = consume()          # Return type annotation
        
        match("=")                       # Match '='
        body = parse_expression()        # Parse function body
        
        return ASTNode("function", name, [
            ASTNode("params", None, params),
            ASTNode("return_type", return_type),
            body
        ])
    
    
    def parse_let():
        """Parse a variable declaration with static typing."""
        match("let")                     # Consume 'let'
        
        if not re.match(r"\w+", tokens[index[0]]):
            raise SyntaxError(f"Expected variable name after 'let', got '{tokens[index[0]]}'")
        name = consume()                 # Consume variable name
        
        match(":")                       # Match ':'
        var_type = consume()             # Type annotation
        
        match("=")                       # Ensure '=' follows
        expr = parse_expression()        # Parse the expression after '='
        
        return ASTNode("let", name, [
            ASTNode("type", var_type),
            expr
        ])

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
    
    def parse_if():
        match("if")
        condition = parse_expression()
        match("then")
        then_expr = parse_expression()
        match("else")
        else_expr = parse_expression()
        return ASTNode("if", None, [condition, then_expr, else_expr])

    def parse_match():
        """Parse a match expression."""
        match("match")
        # Parse the subject of the match
        subject = parse_expression()
        
        # Collect case clauses
        cases = []
        match("{")
        while tokens[index[0]] != "}":
            # Parse the pattern (can be a literal, identifier, or wildcard)
            pattern = parse_match_pattern()
            match("->")
            # Parse the expression to execute for this case
            case_expr = parse_expression()
            cases.append(ASTNode("case", None, [pattern, case_expr]))
            
            # Optional comma between cases
            if tokens[index[0]] == ",":
                match(",")
        
        match("}")
        return ASTNode("match", None, [subject] + cases)

    def parse_match_pattern():
        """Parse a pattern for match expression."""
        token = tokens[index[0]]
        
        # Literal (number or string)
        if token.isdigit():
            return ASTNode("literal", int(consume()))
        elif token.startswith('"') and token.endswith('"'):
            return ASTNode("string", consume()[1:-1])
        # Wildcard pattern
        elif token == "_":
            consume()
            return ASTNode("wildcard")
        # Identifier pattern
        elif re.match(r"\w+", token):
            return ASTNode("identifier", consume())
        else:
            raise SyntaxError(f"Unexpected pattern: {token}")

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
