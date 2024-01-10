import sys
import ast


def convert_node(node: ast.AST) -> str:
    match type(node):
        case ast.Module:
            body = [convert_node(stmt) for stmt in node.body]
            return "; ".join(body)
        case ast.Expr:
            return convert_node(node.value)
        case ast.Call:
            func = convert_node(node.func)
            args = [convert_node(arg) for arg in node.args]
            keywords = [convert_node(arg) for arg in node.keywords]
            if args and keywords:
                return f"{func}({', '.join(args)},{', '.join(keywords)})"
            
            return f"{func}({', '.join(args)}{', '.join(keywords)})"
        case ast.Name:
            return node.id
        case ast.Constant: # TODO: check for multiline string definitions
            return str(node.value)

    raise ValueError(f"Node type {type(node)} not recognized")

def main():
    if len(sys.argv) < 2:
        print("input file not given")
        return
    with open(sys.argv[1]) as file:
        tree = ast.parse(file.read())
    print(convert_node(tree))

if __name__ == "__main__":
    main()
