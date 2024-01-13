import sys
import ast


def _convert_body(body: list[ast.stmt]) -> str:
    return f"({', '.join(convert_node(stmt) for stmt in body)})"

def _convert_for(target: str, iter_: str, body: str):
    return f"max(((0, {body}) for {target} in {iter_}), key=lambda x: x[0])"

def _convert_arguments(posonlyargs: list[ast.arg], args: list[ast.arg], vararg: ast.arg, kwonlyargs: list[ast.arg], kw_defaults: [ast.expr], kwarg: ast.arg, defaults: list[ast.expr]) -> str:
    filled_defaults = [None] * (len(posonlyargs) + len(args) - len(defaults)) + defaults + kw_defaults
    args_strs = [arg.arg + ("" if default is None else f"={convert_node(default)}") for arg, default in zip(posonlyargs + args + kwonlyargs, filled_defaults)]

    if kwarg is not None:
        args_strs.append(f"**{kwarg.arg}")

    if vararg is not None:
        args_strs.insert(len(posonlyargs) + len(args), f"*{vararg.arg}")
    elif kwonlyargs:
        args_strs.insert(len(posonlyargs) + len(args), "*")

    if posonlyargs:
        args_strs.insert(len(posonlyargs), "/")
    
    return ", ".join(args_strs)

def convert_node(node: ast.AST) -> str:
    match node:
        case ast.Module():
            return _convert_body(node.body)
        case ast.FunctionDef():
            args_str = _convert_arguments(node.args.posonlyargs, node.args.args, node.args.vararg, node.args.kwonlyargs, node.args.kw_defaults, node.args.kwarg, node.args.defaults)

            if node.decorator_list:
                decorator_strs = [convert_node(decorator) for decorator in node.decorator_list]

                return f"{node.name} := {'('.join(decorator_strs)}(lambda {args_str}: {_convert_body(node.body)}{')' * len(decorator_strs)}"
            
            return f"{node.name} := lambda {args_str}: {_convert_body(node.body)}"
        case ast.AsyncFunctionDef():
            pass
        case ast.ClassDef():
            pass
        case ast.Return():
            pass
        case ast.Delete():
            pass
        case ast.Assign():
            targets = [convert_node(target) for target in node.targets]
            value = convert_node(node.value)
            if len(targets) == 1:
                return f"{targets[0]} := {value}"
            return f"({', '.join(targets[0])}) := {value}"
        case ast.AugAssign():
            pass
        case ast.AnnAssign():
            pass
        case ast.For():
            return _convert_for(convert_node(node.target), convert_node(node.iter), _convert_body(node.body))
        case ast.AsyncFor():
            pass
        case ast.While():
            return _convert_for("_", f"iter(lambda: {convert_node(node.test)}, False)", _convert_body(node.body))
        case ast.If():
            body = _convert_body(node.body)
            test = convert_node(node.test)
            orelse = _convert_body(node.orelse)
            return f"({body} if {test} else {orelse})"
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
            left = convert_node(node.left)
            right = convert_node(node.right)
            match node.op:
                case ast.Add():
                    op = "+"
                case ast.Sub():
                    op = "-"
                case ast.Mult():
                    op = "*"
                case ast.Div():
                    op = "/"
                case ast.FloorDiv():
                    op = "//"
                case ast.Mod():
                    op = "%"
                case ast.Pow():
                    op = "**"
                case ast.LShift():
                    op = "<<"
                case ast.RShift():
                    op = ">>"
                case ast.BitOr():
                    op = "|"
                case ast.BitXor():
                    op = "^"
                case ast.BitAnd():
                    op = "&"
                case ast.MatMult():
                    op = "@"
            return f"({left} {op} {right})"
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
            ret = convert_node(node.left)
            
            for op, comparator in zip(node.ops, node.comparators):
                ret += " "
                match op:
                    case ast.Eq():
                        ret += "=="
                    case ast.NotEq():
                        ret += "!="
                    case ast.Lt():
                        ret += "<"
                    case ast.LtE():
                        ret += "<="
                    case ast.Gt():
                        ret += ">"
                    case ast.GtE():
                        ret += ">="
                    case ast.Is():
                        ret += "is"
                    case ast.IsNot():
                        ret += "is not"
                    case ast.In():
                        ret += "in"
                    case ast.NotIn():
                        ret += "not in"
                ret += " " + convert_node(comparator)
            
            return ret
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
                case None:
                    return "None"
            
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
