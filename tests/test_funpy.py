from funpy import funpy as fp

def test_identity():
    assert fp.identity(10) == 10
    assert fp.identity("cat") == "cat"
    assert fp.identity(32.2) != 32

def test_prop():
    assert fp.prop("name")({"name": "bob", "age": 34}) == "bob"
    assert fp.prop("shoesize")({"name": "bob", "age": 34}) == None

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
    assert fp.chainUnless(inc)(good) == 1
    assert fp.chainWhen(inc)(bad) == 5
    assert fp.chainUnless(inc)(bad) == 6

def test_inc():
    assert fp.inc(1) == 2
