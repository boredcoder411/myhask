import re
from tokenizer import tokenize, parse
from interpret import Interpreter

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
