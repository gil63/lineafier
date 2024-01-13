def a(b, c=3, /, d=1, *, q, t=None):
    print(b, c, d, q, t)

def b(*args, **kwargs):
    print(args, kwargs)

a(1, 2, 3, q=4, t=5)
b(1,2 ,4, a=4, b=3)

print((lambda x, /: 8)(5))

def f(**kwarg):
    print(kwarg)

print(f(a=1))
