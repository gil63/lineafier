def a(b, c=3, /, d=1, *, q, t=None):
    print(b, c, d, q, t)

def b(*args, **kwargs):
    print(args, kwargs)

a(1, 2, 3, 4, 5)
