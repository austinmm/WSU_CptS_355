import random
# Problem 1a
def addDict(d):
    result = dict()
    for daysDict in d.values():
        for day in daysDict:
            if day in result:
                result[day] += daysDict[day]
            else:
                result[day] = daysDict[day]
    return result


# Problem 1a Test Function
def testaddDict():
    test1 = {'355': {'Mon': 3, 'Wed': 2, 'Sat': 2},
             '360': {'Mon': 3, 'Tue': 2, 'Wed': 2, 'Fri': 10},
             '321': {'Tue': 2, 'Wed': 2, 'Thu': 3},
             '322': {'Tue': 1, 'Thu': 5, 'Sat': 2},
             '317': {'Tue': 3, 'Fri': 2, 'Sat': 2, 'Sun': 4}}
    result1 = addDict(test1)
    expected1 = {'Mon': 6, 'Wed': 6, 'Sat': 6, 'Tue': 8, 'Fri': 12, 'Thu': 8, 'Sun': 4}
    bool1 = result1 == expected1

    test2 = {'122': {'Tue': 3, 'Fri': 2, 'Sat': 2, 'Sun': 4},
             '260': {'Mon': 3, 'Tue': 2, 'Wed': 2, 'Fri': 10},
             '317': {'Thu': 2, 'Fri': 2, 'Sat': 3, 'Sun': 1},
             '355': {'Mon': 1, 'Thu': 5, 'Sat': 2}}
    result2 = addDict(test2)
    expected2 = {'Tue': 5, 'Fri': 14, 'Sat': 7, 'Sun': 5, 'Mon': 4, 'Wed': 2, 'Thu': 7}
    bool2 = result2 == expected2

    return bool1 and bool2


# Problem: 1b
def addDictN(L):
    return combineDict(list(map(addDict, L)))


# Problem 1b Helper Function
def combineDict(dlist):
    result = dict()
    for values in dlist:
        for day, hours in values.items():
            if day in result:
                result[day] += hours
            else:
                result[day] = hours
    return result


# Problem 1b Test Function
def testaddDictN():
    test1 = [{'355': {'Mon': 3, 'Wed': 2, 'Sat': 2},
              '360': {'Mon': 3, 'Tue': 2, 'Wed': 2, 'Fri': 10},
              '321': {'Tue': 2, 'Wed': 2, 'Thu': 3}},
             {'322': {'Tue': 1, 'Thu': 5, 'Sat': 2},
              '317': {'Tue': 3, 'Fri': 2, 'Sat': 2, 'Sun': 4}}]
    result1 = addDictN(test1)
    expected1 = {'Mon': 6, 'Wed': 6, 'Sat': 6, 'Tue': 8, 'Fri': 12, 'Thu': 8, 'Sun': 4}
    bool1 = result1 == expected1

    test2 = [{'355': {'Mon': 3, 'Wed': 2, 'Sat': 2},
              '360': {'Mon': 3, 'Tue': 2, 'Wed': 2, 'Fri': 10},
              '321': {'Tue': 2, 'Wed': 2, 'Thu': 3},
              '322': {'Tue': 1, 'Thu': 5, 'Sat': 2}},
             {'322': {'Mon': 2}, '360': {'Thu': 2, 'Fri': 5}, '321': {'Mon': 1, 'Sat': 3}},
             {'355': {'Sun': 8}, '360': {'Fri': 5}, '321': {'Mon': 4}, '322': {'Sat': 3}}]
    result2 = addDictN(test2)
    expected2 = {'Mon': 13, 'Wed': 6, 'Sat': 10, 'Tue': 5, 'Fri': 20, 'Thu': 10, 'Sun': 8}
    bool2 = result2 == expected2

    return bool1 and bool2


# Problem: 2a
def lookupVal(L, k):
    # L: List of Dictionaries
    # k: Key
    size = len(L)
    # end of list
    index = size - 1
    # Checks each dictionary in L, starting from the end of the list
    for i in range(size):
        dictionary = L[index]
        for x, y in dictionary.items():
            # If k appears in a dictionary, lookupVal returns the value for key k.
            if x == k:
                return y
            else:
                continue
        index -=1
    return None


# Problem 2a Test Function
def testlookupVal():
    test1 = [ {'Mon': 3, 'Wed': 2, 'Sat': 2},
              {'Mon': 3, 'Tue': 2, 'Wed': 2, 'Fri': 10},
              {'Tue': 2, 'Wed': 2, 'Thu': 3},
              {'Tue': 1, 'Thu': 5, 'Sat': 2},
              {'Tue': 3, 'Fri': 2, 'Sat': 2, 'Sun': 4}]
    result1 = lookupVal(test1, 'Mon')
    expected1 = 3
    bool1 = result1 == expected1

    test2 = [ {'Mon': 3, 'Wed': 2, 'Sat': 2},
              {'Mon': 3, 'Tue': 2, 'Wed': 2, 'Fri': 10},
              {'Tue': 2, 'Wed': 2, 'Thu': 3},
              {'Tue': 1, 'Thu': 5, 'Sat': 2},
              {'Mon': 2, 'Thu': 2, 'Fri': 5},
              {'Mon': 1, 'Sat': 3, 'Sun': 8},
              {'Mon': 4, 'Fri': 5, 'Sat': 3}]
    result2 = lookupVal(test2, 'Tue')
    expected2 = 1
    bool2 = result2 == expected2

    return bool1 and bool2


# Problem: 2b
def lookupVal2(tL, k):
    # tL: List of tuples
    # k: key
    # Each tuple in the input list includes an integer index value and a dictionary
    # The index in each tuple represent a link to another tuple in the list
    size = len(tL)
    currIndex = size-1
    while True:
        tupl = tL[currIndex]
        nextIndex = tupl[0]
        dictionary = tupl[1]
        for x,y in dictionary.items():
            if x == k:
                return y
            else:
                continue
        if currIndex == nextIndex:
            break
        else:
            currIndex = nextIndex
    return None


# Problem 2b Test Function
def testlookupVal2():
    test1 = [ (0, {'Mon': 3, 'Wed': 2, 'Sat': 2}),
              (0, {'Mon': 3, 'Tue': 2, 'Wed': 2, 'Fri': 10}),
              (3, {'Tue': 2, 'Wed': 2, 'Thu': 3}),
              (1, {'Tue': 1, 'Thu': 5, 'Sat': 2}),
              (2, {'Tue': 3, 'Fri': 2, 'Sat': 2, 'Sun': 4})]
    result1 = lookupVal2(test1, 'Mon')
    expected1 = 3
    bool1 = result1 == expected1

    test2 = [ (0, {'Mon': 3, 'Wed': 2, 'Sat': 2}),
              (3, {'Mon': 3, 'Tue': 2, 'Wed': 2, 'Fri': 10}),
              (4, {'Tue': 2, 'Wed': 2, 'Thu': 3}),
              (0, {'Tue': 1, 'Thu': 5, 'Sat': 2}),
              (3, {'Mon': 2, 'Thu': 2, 'Fri': 5}),
              (1, {'Mon': 1, 'Sat': 3, 'Sun': 8}),
              (2, {'Mon': 4, 'Fri': 5, 'Sat': 3})]
    result2 = lookupVal2(test2, 'Tue')
    expected2 = 2
    bool2 = result2 == expected2

    return bool1 and bool2


# Problem: 3
def numPaths(m, n, blocks):
    # m: grid length (rows)
    # n: grid width (columns)
    # blocks: list of the blocked cells
    # returns: returns the number of different paths the robot can take from the start to the end
    # The robot starts at the top left corner, (0,0), and is supposed to reach to the bottom right corner: (m-1,n-1)
    # Some of the cells in the grid are blocked and the robot is not allowed to visit those cells
    newBlock = []
    for block in blocks:
        tple = (block[0] - 1, block[1] - 1)
        newBlock.append(tple)

    return findPath(0, 0, (m,n), newBlock)


# Problem: 3 Helper Function
def findPath(row, col, finish, blocks):
    path1 = 0
    path2 = 0
    # Base Case
    currState = (row, col)
    if (currState[0] == finish[0]-1) and (currState[1] == finish[1]-1):
        return 1
    # able to move down
    downPath = (row + 1, col)
    if (downPath[0] < finish[0]) and (downPath not in blocks):
        path1 = findPath(row + 1, col, finish, blocks)
    # able to move right
    rightPath = (row, col + 1)
    if (rightPath[1] < finish[1]) and (rightPath not in blocks):
        path2 = findPath(row, col + 1, finish, blocks)

    return path1+path2


# Problem: 3 Test Function
def testnumPaths():
    result1 = numPaths(10, 5, [(0, 2), (1, 3), (4, 1)])
    expected1 = 450
    bool1 = result1 == expected1

    result2 = numPaths(2, 7, [(1, 1), (0, 6), (0, 4)])
    expected2 = 7
    bool2 = result2 == expected2

    return bool1 and bool2


# Problem: 4
def palindromes(strs):
    # strs: strsing
    # returns a list of the unique palindromes that appear in the input strsing
    strsings = createstrsList(strs)
    strsings = removeDuplicates(strsings)
    result = []
    for index in range(len(strsings)):
        strs = strsings[index]
        revstrs = strs[::-1]
        if strs == revstrs:
            result.append(strs)
        else:
            continue
    return result


# Problem: 4 Helper Function
def createstrsList(strs):
    length = len(strs)
    strsings = []
    for i in range(length):
        newstrs = strs[i:]
        first = newstrs[0]
        sub = ""
        for char in newstrs[1:]:
            sub += char
            strsings.append(first + sub)
    return strsings


# Problem: 4 Helper Function
def removeDuplicates(strsings):
    newList = []
    for strs in strsings:
        if strs not in newList:
            newList.append(strs)
    return newList

# Problem: 4 Test Function
def testpalindromes():
    test1 = "ascasbbaccacsa"
    result1 = palindromes(test1)
    expected1 = ['bb', 'acca', 'cc', 'cac']
    bool1 = result1 == expected1

    test2 = "annahasacookie"
    result2 = palindromes(test2)
    expected2 = ['anna', 'nn', 'aha', 'asa', 'oo']
    bool2 = result2 == expected2

    return bool1 and bool2


# Problem: 5a
class iterApply():
    Max = None

    def __init__(self, n, f):
        self.f = f
        self.n = n

    def __iter__(self):
        self.n = 1
        return self

    def __next__(self):
        result = self.f(self.n)
        self.n += 1
        return result

    def __prev__(self):
        self.n -= 1
        result = self.f(self.n)
        return result


# Problem: 5b
def iMerge(iNumbers1, iNumbers2, N):
    # iNumbers1: iterable value (sorted sequences of increasing numbers)
    # iNumbers2: iterable value (sorted sequences of increasing numbers)
    # returns: merges the two input sequences and returns the first N elements from the merged sequence
    List1 = []
    List2 = []
    if iterApply.Max != None:
        num1 = iNumbers1.f(iNumbers1.n)
        num2 = iNumbers2.f(iNumbers2.n)
        while num1 > iterApply.Max:
            num1 = iNumbers1.__prev__()
        while num2 > iterApply.Max:
            num2 = iNumbers2.__prev__()
        iNumbers1.__next__()
        iNumbers2.__next__()
    for i in range(N):
        List1.append(iNumbers1.__next__())
        List2.append(iNumbers2.__next__())
    List1 += List2
    List1.sort()
    List = []
    for i in range(N):
        List.append(List1[i])
    iterApply.Max = List[-1]
    return List


class Stream(object):
    def __init__(self, first, compute_rest, empty=False):
        self.first = first
        self._compute_rest = compute_rest
        self.empty = empty
        self._rest = None
        self._computed = False

    @property
    def rest(self):
        assert not self.empty, 'Empty streams have no rest.'
        if not self._computed:
            self._rest = self._compute_rest()
            self._computed = True
        return self._rest


# Problem: 6a
def streamRandoms(k, min, max):
    # creates an infinite stream of positive random integers starting at k
    # The values in the stream should be randomly generated
    # Each value should be between min and max argument values (inclusive)
    def compute_rest():
        rand = random.randint(min, max)
        return streamRandoms(rand, min, max)
    return Stream(k, compute_rest)


# Problem: 6b
def oddStream(stream):
    if stream.empty:
        return stream

    def compute_rest():
        return oddStream(stream.rest)

    while stream.first % 2 == 0:
        stream = stream.rest
    return Stream(stream.first, compute_rest)


if __name__ == '__main__':
    passedMsg = "%s passed"
    failedMsg = "%s failed"

    if testaddDict():
        print(passedMsg % 'addDict')
    else:
        print(failedMsg % 'addDict')

    if testaddDictN():
        print(passedMsg % 'addDictN')
    else:
        print(failedMsg % 'addDictN')

    if testlookupVal():
        print(passedMsg % 'lookupVal')
    else:
        print(failedMsg % 'lookupVal')

    if testlookupVal2():
        print(passedMsg % 'lookupVal2')
    else:
        print(failedMsg % 'lookupVal2')

    if testnumPaths():
        print(passedMsg % 'numPaths')
    else:
        print(failedMsg % 'numPaths')

    if testpalindromes():
        print(passedMsg % 'palindromes')
    else:
        print(failedMsg % 'palindromes')
