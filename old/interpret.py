class Interpreter:
    def __init__(self):
        self.environment = {}  # Stores variables and functions
        self.types = {}        # Stores type information for variables and functions

    def interpret(self, nodes):
        results = []
        for node in nodes:
            result = self.interpret_node(node)
            results.append(result)
        return results

    def interpret_node(self, node):
        if node.type == "let":
            # Process 'let' statements with type enforcement
            name = node.value
            var_type = node.children[0].value  # Type annotation
            value = self.interpret_node(node.children[1])  # Value expression

            self._check_type(var_type, value, f"Variable '{name}'")
            self.environment[name] = value
            self.types[name] = var_type  # Store type info
            return value

        elif node.type == "function":
            # Process function definitions with type annotations
            name = node.value
            params_node = node.children[0]  # Params node
            params = []
        
            for param_node in params_node.children:
                param_name = param_node.value
                param_type = param_node.children[0].value  # Type of the parameter
                params.append((param_name, param_type))
            
            return_type = node.children[1].value  # Return type
            body = node.children[2]
        
            self.environment[name] = (params, return_type, body)
            self.types[name] = "function"
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
            
            params, return_type, body = self.environment[func_name]
            args = [self.interpret_node(child) for child in node.children]
        
            if len(params) != len(args):
                raise TypeError(f"Function {func_name} expects {len(params)} arguments, got {len(args)}")
        
            # Type-check arguments
            for (param_name, param_type), arg in zip(params, args):
                self._check_type(param_type, arg, f"Argument '{param_name}' in function '{func_name}'")
            
            # Temporary scope for function execution
            old_env = self.environment.copy()
            self.environment.update({param_name: arg for (param_name, _), arg in zip(params, args)})
            result = self.interpret_node(body)
            self.environment = old_env  # Restore previous environment
        
            # Type-check the return value
            self._check_type(return_type, result, f"Return value of function '{func_name}'")
            return result

        elif node.type == "if":
            # Process 'if' statements
            condition = self.interpret_node(node.children[0])
            then_expr = node.children[1]
            else_expr = node.children[2]

            if not isinstance(condition, bool):
                raise TypeError(f"Condition in 'if' statement must be a boolean, got {type(condition).__name__}")
            
            if condition:
                return self.interpret_node(then_expr)
            else:
                return self.interpret_node(else_expr)

        elif node.type == "comparison_op":
            # Process comparison operations
            left = self.interpret_node(node.children[0])
            right = self.interpret_node(node.children[1])

            self._check_type("int", left, "Comparison operator")
            self._check_type("int", right, "Comparison operator")

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

            if node.value in "+-*/":
                self._check_type("int", left, "Binary operator")
                self._check_type("int", right, "Binary operator")

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

        elif node.type == "match":
            # Process match expressions
            subject = self.interpret_node(node.children[0])

            for case in node.children[1:]:
                pattern = case.children[0]
                expr = case.children[1]

                if self._pattern_match(pattern, subject):
                    return self.interpret_node(expr)
            raise ValueError(f"No matching pattern found for {subject}")

        else:
            raise ValueError(f"Unknown node type: {node.type}")

    def _pattern_match(self, pattern, subject):
        """Helper method to check if a pattern matches a subject."""
        if pattern.type == "wildcard":
            return True
        elif pattern.type in ["literal", "string"]:
            return pattern.value == subject
        elif pattern.type == "identifier":
            self.environment[pattern.value] = subject
            return True
        return False

    def _check_type(self, expected_type, value, context):
        """Runtime type checking to enforce static typing."""
        actual_type = type(value).__name__
        if expected_type == "int" and not isinstance(value, int):
            raise TypeError(f"{context}: Expected type 'int', got '{actual_type}'")
        elif expected_type == "str" and not isinstance(value, str):
            raise TypeError(f"{context}: Expected type 'str', got '{actual_type}'")
        elif expected_type == "bool" and not isinstance(value, bool):
            raise TypeError(f"{context}: Expected type 'bool', got '{actual_type}'")
        # Add more types as needed

