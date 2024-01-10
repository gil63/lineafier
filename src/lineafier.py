import sys
import ast


def convert_node(node: ast.AST) -> str:
    match node:
        case ast.Module():
            body = [convert_node(stmt) for stmt in node.body]
            return "; ".join(body)
        case ast.Expr():
            return convert_node(node.value)
        case ast.Call():
            func = convert_node(node.func)
            args = [convert_node(arg) for arg in node.args]
            keywords = [convert_node(arg) for arg in node.keywords]
            if args and keywords:
                return f"{func}({', '.join(args)},{', '.join(keywords)})"
            
            return f"{func}({', '.join(args)}{', '.join(keywords)})"
        case ast.Name():
            return node.id
        case ast.Constant():

            match node.value:
                case int():
                    return str(node.value)
                case str():
                    representation = node.value.replace("\n", "\\n")
                    return f"\"{representation}\""
                case bytes():
                    return str(node.value)
            
            raise ValueError(f"Constant type '{type(node.value).__name__}' not recognized")
        
        case ast.For():
            target = convert_node(node.target)
            iter_ = convert_node(node.iter)
            body = [convert_node(stmt) for stmt in node.body]
            return f"max(((0, {', '.join(body)}) for {target} in {iter_}), key=lambda x: x[0])"
        case ast.While():
            test = convert_node(node.test)
            body = [convert_node(stmt) for stmt in node.body]
            return f"max(((0, {', '.join(body)}) for {target} in iter(lambda: {test}), False), key=lambda x: x[0])"
        case ast.List():
            elts = [convert_node(elt) for elt in node.elts]
            return f"[{', '.join(elts)}]"
        case ast.Assign():
            return f"()"

    raise ValueError(f"Node type '{type(node).__name__}' not recognized")

def convert(code: str) -> str:
    return convert_node(ast.parse(code))

def convert_file(file: str) -> str:
    with open(file) as handle:
        return convert(handle.read())

def main() -> None:
    if len(sys.argv) < 2:
        print("input file not given")
        return
    print(convert_file(sys.argv[1]))

if __name__ == "__main__":
    main()
