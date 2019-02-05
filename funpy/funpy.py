from functools import reduce

# Functors?
identity = lambda x: x

# Composition
compose2 = lambda f, g: lambda x: f(g(x))
compose = lambda *fns: reduce(compose2, fns, identity)
pipe = lambda *fns: reduce(compose2, fns[::-1], identity)

# Accessors
prop = lambda key: lambda adict: adict[key] if key in adict else None

# Comparisions
ifElse = lambda ifFn, when, unless: lambda x: when(x) if ifFn(x) else unless(x)
when = lambda ifFn, when: ifElse(ifFn, when, identity)
unless = lambda ifFn, unless: ifElse(ifFn, identity, unless)
propEq = lambda key, val: lambda x: prop(key)(x) == val

# Monads
result = lambda ok: lambda data: {"ok": ok, "data": data}
resultGood = result(True)
resultBad = result(False)
resultData = prop("data")
resultIsOk = propEq("ok", True)
chainIfElse = lambda when, unless: ifElse(
    resultIsOk, compose(when, resultData), compose(unless, resultData)
)
chainWhen = lambda when: chainIfElse(when, identity)
chainUnless = lambda when: chainIfElse(identity, when)

# Operations
inc = lambda x: x + 1
