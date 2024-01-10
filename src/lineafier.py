import sys
import ast


def convert_node(node: ast.AST) -> str:
    match node:
        case ast.Module():
            body = [convert_node(stmt) for stmt in node.body]
            return "; ".join(body)
        case ast.FunctionDef():
            pass
        case ast.AsyncFunctionDef():
            pass
        case ast.ClassDef():
            pass
        case ast.Return():
            pass
        case ast.Delete():
            pass
        case ast.Assign():
            pass
        case ast.TypeAlias():
            pass
        case ast.AugAssign():
            pass
        case ast.AnnAssign():
            pass
        case ast.For():
            target = convert_node(node.target)
            iter_ = convert_node(node.iter)
            body = [convert_node(stmt) for stmt in node.body]
            return f"max(((0, {', '.join(body)}) for {target} in {iter_}), key=lambda x: x[0])"
        case ast.AsyncFor():
            pass
        case ast.While():
            test = convert_node(node.test)
            body = [convert_node(stmt) for stmt in node.body]
            return f"max(((0, {', '.join(body)}) for {target} in iter(lambda: {test}), False), key=lambda x: x[0])"
        case ast.If():
            pass
        case ast.With():
            pass
        case ast.AsyncWith():
            pass
        case ast.Match():
            pass
        case ast.Raise():
            pass
        case ast.Try():
            pass
        case ast.TryStar():
            pass
        case ast.Assert():
            pass
        case ast.Import():
            pass
        case ast.ImportFrom():
            pass
        case ast.Global():
            pass
        case ast.Nonlocal():
            pass
        case ast.Expr():
            return convert_node(node.value)
        case ast.Pass():
            pass
        case ast.BoolOp():
            pass
        case ast.NamedExpr():
            pass
        case ast.BinOp():
            pass
        case ast.UnaryOp():
            pass
        case ast.Lambda():
            pass
        case ast.IfExp():
            pass
        case ast.Dict():
            pass
        case ast.Set():
            pass
        case ast.ListComp():
            pass
        case ast.SetComp():
            pass
        case ast.DictComp():
            pass
        case ast.GeneratorExp():
            pass
        case ast.Await():
            pass
        case ast.Yield():
            pass
        case ast.YieldFrom():
            pass
        case ast.Compare():
            pass
        case ast.Call():
            func = convert_node(node.func)
            args = [convert_node(arg) for arg in node.args]
            keywords = [convert_node(arg) for arg in node.keywords]
            if args and keywords:
                return f"{func}({', '.join(args)},{', '.join(keywords)})"
            
            return f"{func}({', '.join(args)}{', '.join(keywords)})"
        case ast.FormattedValue():
            pass
        case ast.JoinedStr():
            pass
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
        case ast.Attribute():
            pass
        case ast.Subscript():
            pass
        case ast.Starred():
            pass
        case ast.Name():
            return node.id
        case ast.List():
            elts = [convert_node(elt) for elt in node.elts]
            return f"[{', '.join(elts)}]"
        case ast.Tuple():
            pass
        case ast.Slice():
            pass


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
