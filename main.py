from tokenizer import tokenize, parse
from interpret import Interpreter

# Example usage
if __name__ == "__main__":
    code = """
        let x = 10
        let y = 20
        
        fn add(a, b) = a + b
        fn multiply(a, b) = a * b
        
        if add(x, y) >= multiply(x, y) then
            "Addition is greater"
        else
            "Multiplication is greater"
    """
    tokens = tokenize(code)
    print("Tokens:", tokens)
    ast = parse(tokens)
    print("AST:", ast)

    interpreter = Interpreter()
    result = interpreter.interpret(ast)
    print(f"Result: {result}")
