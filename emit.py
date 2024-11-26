from main import ASTNode

class WASMEmitter:
    def __init__(self):
        self.result = ""
    
    def emit(self, nodes):
        for node in nodes:
            self.emit_node(node)
        return self.result
    
    def emit_node(self, node):
        match node.type:
            case "let":
                self.result += f"(local ${{node.value}} (f32.const {node.children[0].value}))\n"
            case "function":
                self.result += f"(func ${node.value} "
                self.emit_node(node.children[0])
                self.emit_node(node.children[1])
                self.result += ")\n"
            case "params":
                self.result += "(param "
                for child in node.children:
                    self.result += f"(local ${child} f32)"
                self.result += ")\n"
            case "call":
                self.result += f"(call ${node.value} "
                for child in node.children:
                    self.emit_node(child)
                self.result += ")\n"
            case "identifier":
                self.result += f"${node.value} "
            case "binary_op":
                self.emit_node(node.children[0])
                self.emit_node(node.children[1])
                self.result += f"(f32.{node.value})\n"
            case _:
                raise ValueError(f"Unknown node type: {node.type}")