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
dictstack = [{}]


# Pops values from the top of the stack (end of the list)
def dictPop():
    try:
        dictstack.pop()
    except:
        pass


# Pushes values onto the top of the stack (end of the list)
def dictPush(val={}):
    if isinstance(val, dict):
        size = len(dictstack) - 1
        dictstack[size].update(val)


def dictClear():
    dictstack.clear()
    dictstack.append({})

''' dictPush pushes a new dictionary to the dictstack. Note that, your interpreter
   will call dictPush only when Postscript “begin” operator is called. “begin”
   should pop the empty dictionary from the opstack and push it onto the dictstack
   by calling dictPush. You may either pass this dictionary (which you popped from
   opstack) to dictPush as a parameter or just simply push a new empty dictionary in dictPush.'''


# add name:value to the top dictionary in the dictionary stack.
def define(name, value):
    if isinstance(name, str):
        name = name.replace("/", "")
        dictPush({name: value})


# return the value associated with name or None if key is not found
def lookup(name):
    size = len(dictstack)
    for i in range(size):
        top = dictstack[size-i-1]
        if top.get(name, None) != None:
            value = top[name]
            if isinstance(value, list):
                functCheck = [type(i) for i in value]
                if functCheck.count(int) == len(functCheck) or functCheck.count(float) == len(functCheck):
                    opPush(top[name])
                    return
                else:
                    codearray = iter(value)
                    interpretSPS(codearray)
                    return
            else:
                opPush(value)
                return


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
    size = len(opstack)
    for i in range(size):
        print(opstack[size-1-i])


# --------------------------- 20% -------------------------------------
# Dictionary manipulation operators: psDict, begin, end, psDef
def psDict():
    num = opPop()
    newDict = dict()
    for i in range(num):
        newDict[i] = None
    opPush(newDict)


# Takes a dictionary from the top of the operand stack and pushes it on the dictionary stack.
def begin():
    val = opPop()
    if isinstance(val, dict):
        dictstack.append(val)


# Pop the top dictionary from the dictionary stack and throw it away
def end():
    dictPop()


# always creates or modifies a dictionary entry in the top most dictionary on the dictionary stack
# Pops the name and value from operand stack and call the “define” function.
def psDef():
    value = opPop()
    name = opPop()
    define(name, value)


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
    "dict": psDict,
    "begin": begin,
    "end": end,
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


# Write the necessary code here; again write
# auxiliary functions if you need them. This will probably be the largest
# function of the whole project, but it will have a very regular and obvious
# structure if you've followed the plan of the assignment.
#
def interpretSPS(code): # code is a code array
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
                lookup(item)
        elif isinstance(item, list) or isinstance(item, (int, float, complex)) or isinstance(item, bool):
            opPush(item)
        return interpretSPS(code)
    except StopIteration:
        return None


def interpreter(s): # s is a string
    val = parse(tokenize(s))
    val = iter(val)
    interpretSPS(val)


# Test Inputs
input1 = """
  /square {dup mul} def  
  [1 2 3 4] {square} forall 
  add add add 30 eq true 
  stack
"""


input2 = """ 
  [1 2 3 4 5] dup length /n exch def
  /fact {
      0 dict begin
         /n exch def
         n 2 lt
         { 1}
         {n 1 sub fact n mul }
         ifelse
      end 
  } def
  n fact stack    
"""


input3 = """
  [9 9 8 4 10] {dup 5 lt {pop} if}  forall 
  stack 
"""

input4 = """
  [1 2 3 4 5] dup length exch {dup mul}  forall
  add add add add
  exch 0 exch -1 1 {dup mul add} for
  eq stack 
"""

input5 = """
    /n 5 def
    n /factorial {
        dup 0 eq 
        {pop 1}
        {dup 1 sub factorial mul} 
        ifelse
    } def factorial stack
"""


input6 = """
    5 6
    /max {
        /num1 exch def
        /num2 exch def
        num1 num2 gt
        {num1} if
        num1 num2 lt
        {num2} if
     } def max stack
"""

def test1():
    isSuccessful = False
    print("\n***** Input1 Test Results *****")
    print("- OpStack -")
    interpreter(input1)
    print("- DictStack -")
    print(dictstack)
    if (opstack == [True, True]
        and dictstack == [{'square': ['dup', 'mul']}]):
        isSuccessful = True
    clear()
    dictClear()
    return isSuccessful


def test2():
    isSuccessful = False
    print("\n***** Input2 Test Results *****")
    print("- OpStack -")
    interpreter(input2)
    print("- DictStack -")
    print(dictstack)
    if (opstack == [[1, 2, 3, 4, 5], 120]
        and dictstack == [{'n': 5, 'fact': [0, 'dict', 'begin', '/n', 'exch', 'def', 'n', 2, 'lt', [1], ['n', 1, 'sub', 'fact', 'n', 'mul'], 'ifelse', 'end']}]):
        isSuccessful = True
    clear()
    dictClear()
    return isSuccessful


def test3():
    isSuccessful = False
    print("\n***** Input3 Test Results *****")
    print("- OpStack -")
    interpreter(input3)
    print("- DictStack -")
    print(dictstack)
    if (opstack == [9, 9, 8, 10]
        and dictstack == [{}]):
        isSuccessful = True
    clear()
    dictClear()
    return isSuccessful

def test4():
    isSuccessful = False
    print("\n***** Input4 Test Results *****")
    print("- OpStack -")
    interpreter(input4)
    print("- DictStack -")
    print(dictstack)
    if (opstack == [True]
        and dictstack == [{}]):
        isSuccessful = True
    clear()
    dictClear()
    return isSuccessful

def test5():
    isSuccessful = False
    print("\n***** Input5 Test Results *****")
    print("- OpStack -")
    interpreter(input5)
    print("- DictStack -")
    print(dictstack)
    if (opstack == [120]
        and dictstack == [{'n': 5, 'factorial': ['dup', 0, 'eq', ['pop', 1], ['dup', 1, 'sub', 'factorial', 'mul'], 'ifelse']}]):
        isSuccessful = True
    clear()
    dictClear()
    return isSuccessful

def test6():
    isSuccessful = False
    print("\n***** Input6 Test Results *****")
    print("- OpStack -")
    interpreter(input6)
    print("- DictStack -")
    print(dictstack)
    if (opstack == [6]
        and dictstack == [{'max': ['/num1', 'exch', 'def', '/num2', 'exch', 'def', 'num1', 'num2', 'gt', ['num1'], 'if', 'num1', 'num2', 'lt', ['num2'], 'if'], 'num1': 6, 'num2': 5}]):
        isSuccessful = True
    clear()
    dictClear()
    return isSuccessful


def testInput():
    testCases = [('test1', test1), ('test2', test2), ('test3', test3),
                 ('test4', test4), ('test5', test5), ('test6', test6)]
    # add you test functions to this list along with suitable names
    failedTests = [testName for (testName, testProc) in testCases if not testProc()]
    if failedTests:
        return ('Some Part-2 Tests Failed', failedTests)
    else:
        return ('All Part-2 Tests Succeeded!')

if __name__ == '__main__':
    result = testInput()
    print("\n\n***** Overall Test Results *****")
    print(result)
    print("********************************")





