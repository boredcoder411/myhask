from tokenizer import tokenize, parse
from interpret import Interpreter

# Example usage
if __name__ == "__main__":
    code = """
let x: int = 10
let y: int = 20

fn add(a: int, b: int) -> int = a + b
fn multiply(a: int, b: int) -> int = a * b

if add(x, y) >= multiply(x, y) then
    "Addition is greater"
else
    "Multiplication is greater"

match x {
    1 -> "one",
    2 -> "two",
    _ -> "unknown"
}
    """
    tokens = tokenize(code)
    print("Tokens:", tokens)
    ast = parse(tokens)
    print("AST:", ast)

    interpreter = Interpreter()
    result = interpreter.interpret(ast)
    print(f"Result: {result}")
