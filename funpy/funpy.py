from functools import reduce

# Functors?
identity = lambda x: x

# Operations
inc = lambda x: x + 1
merge = lambda f: lambda g: {**f, **g}
trim = lambda x: x.strip() if x is not None else x

# First class functions
map = lambda fn: lambda arr: [fn(a) for a in arr]
filter = lambda fn: lambda arr: [a for a in arr if fn(a)]

# Composition
compose2 = lambda f, g: lambda x: f(g(x))
compose = lambda *fns: reduce(compose2, fns, identity)
pipe = lambda *fns: reduce(compose2, fns[::-1], identity)

# Accessors
prop = lambda key: lambda adict: adict[key] if key in adict else None
attr = lambda name: lambda cls: getattr(cls, name, None)

# Comparisions
ifElse = lambda ifFn, when, unless: lambda x: when(x) if ifFn(x) else unless(x)
when = lambda ifFn, when: ifElse(ifFn, when, identity)
unless = lambda ifFn, unless: ifElse(ifFn, identity, unless)
propEq = lambda key, val: lambda x: prop(key)(x) == val
isNone = lambda x: x is None
isNotNone = lambda x: x is not None
emptyString = lambda x: x=="" or x == None
trimEmpty = compose(emptyString, trim)

# Monads
result = lambda ok: lambda data: {"ok": ok, "data": data}
resultGood = result(True)
resultBad = result(False)
resultData = prop("data")
resultIsOk = propEq("ok", True)
chain = lambda when, unless: ifElse(resultIsOk, when, unless)
chainIfElse = lambda when, unless: chain(
    compose(when, resultData), compose(unless, resultData)
)
chainWhen = lambda when: chain(compose(when, resultData), identity)
chainUnless = lambda unless: chain(identity, compose(unless, resultData))
maybe = lambda ifFn, when, unless: ifElse(
    ifFn, compose(resultGood, when), compose(resultBad, unless)
)
check = lambda prop, fn, msg: {"prop": prop, "fn": fn, "msg": msg}
validate = lambda checks: lambda data: compose(
    maybe(lambda x: len(x)==0, lambda noErr: data, identity),
    lambda data: [
        c["msg"] for c in checks
        if c["fn"](prop(c["prop"])(data))
    ]
)(data)
