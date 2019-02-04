# 1. The Operand Stack
    # The operand stack should be implemented as a Python list
    # The list will contain Python integers, arrays, and later in Part 2 code arrays
    # Python integers and lists on the stack represent Postscript integer constants and array constants.
    #  Python strings which start with a slash / on the stack represent names of Postscript variables.
    # The hot end is where pushing and popping happens from the list, I will use the end of the list as the hot end
    # For all operators you need to implement basic checks, i.e., check whether there are sufficient number of values in the operand stack and check whether those values have correct types.
# 2. The Dictionary Stack
    # The dictionary stack is also implemented as a Python list.
    # It will contain Python dictionaries which will be the implementation for Postscript dictionaries.
    # The dictionary stack needs to support adding and removing dictionaries at the hot end, as well as defining and looking up names.
# 3. Operators
    # Operators will be implemented as zero-argument Python functions that manipulate the operand and dictionary stacks.
    # The begin and end operators are a little different in that they manipulate the dictionary stack in addition to or instead of the operand stack.
    # Note about dict: Remember that the dict operator takes an integer operand from the operand stack and pushes an empty dictionary to the operand stack (affects only the operand stack).
# 4. Name Lookup
    # Name lookup is implemented by a Python function
    # Note that name lookup is not a Postscript operator, but you will implement it in your interpreter.

# ------------------------- 10% -------------------------------------
# The operand stack:
opstack = []


# Pops values from the top of the stack (end of the list)
def opPop():
    return opstack.pop(len(opstack)-1)


# Pushes values onto the top of the stack (end of the list)
def opPush(value):
    opstack.append(value)


# Pushes values onto the top of the stack (end of the list)
def opSize():
    return len(opstack)


# -------------------------- 20% -------------------------------------
#  The dictionary stack:
dictstack = []


# Pops values from the top of the stack (end of the list)
def dictPop():
    return dictstack.pop()


# Pushes values onto the top of the stack (end of the list)
def dictPush(value):
    if type(value) is dict:
        dictstack.append(value)

''' dictPush pushes a new dictionary to the dictstack. Note that, your interpreter
   will call dictPush only when Postscript “begin” operator is called. “begin”
   should pop the empty dictionary from the opstack and push it onto the dictstack
   by calling dictPush. You may either pass this dictionary (which you popped from
   opstack) to dictPush as a parameter or just simply push a new empty dictionary in dictPush.'''


# add name:value to the top dictionary in the dictionary stack.
def define(name, value):
    if type(name) is str:
        newdict = dict(name=name, value=value);
        dictPush(newdict)


# return the value associated with name or None if key is not found
def lookup(name):
    size = len(dictstack)
    for i in range(size):
        top = dictstack[size-i-1]
        if top != {} and top["name"][1:] == name:
            return top["value"]
    return None


# --------------------------- 15% -------------------------------------
# Arithmetic and comparison operators: add, sub, mul, div, eq, lt, gt
# Make sure to check the operand stack has the correct number of parameters and types of the parameters are correct.
def add():
    opPush(opPop() + opPop())


def sub():
    num = opPop()
    opPush(opPop() - num)


def mul():
    opPush(opPop() * opPop())


def div():
    num = opPop()
    opPush(opPop() / num)


def eq():
    opPush(opPop() == opPop())


def lt():
    num = opPop()
    opPush(opPop() < num)


def gt():
    num = opPop()
    opPush(opPop() > num)


# --------------------------- 15% -------------------------------------
# Array operators: length, get

# Removes the array object from the stack
# and pushes the length of the array onto the stack
def length():
    arr = opPop()
    if type(arr) is list:
        opPush(len(arr))


# Removes the <index> and array object from the stack
def get():
    index = opPop()
    arr = opPop()
    if type(arr) is list:
        opPush(arr[index])


# --------------------------- 15% -------------------------------------
# Boolean operators: psAnd, psOr, psNot that take boolean operands only
def psAnd():
    bool1 = opPop()
    bool2 = opPop()
    if type(bool1) is bool and type(bool2) is bool:
        opPush(True if bool1 and bool2 else False)


def psOr():
    bool1 = opPop()
    bool2 = opPop()
    if type(bool1) is bool and type(bool2) is bool:
        opPush(True if bool1 or bool2 else False)


def psNot():
    bool1 = opPop()
    if type(bool1) is bool:
        opPush(True if not bool1 else False)


# --------------------------- 25% -------------------------------------
# Stack manipulation and print operators: dup, exch, pop, copy, clear, stack

# Duplicate the top value on the stack
def dup():
    val = opPop()
    opPush(val)
    opPush(val)


# Exchange the top two stack values
def exch():
    val1 = opPop()
    val2 = opPop()
    opPush(val1)
    opPush(val2)


# Pop the top value from the stack
def pop():
    return opPop()


# copy the top stack values onto the stack
def copy():
    val = opPop()
    opPush(val)
    opPush(val)


# Clears all elements from the stack
def clear():
    opstack.clear()


# Display the contents of the stack
def stack():
    for item in opstack:
        print(item)


# --------------------------- 20% -------------------------------------
# Dictionary manipulation operators: psDict, begin, end, psDef
def psDict():
    num = opPop()
    for i in range(num):
        opPush(dict())


# Takes a dictionary from the top of the operand stack and pushes it on the dictionary stack.
def begin():
    value = opPop()
    if type(value) is dict:
        dictPush(value)


# Pop the top dictionary from the dictionary stack and throw it away
def end():
    dictPop()


# always creates or modifies a dictionary entry in the top most dictionary on the dictionary stack
# Pops the name and value from operand stack and call the “define” function.
def psDef():
    value = opPop()
    name = opPop()
    define(name, value)

# --------------------------- TEST FUNCTIONS -----------------------------------
# ------- Part 1 TEST CASES--------------
def testDefine():
    define("/n2", 5)
    if lookup("n2") != 5:
        return False
    return True


def testLookup():
    opPush("/n4")
    opPush(7)
    psDef()
    if lookup("n4") != 7:
        return False
    return True


# Arithmatic operator tests
def testAdd():
    opPush(-9)
    opPush(21)
    add()
    if opPop() != 12:
        return False
    return True


def testSub():
    opPush(11)
    opPush(4.5)
    sub()
    if opPop() != 6.5:
        return False
    return True


def testMul():
    opPush(-2)
    opPush(4.5)
    mul()
    if opPop() != -9:
        return False
    return True


def testDiv():
    opPush(-12)
    opPush(4)
    div()
    if opPop() != -3:
        return False
    return True


# Comparison operators tests
def testEq():
    opPush(6)
    opPush(7)
    eq()
    if opPop() != False:
        return False
    return True


def testLt():
    opPush(6)
    opPush(4)
    lt()
    if opPop() != False:
        return False
    return True


def testGt():
    opPush(1)
    opPush(9)
    gt()
    if opPop() != False:
        return False
    return True


# boolean operator tests
def testPsAnd():
    opPush(True)
    opPush(True)
    psAnd()
    if opPop() != True:
        return False
    return True


def testPsOr():
    opPush(False)
    opPush(False)
    psOr()
    if opPop() != False:
        return False
    return True


def testPsNot():
    opPush(False)
    psNot()
    if opPop() != True:
        return False
    return True


# Array operator tests
def testLength():
    opPush([1, 2, 3, 4, 5, 6, 7])
    length()
    if opPop() != 7:
        return False
    return True


def testGet():
    opPush([1, 2, 21, 4, -2])
    opPush(2)
    get()
    if opPop() != 21:
        return False
    return True


# stack manipulation functions
def testDup():
    opPush(11)
    dup()
    if opPop() != opPop():
        return False
    return True


def testExch():
    opPush(12)
    opPush("/var")
    exch()
    if opPop() != 12 and opPop() != "/var":
        return False
    return True


def testPop():
    l1 = len(opstack)
    opPush(10)
    pop()
    l2 = len(opstack)
    if l1 != l2:
        return False
    return True


def testCopy():
    opPush(1)
    opPush(2)
    opPush(3)
    opPush(4)
    opPush(5)
    opPush(2)
    copy()
    if opPop() != 5 and opPop() != 4 and opPop() != 5 and opPop() != 4 and opPop() != 3 and opPop() != 2:
        return False
    return True


def testClear():
    opPush(10)
    opPush("/x")
    clear()
    if len(opstack) != 0:
        return False
    return True


# dictionary stack operators
def testDict():
    opPush(1)
    psDict()
    if opPop() != {}:
        return False
    return True


def testBeginEnd():
    opPush("/x")
    opPush(3)
    psDef()
    opPush({})
    begin()
    opPush("/x")
    opPush(4)
    psDef()
    end()
    if lookup("x") != 3:
        return False
    return True


def testpsDef():
    opPush("/x")
    opPush(10)
    psDef()
    if lookup("x") != 10:
        return False
    return True


def testpsDef2():
    opPush("/x")
    opPush(-11)
    psDef()
    opPush(1)
    psDict()
    begin()
    if lookup("x") != -11:
        end()
        return False
    end()
    return True


def main_part1():
    testCases = [('define', testDefine), ('lookup', testLookup), ('add', testAdd), ('sub', testSub), ('mul', testMul),
                 ('div', testDiv),
                 ('eq', testEq), ('lt', testLt), ('gt', testGt), ('psAnd', testPsAnd), ('psOr', testPsOr),
                 ('psNot', testPsNot),
                 ('length', testLength), ('get', testGet), ('dup', testDup), ('exch', testExch), ('pop', testPop),
                 ('copy', testCopy),
                 ('clear', testClear), ('dict', testDict), ('begin', testBeginEnd), ('psDef', testpsDef),
                 ('psDef2', testpsDef2)]
    # add you test functions to this list along with suitable names
    failedTests = [testName for (testName, testProc) in testCases if not testProc()]
    if failedTests:
        return ('Some tests failed', failedTests)
    else:
        return ('All part-1 tests OK')


if __name__ == '__main__':
    print(main_part1())




