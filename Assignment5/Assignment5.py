# Austin Marino - 11507852
import re
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# ------------------------- 10% -------------------------------------
# The operand stack:
opstack = []


# Pops values from the top of the stack (end of the list)
def opPop():
    try:
        return opstack.pop(len(opstack)-1)
    except:
        pass


# Pushes values onto the top of the stack (end of the list)
def opPush(value):
    opstack.append(value)


# Pushes values onto the top of the stack (end of the list)
def opSize():
    opPush(len(opstack))


# -------------------------- 20% -------------------------------------
#  The dictionary stack:
dictstack = [({}, 0)]


# Pops values from the top of the stack (end of the list)
def dictPop():
    try:
        dictstack.pop()
    except:
        pass


# Pushes values onto the top of the stack (end of the list)
def dictPush(name, value):
    top = len(dictstack) - 1
    dictstack[top][0][name] = value


def dictClear():
    dictstack.clear()
    dictstack.append(({}, 0))

''' dictPush pushes a new dictionary to the dictstack. Note that, your interpreter
   will call dictPush only when Postscript “begin” operator is called. “begin”
   should pop the empty dictionary from the opstack and push it onto the dictstack
   by calling dictPush. You may either pass this dictionary (which you popped from
   opstack) to dictPush as a parameter or just simply push a new empty dictionary in dictPush.'''


# add name:value to the top dictionary in the dictionary stack.
def define(name, value):
    if isinstance(name, str):
        name = name.replace("/", "")
        dictPush(name, value)


# return the value associated with name or None if key is not found
def lookup(name, scope):
    returnTuple = ()
    if scope == "static":
        currentScope = len(dictstack)-1
        returnTuple = staticFind(name, currentScope)
    else:
        returnTuple = dynamicFind(name)
    parentScope = returnTuple[0]
    value = returnTuple[1]
    if isinstance(value, list):
        functCheck = [type(i) for i in value]
        if functCheck.count(int) == len(functCheck):
            opPush(value)
            return
        else:
            addScope(parentScope)
            codeArray = iter(value)
            interpretSPS(codeArray, scope)
            dictstack.pop()
            return
    else:
        opPush(value)


def staticFind(name, scope):
    parentScope = dictstack[scope][1]
    functions = dictstack[scope][0]
    if parentScope == scope:
        return (scope, functions[name])
    elif functions.get(name, None) != None:
        return (scope, functions[name])
    else:
        return staticFind(name, parentScope)


def dynamicFind(name):
    size = len(dictstack)
    for i in range(size):
        index = size-i-1
        functions = dictstack[index][0]
        if functions.get(name, None) != None:
            return (index, functions[name])


# --------------------------- 15% -------------------------------------
# Arithmetic and comparison operators: add, sub, mul, div, eq, lt, gt
# Make sure to check the operand stack has the correct number of parameters and types of the parameters are correct.
def add():
    num1 = opPop()
    num2 = opPop()
    if ((isinstance(num1, int) or isinstance(num1, float))
            and (isinstance(num2, int) or isinstance(num2, float))):
        opPush(num1 + num2)
    else:
        opPush(num2)
        opPush(num1)


def sub():
    num2 = opPop()
    num1 = opPop()
    if ((isinstance(num1, int) or isinstance(num1, float))
            and (isinstance(num2, int) or isinstance(num2, float))):
        opPush(num1 - num2)
    else:
        opPush(num2)
        opPush(num1)


def mul():
    num1 = opPop()
    num2 = opPop()
    if ((isinstance(num1, int) or isinstance(num1, float))
            and (isinstance(num2, int) or isinstance(num2, float))):
        opPush(num1 * num2)
    else:
        opPush(num2)
        opPush(num1)


def div():
    num2 = opPop()
    num1 = opPop()
    if ((isinstance(num1, int) or isinstance(num1, float))
            and (isinstance(num2, int) or isinstance(num2, float))):
        opPush(num1 / num2)
    else:
        opPush(num2)
        opPush(num1)


def eq():
    num1 = opPop()
    num2 = opPop()
    if ((isinstance(num1, int) or isinstance(num1, float))
            and (isinstance(num2, int) or isinstance(num2, float))):
        opPush(num1 == num2)
    else:
        opPush(num2)
        opPush(num1)


def lt():
    num2 = opPop()
    num1 = opPop()
    if ((isinstance(num1, int) or isinstance(num1, float))
            and (isinstance(num2, int) or isinstance(num2, float))):
        opPush(num1 < num2)
    else:
        opPush(num2)
        opPush(num1)


def gt():
    num2 = opPop()
    num1 = opPop()
    if ((isinstance(num1, int) or isinstance(num1, float))
            and (isinstance(num2, int) or isinstance(num2, float))):
        opPush(num1 > num2)
    else:
        opPush(num2)
        opPush(num1)



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
    opPop()


# copy the top stack values onto the stack
def copy():
    n = opPop()
    val = opPop()
    opPush(val)
    for i in range(n):
        opPush(val)


# Clears all elements from the stack
def clear():
    opstack.clear()


# Display the contents of the stack
def stack():
    print("==============")
    size = len(opstack)
    for i in range(size):
        print(opstack[size-1-i])
    displayDicts()


# --------------------------- 20% -------------------------------------
# Dictionary manipulation operators: psDict, begin, end, psDef
def addScope(parentScope):
    dictstack.append(({}, parentScope))

# always creates or modifies a dictionary entry in the top most dictionary on the dictionary stack
# Pops the name and value from operand stack and call the “define” function.
def psDef():
    value = opPop()
    name = opPop()
    define(name, value)

def displayDicts():
    print("==============")
    size = len(dictstack)
    for i in range(size):
        scope = size - i - 1
        top = dictstack[scope]
        functions = top[0]
        parentScope = top[1]
        print("----", scope, "----", parentScope, "----")
        for key, value in functions.items():
            print("/" + key + " ", value)
    print("==============")


functDict = {
    "opPop": opPop,
    "opSize": opSize,
    "dictPop": dictPop,
    "add": add,
    "sub": sub,
    "mul": mul,
    "div": div,
    "eq": eq,
    "lt": lt,
    "gt": gt,
    "length": length,
    "get": get,
    "and": psAnd,
    "or": psOr,
    "not": psNot,
    "dup": dup,
    "exch": exch,
    "pop": pop,
    "copy": copy,
    "clear": clear,
    "stack": stack,
    "def": psDef
}


def psIf():
    arr = opPop()
    boolean = opPop()
    if isinstance(boolean, bool) and boolean == True:
        arr = iter(arr)
        interpretSPS(arr)


def psIfelse():
    arr1 = opPop()
    arr2 = opPop()
    boolean = opPop()
    if isinstance(boolean, bool) and boolean == True:
        arr2 = iter(arr2)
        interpretSPS(arr2)
    else:
        arr1 = iter(arr1)
        interpretSPS(arr1)


def psFor():
    codearray = opPop()
    final = opPop()
    incr = opPop()
    init = opPop()
    if(incr > 0):
        while(init <= final):
            opPush(init)
            funct = iter(codearray)
            interpretSPS(funct)
            init += incr
    else:
        while (init >= final):
            opPush(init)
            funct = iter(codearray)
            interpretSPS(funct)
            init += incr


def forAll():
    codearray = opPop()
    arr = opPop()
    for item in arr:
        opPush(item)
        funct = iter(codearray)
        interpretSPS(funct)


spsDict = {
    "if": psIf,
    "ifelse": psIfelse,
    "for": psFor,
    "forall": forAll
}


def tokenize(s):
    return re.findall("/?[a-zA-Z][a-zA-Z0-9_]*|[[][a-zA-Z0-9_\s!][a-zA-Z0-9_\s!]*[]]|[-]?[0-9]+|[}{]+|%.*|[^ \t\n]", s)


# The it argument is an iterator.
# The sequence of return characters should represent a list of properly nested
# tokens, where the tokens between '{' and '}' is included as a sublist. If the
# parenteses in the input iterator is not properly nested, returns False.
def groupMatching(it):
    res = []
    for c in it:
        if c == '}':
            return res
        elif c == '{':
            res.append(groupMatching(it))
        else:
            res.append(convert(c))
    return False


def arrayMatching(it):
    res = []
    it = it.split(" ")
    for c in it:
        end = c[-1]
        start = c[0]
        if end == ']':
            res.append(convert(c[0:-1]))
            return res
        elif start == '[':
            res.append(arrayMatching(it))
        elif c != ' ':
            res.append(convert(c))
    return False


def canConvert(variable, typeOf):
    try:
        return typeOf(variable)
    except:
        return variable


# Function to parse a list of tokens and arrange the tokens between { and } braces
# as code-arrays.
# Properly nested parentheses are arranged into a list of properly nested lists.
def parse(tokens):
    res = []
    it = iter(tokens)
    for c in it:
        if c == '}' or c == ']':
            # non matching closing paranthesis; return false since there is
            # a syntax error in the Postscript code.
            return False
        elif c == '{':
            res.append(groupMatching(it))
        elif c[0] == '[':
            arr = arrayMatching(c[1:])
            res.append(arr)
        else:
            res.append(convert(c))
    return res


def convert(val):
    if val == 'true':
        return True
    elif val == 'false':
        return False
    elif '.' in val:
        return canConvert(val, float)
    else:
        return canConvert(val, int)

currentScope = 0
# This is the recursive function to interpret a given code array.
# code is a code array; scope is a string (either “static” or “dynamic”)
def interpretSPS(code, scope):
    try:
        item = next(code)
        if isinstance(item, str):
            if '/' in item:
                opPush(item)
            elif functDict.get(item, None) != None:
                functDict[item]()
            elif spsDict.get(item, None) != None:
                spsDict[item]()
            else:
                lookup(item, scope)
        elif isinstance(item, list) or isinstance(item, (int, float, complex)) or isinstance(item, bool):
            opPush(item)
        return interpretSPS(code, scope)
    except StopIteration:
        return None


# s is a string; scope is a string (either “static” or “dynamic”)
def interpreter(s, scope):
    code = iter(parse(tokenize(s)))
    interpretSPS(code, scope)


# Test Inputs
input1 = """
    /x 4 def
    /g { x stack } def
    /f { /x 7 def g } def
    f
"""

input2 = """
    /m 50 def
    /n 100 def
    /egg1 {/m 25 def n} def
    /chic {
        /n 1 def
        /egg2 { n } def 
        m n
        egg1
        egg2
        stack 
    } def
    n chic
"""

input3 = """
    /x 10 def
    /A { x } def
    /C { /x 40 def A stack } def
    /B { /x 30 def /A { x } def C } def B
"""

input4 = """
    /x 4 def
    /g { x } def
    /f { /x 7 def chic } def
    /chic {
            /x 22 def 
            g
            stack 
        } def
    f
"""

input5 = """
    /Add { 4 num add } def
    /x 6 def
    /num x def
    /Mul { /x 9 def num Add mul stack } def
    /Compute {
            /num x def 
            /Add { 2 num add } def 
            Mul
        } def
    Compute
"""


def clearStacks():
    clear()
    dictClear()


def test1():
    print("\n***** Test 1 *****")
    isSuccessful = False
    print("Static")
    interpreter(input1, "static")
    result1 = opPop()
    clearStacks()
    print("\nDynamic")
    interpreter(input1, "dynamic")
    result2 = opPop()
    if result1 == 4 and result2 == 7:
        isSuccessful = True
    clearStacks()
    return isSuccessful


def test2():
    print("\n***** Test 2 *****")
    isSuccessful = False
    print("Static")
    interpreter(input2, "static")
    list1 = [100, 50, 1, 100, 1]
    result1 = True
    for i in range(len(opstack)):
        if opstack[i] != list1[i]:
            result1 = False
            break
    clearStacks()
    print("\nDynamic")
    interpreter(input2, "dynamic")
    list2 = [100, 50, 1, 1, 1]
    result2 = True
    for i in range(len(opstack)):
        if opstack[i] != list2[i]:
            result2 = False
            break
    if result1 and result2:
        isSuccessful = True
    clearStacks()
    return isSuccessful


def test3():
    print("\n***** Test 3 *****")
    isSuccessful = False
    print("Static")
    interpreter(input3, "static")
    result1 = opPop()
    clearStacks()
    print("\nDynamic")
    interpreter(input3, "dynamic")
    result2 = opPop()
    if result1 == 10 and result2 == 40:
        isSuccessful = True
    clearStacks()
    return isSuccessful

def test4():
    print("\n***** Test 4 *****")
    isSuccessful = False
    print("Static")
    interpreter(input4, "static")
    result1 = opPop()
    clearStacks()
    print("\nDynamic")
    interpreter(input4, "dynamic")
    result2 = opPop()
    if result1 == 4 and result2 == 22:
        isSuccessful = True
    clearStacks()
    return isSuccessful

def test5():
    print("\n***** Test 5 *****")
    isSuccessful = False
    print("Static")
    interpreter(input5, "static")
    result1 = opPop()
    clearStacks()
    print("\nDynamic")
    interpreter(input5, "dynamic")
    result2 = opPop()
    if result1 == 60 and result2 == 48:
        isSuccessful = True
    clearStacks()
    return isSuccessful



def testInput():
    testCases = [('test1', test1), ('test2', test2), ('test3', test3), ('test4', test4), ('test5', test5)]
    # add you test functions to this list along with suitable names
    failedTests = [testName for (testName, testProc) in testCases if not testProc()]
    if failedTests:
        return ('Some Tests Failed', failedTests)
    else:
        return ('All Tests Succeeded!')


if __name__ == '__main__':
    result = testInput()
    print("\n\n***** Overall Test Results *****")
    print(result)
    print("********************************")








