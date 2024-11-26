import re
from tokenizer import tokenize, parse
from interpret import Interpreter

# Example usage
if __name__ == "__main__":
    code = """
        let x = 10
        let y = 20
        
        fn add(a, b) = a + b
        fn multiply(a, b) = a * b
        
        let result = add(x, y)
        let product = multiply(x, y)
        
        if x >= y then
            let message = "x is greater than or equal to y"
        else
            let message = "x is less than y"
        
        message
    """
    tokens = tokenize(code)
    print("Tokens:", tokens)
    ast = parse(tokens)
    print("AST:", ast)

    interpreter = Interpreter()
    result = interpreter.interpret(ast)
    print(f"Result: {result}")
