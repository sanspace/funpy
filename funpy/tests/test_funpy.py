import funpy as fp

def test_identity():
    assert fp.identity(10) == 10
    assert fp.identity("cat") == "cat"
    assert fp.identity(32.2) != 32
    
def test_inc():
    assert fp.inc(1) == 2

def test_merge():
    assert fp.merge({"a": 1, "b": 2, })({"c": 3}) == {"a": 1, "b": 2, "c": 3}
    assert fp.merge({"a": 1, "b": 2, })({"b": 3}) == {"a": 1, "b": 3}

def test_trim():
    assert fp.trim("  ") == ""
    assert fp.trim("") == ""
    assert fp.trim(" a ") == "a"
def test_prop():
    assert fp.prop("name")({"name": "bob", "age": 34}) == "bob"
    assert fp.prop("shoesize")({"name": "bob", "age": 34}) == None

def test_attr():
    class person():
        def __init__(self):
            self.name="bob"
    assert(fp.attr("name")(person()) == "bob")

def test_conditional():
    isOne = lambda x: x == 1
    addOne = lambda x: x + 1
    assert fp.ifElse(isOne, addOne, lambda x: x)(1) == 2
    assert fp.ifElse(isOne, addOne, lambda x: x+2)(5) == 7
    assert fp.when(isOne, addOne)(1) == 2
    assert fp.unless(isOne, addOne)(1) == 1
    assert fp.when(isOne, addOne)(5) == 5
    assert fp.unless(isOne, addOne)(5) == 6

def test_compare():
    assert fp.propEq("name", "bob")({"name": "bob"}) == True
    assert fp.propEq("name", "john")({"name": "bob"}) == False
    assert fp.propEq("age", 34)({"name": "bob"}) == False

def test_isNone():
    assert(fp.isNone(None) == True)
    assert(fp.isNone("bob") == False)

def test_isNotNone():
    assert(fp.isNotNone(None) == False)
    assert(fp.isNotNone("bob") == True)

def test_emptyString():
    assert fp.emptyString("  ") == False
    assert fp.emptyString("") == True
    assert fp.emptyString(" a ") == False

def test_trimEmpty():
    assert fp.trimEmpty("  ") == True
    assert fp.trimEmpty("") == True
    assert fp.trimEmpty(" a ") == False
    assert fp.trimEmpty(None) == True

def test_map():
    assert fp.map(lambda x: x+1)([1,2,3]) == [2,3,4]

def test_filter():
    assert fp.filter(lambda x: x!=2)([1,2,3]) == [1,3,]

def test_compose():
    addOne = lambda x: x+1
    multFive = lambda x: x*5
    assert fp.compose(multFive, addOne)(1) == 10
    assert fp.pipe(addOne, multFive)(1) == 10

def test_monads():
    assert fp.resultGood("cat") == {"ok": True, "data": "cat"}
    assert fp.resultBad("dog") == {"ok": False, "data": "dog"}
    assert fp.resultData({"ok": True, "data": "smoke"}) == "smoke"
    assert fp.resultData({"ok": True, "dat": "smoke"}) == None
    assert fp.resultIsOk({"ok": True, "data": "smoke"}) == True
    assert fp.resultIsOk({"ok": False, "data": "smoke"}) == False

def test_chain():
    good = {"ok": True, "data": 1}
    bad = {"ok": False, "data": 5}
    inc = lambda x: x+1
    dec = lambda x: x-1
    assert fp.chainIfElse(inc, dec)(good) == 2
    assert fp.chainIfElse(inc, dec)(bad) == 4
    assert fp.chainWhen(inc)(good) == 2
    assert fp.chainUnless(inc)(good) == good
    assert fp.chainWhen(inc)(bad) == bad
    assert fp.chainUnless(inc)(bad) == 6

def test_maybe():
    isOne = lambda x: x == 1
    addOne = lambda x: x + 1
    assert fp.maybe(isOne, addOne, lambda x: x)(1) == {"ok": True, "data": 2}
    assert fp.maybe(isOne, addOne, lambda x: x+2)(5) == {"ok": False, "data": 7}

def test_validate():
    x = {"name": "bob", "foo": "bar"}
    checks = [
        fp.check("name", lambda x: x=="bob", "it's bob"),
        fp.check("age", lambda x: x is None, "age needed"),
        fp.check("foo", lambda x: x != "bar", "foobar!"),
    ]
    assert fp.validate(checks)(x) == {
        "ok": False, "data": ["it's bob", "age needed"]
    }
    assert fp.validate(checks)({**x, **{"age": 10}}) == {
        "ok": False, "data": ["it's bob",]
    }
    good = {"name": "john", "age": 10, "foo": "bar"}
    assert fp.validate(checks)(good) == {
        "ok": True, "data": good
    }
