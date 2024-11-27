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
    
        elif node.type == "string":
            # Process string literals
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
        
        elif node.type == "if":
            # Process 'if' statements
            condition = self.interpret_node(node.children[0])
            then_expr = node.children[1]
            else_expr = node.children[2]
            if condition:
                return self.interpret_node(then_expr)
            else:
                return self.interpret_node(else_expr)
        
        elif node.type == "comparison_op":
            # Process comparison operations
            left = self.interpret_node(node.children[0])
            right = self.interpret_node(node.children[1])
            if node.value == ">":
                return left > right
            elif node.value == "<":
                return left < right
            elif node.value == ">=":
                return left >= right
            elif node.value == "<=":
                return left <= right
            elif node.value == "==":
                return left == right
            elif node.value == "!=":
                return left != right
            else:
                raise ValueError(f"Unknown operator: {node.value}")

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
