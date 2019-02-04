
(*Provided Helper Commands/Functions*)
Control.Print.printDepth := 100;
fun map f [] = []
    | map f (x::rest) = (f x)::(map f rest);
(*val map = fn: ('a -> 'b) -> 'a list -> 'b list*)

fun fold f base [] = base
    | fold f base (x::rest) = f x (fold f base rest);
(*val fold = fn: ('a -> 'b -> 'b) -> 'b -> 'a list -> 'b*)

fun filter pred [] = []
    | filter pred (x::rest) = if pred x then x::(filter pred rest)
      else (filter pred rest);
(*val filter = fn: ('a -> bool) -> 'a list -> 'a list*)

(****************************************)
(*Problem 1: numbersToSum*)
fun numbersToSum sum [] = []
  | numbersToSum sum (L::rest) =
    let
      val currSum = sum - L
    in
      if currSum > 0 then [L]@numbersToSum currSum rest
      else []
    end;

(*Problem 1: numbersToSumTail*)
fun numbersToSumTail sum [] = []
  | numbersToSumTail sum (L::rest) =
    let
      val currSum = sum - L
    in
      if currSum <= 0 then []
      else [L]@numbersToSum currSum rest
    end;

(****************************************)
(*Problem 2: partition*)
fun partition funct [] = ([],[])
  | partition funct (L::rest) =
    let
      (*Helper Function*)
      fun combineTuples ((L1, L2),(L3, L4)) = (L1@L3, L2@L4);
      val isTrue = funct L
    in
      if isTrue = true then combineTuples(([L], []), partition funct rest)
      else combineTuples(([], [L]), partition funct rest)
    end;

(****************************************)
(*Problem 3: areAllUnique*)
fun areAllUnique [] = true
  | areAllUnique L =
  let
    fun countInList [] n = 0
    	| countInList (L::rest) n =
    	if n = L then 1 + countInList rest n
    	else countInList rest n;
    fun addup a b = a + b;
    val counts = map (fn y => countInList L y) L
    val len = length L
    val result = fold addup 0 counts
  in
    if len = result then true
    else false
  end;

(****************************************)
(*Problem 4: sum*)
fun sum [[]] = 0
  | sum [] = 0
  | sum L =
  let
    fun combineList x y = x@y;
    fun addup a b = a + b;
    val oneList = fold combineList [] L
    val result = fold addup 0 oneList
  in
    result
  end;

(*Problem 4: sumOption*)
fun sumOption [[]] = NONE
  | sumOption [] = NONE
  | sumOption L =
  let
    fun combineList x y = x@y;
    fun addup NONE NONE = NONE
    | addup a NONE = a
    | addup NONE b = b
    | addup a b = SOME(valOf a + valOf b);
    val oneList = fold combineList [] L
    val result = fold addup NONE oneList
  in
    result
  end;

(*Problem 4: sumEither*)
datatype either = IString of string | IInt of int;
fun sumEither [[]] = IInt 0
  | sumEither [] = IInt 0
  | sumEither L =
  let
    fun combineList x y = x@y;
    fun str2int s = valOf(Int.fromString(s));
    fun typeCheck x =
      case x of IInt x => x
      | IString x => str2int x;
    fun addup a b =
    let
      val aVal = typeCheck a
      val bVal = typeCheck b
      val sum = IInt (aVal + bVal)
    in
      sum
    end;
    val default = IInt 0
    val oneList = fold combineList [] L
    val result = fold addup default oneList
  in
    result
  end;

(****************************************)
(*Problem 5: depthScan*)
datatype 'a Tree = LEAF of 'a | NODE of 'a * ('a Tree) * ('a Tree);
fun depthScan (LEAF(v)) = [v]
  |depthScan (NODE(v, left, right)) =
    (depthScan left)@(depthScan right)@[v];

(*Problem 5: depthSearch*)
val myT = NODE(6, NODE (1, NODE(9, LEAF 10 ,LEAF 5),LEAF 2), NODE(1,LEAF 8,LEAF 5));
fun depthSearch node key =
  let
    fun findVal (LEAF(v)) key depth =
      if v = key then depth
      else ~1
    | findVal (NODE(v, left, right)) key depth =
      let
        val lResult = findVal left key (1+depth)
        val rResult = findVal right key (1+depth)
      in
        if (lResult <> ~1) andalso (lResult > rResult) then lResult
        else if (rResult <> ~1) andalso (rResult > lResult) then rResult
        else if v = key then depth
        else ~1
      end;
  in
    findVal node key 1
  end;

(*Problem 5: addTrees*)
val T1 = NODE(1, NODE (2, NODE(3, LEAF 4 ,LEAF 5),LEAF 6), NODE(7,LEAF 8,LEAF 9));
val T2 = NODE(1, NODE (2, LEAF 3, LEAF 6), NODE(7, NODE(8, LEAF 10 ,LEAF 11),LEAF 9));
fun addTrees (LEAF(v)) (LEAF(z)) =
    LEAF(v+z)
  |addTrees (LEAF(v)) (NODE(z, left2, right2)) =
    NODE(v+z, (addTrees left2 (LEAF 0)), (addTrees right2 (LEAF 0)))
  |addTrees (NODE(v, left1, right1)) (LEAF(z)) =
    NODE(v+z, (addTrees left1 (LEAF 0)), (addTrees right1 (LEAF 0)))
  |addTrees (NODE(v, left1, right1)) (NODE(z, left2, right2)) =
    NODE(v+z, (addTrees left1 left2), (addTrees right1 right2));

(**********Test-Functions**********)
(*Test Function: depthScan*)
fun depthScanTest () =
	let
    (*Helper Functions*)
    fun printIntList L = String.concatWith ", " (map Int.toString L);
    fun printStrList L = String.concatWith ", " L;
    val tree1 = NODE(5, NODE(1, NODE(2, NODE(20, LEAF 5, NODE(9, LEAF 22, LEAF 89)), NODE(11, LEAF 67, LEAF 89)), LEAF 7), LEAF 99)
    val tree2 = NODE(5, NODE(1, NODE(2, NODE(20, LEAF 5, LEAF 33), LEAF 21), LEAF 79), NODE(34, LEAF 87, NODE(23, LEAF 66, NODE(71, LEAF 55, LEAF 44))))
    val tree3 = NODE("5", NODE("1", NODE("2", NODE("20", LEAF "5", LEAF "33"), LEAF "21"), LEAF "79"), NODE("34", LEAF "87", NODE("23", LEAF "66", NODE("71", LEAF "55", LEAF "44"))))
    val test1 = depthScan tree1
    val bool1 = test1 = [5,22,89,9,20,67,89,11,2,7,1,99,5]
    val test2 = depthScan tree2
    val bool2 = test2 = [5,33,20,21,2,79,1,87,66,55,44,71,23,34,5]
    val test3 = depthScan tree3
    val bool3 = test3 = ["5","33","20","21","2","79","1","87","66","55","44","71","23","34","5"]
  in
		print("*** depthScan Test Results ***\n" ^
    	"Test1: " ^ printIntList test1 ^ " => " ^ Bool.toString(bool1) ^ "\n" ^
    	"Test2: " ^ printIntList test2 ^ " => " ^ Bool.toString(bool2) ^ "\n" ^
      "Test3: " ^ printStrList test3 ^ " => " ^ Bool.toString(bool3) ^ "\n")
end;
val _ = depthScanTest ();

(****************************************)
(*Test Function: depthSearch*)
fun depthSearchTest () =
	let
    val tree1 = NODE(5, NODE(1, NODE(2, NODE(20, LEAF 5, NODE(9, LEAF 22, LEAF 89)), NODE(11, LEAF 67, LEAF 89)), LEAF 7), LEAF 99)
    val tree2 = NODE(5, NODE(1, NODE(2, NODE(20, LEAF 5, LEAF 33), LEAF 21), LEAF 79), NODE(34, LEAF 87, NODE(23, LEAF 66, NODE(71, LEAF 55, LEAF 44))))
    val tree3 = NODE("5", NODE("1", NODE("2", NODE("20", LEAF "5", LEAF "33"), LEAF "21"), LEAF "79"), NODE("34", LEAF "87", NODE("23", LEAF "66", NODE("71", LEAF "55", LEAF "44"))))
    val test1 = depthSearch tree1 5
    val bool1 = test1 = 5
    val test2 = depthSearch tree2 17
    val bool2 = test2 = ~1
    val test3 = depthSearch tree3 "87"
    val bool3 = test3 = 3
  in
		print("*** depthSearch Test Results ***\n" ^
    	"Test1: " ^ Int.toString(test1) ^ " => " ^ Bool.toString(bool1) ^ "\n" ^
    	"Test2: " ^ Int.toString(test2) ^ " => " ^ Bool.toString(bool2) ^ "\n" ^
      "Test3: " ^ Int.toString(test3) ^ " => " ^ Bool.toString(bool3) ^ "\n")
end;
val _ = depthSearchTest ();

(****************************************)
(*Test Function: addTrees*)
fun addTreesTest () =
	let
    val tree1 = NODE(5, NODE(1, NODE(2, NODE(20, LEAF 5, NODE(9, LEAF 22, LEAF 89)), NODE(11, LEAF 67, LEAF 89)), LEAF 7), LEAF 99)
    val tree2 = NODE(5, NODE(1, NODE(2, NODE(20, LEAF 5, LEAF 33), LEAF 21), LEAF 79), NODE(34, LEAF 87, NODE(23, LEAF 66, NODE(71, LEAF 55, LEAF 44))))
    val tree3 = NODE(21, NODE(11, NODE(~5, NODE(~78, LEAF 77, LEAF 37), LEAF 22), LEAF ~81), NODE(76, LEAF ~3, NODE(23, LEAF 45, NODE(96, LEAF ~51, LEAF 48))))
    val test1 = addTrees tree1 tree2
    val bool1 = test1 = NODE(10,NODE(2,NODE(4,NODE (40,LEAF 10,NODE (42,LEAF 22,LEAF 89)),NODE (32,LEAF 67,LEAF 89)),LEAF 86),NODE (133,LEAF 87,NODE (23,LEAF 66,NODE (71,LEAF 55,LEAF 44))))
    val test2 = addTrees tree2 tree3
    val bool2 = test2 = NODE(26,NODE (12,NODE (~3,NODE (~58,LEAF 82,LEAF 70),LEAF 43),LEAF ~2),NODE (110,LEAF 84,NODE (46,LEAF 111,NODE (167,LEAF 4,LEAF 92))))
    val test3 = addTrees tree3 tree1
    val bool3 = test3 = NODE(26,NODE(12,NODE(~3,NODE (~58,LEAF 82,NODE (46,LEAF 22,LEAF 89)),NODE (33,LEAF 67,LEAF 89)),LEAF ~74),NODE (175,LEAF ~3,NODE (23,LEAF 45,NODE (96,LEAF ~51,LEAF 48))))
  in
		print("*** addTrees Test Results ***\n" ^
    	"Test1: " ^ Bool.toString(bool1) ^ "\n" ^
    	"Test2: " ^ Bool.toString(bool2) ^ "\n" ^
      "Test3: " ^ Bool.toString(bool3) ^ "\n")
end;
val _ = addTreesTest ();

(****************************************)
(*Test Function: numbersToSum*)
fun numbersToSumTest () =
	let
    (*Helper Function*)
    fun printIntList L = String.concatWith ", " (map Int.toString L);
    val test1 = numbersToSum 200 [100,10,33,67,200,1]
    val bool1 = test1 = [100,10,33]
    val test2 = numbersToSum 41 [4,3,5,22,7,26,99]
    val bool2 = test2 = [4,3,5,22]
    val test3 = numbersToSum 30 [1,~22,40,7,~8,21,7]
    val bool3 = test3 = [1,~22,40,7,~8]
  in
  print("*** numbersToSum Test Results ***\n" ^
    "Test1: " ^ printIntList test1 ^ " => " ^ Bool.toString(bool1) ^ "\n" ^
    "Test2: " ^ printIntList test2 ^ " => " ^ Bool.toString(bool2) ^ "\n" ^
    "Test3: " ^ printIntList test3 ^ " => " ^ Bool.toString(bool3) ^ "\n")
end;
val _ = numbersToSumTest ();

(****************************************)
(*Test Function: partition*)
fun partitionTest () =
	let
    val test1 = partition (fn x => (x<=34)) [100,10,33,67,200,1]
    val bool1 = test1 = ([10,33,1],[100,67,200])
    val test2 = partition null [[1,2],[1],[],[5],[],[6,7,8]]
    val bool2 = test2 = ([[],[]],[[1,2],[1],[5],[6,7,8]])
    val test3 = partition (fn x => (x < 0)) [1,~22,40,7,~8,21,7]
    val bool3 = test3 = ([~22,~8],[1,40,7,21,7])
  in
  print("*** partition Test Results ***\n" ^
    "Test1: " ^ Bool.toString(bool1) ^ "\n" ^
    "Test2: " ^ Bool.toString(bool2) ^ "\n" ^
    "Test3: " ^ Bool.toString(bool3) ^ "\n")
end;
val _ = partitionTest ();

(****************************************)
(*Test Function: areAllUnique*)
fun areAllUniqueTest () =
	let
    val test1 = areAllUnique [100,10,33,67,200,33]
    val bool1 = test1 = false
    val test2 = areAllUnique [[1,2],[1],[],[5],[6,7,8]]
    val bool2 = test2 = true
    val test3 = areAllUnique ["1","22","40","7","8","21","70"]
    val bool3 = test3 = true
  in
  print("*** areAllUnique Test Results ***\n" ^
    "Test1: " ^ Bool.toString(test1) ^ " => " ^ Bool.toString(bool1) ^ "\n" ^
    "Test2: " ^ Bool.toString(test2) ^ " => " ^ Bool.toString(bool2) ^ "\n" ^
    "Test3: " ^ Bool.toString(test3) ^ " => " ^ Bool.toString(bool3) ^ "\n")
end;
val _ = areAllUniqueTest ();

(****************************************)
(*Test Function: sum*)
fun sumTest () =
	let
    val test1 = sum [[100,10,33],[67,200,33]]
    val bool1 = test1 = 443
    val test2 = sum [[1,2],[1],[],[5],[6,7,8]]
    val bool2 = test2 = 30
    val test3 = sum [[1,2,3,4],[5,6,7,8],[~1,~2,3,~7]]
    val bool3 = test3 = 29
  in
  print("*** sum Test Results ***\n" ^
    "Test1: " ^ Int.toString(test1) ^ " => " ^ Bool.toString(bool1) ^ "\n" ^
    "Test2: " ^ Int.toString(test2) ^ " => " ^ Bool.toString(bool2) ^ "\n" ^
    "Test3: " ^ Int.toString(test3) ^ " => " ^ Bool.toString(bool3) ^ "\n")
end;
val _ = sumTest ();

(****************************************)
(*Test Function: sumOption*)
fun sumOptionTest () =
	let
    val test1 = sumOption [[SOME(100),SOME(10),SOME(33)],[SOME(67),SOME(200),SOME(33)]]
    val bool1 = test1 = SOME(443)
    val test2 = sumOption [[SOME(1),SOME(2)],[SOME(1)],[],[SOME(5)],[SOME(6),SOME(7),SOME(8)]]
    val bool2 = test2 = SOME(30)
    val test3 = sumOption [[SOME(1),SOME(2),SOME(3),SOME(4)],[SOME(5),SOME(6),SOME(7),SOME(8)],[SOME(~1),SOME(~2),SOME(3),SOME(~7)]]
    val bool3 = test3 = SOME(29)
  in
  print("*** sumOption Test Results ***\n" ^
    "Test1: SOME " ^ Int.toString((valOf test1)) ^ " => " ^ Bool.toString(bool1) ^ "\n" ^
    "Test2: SOME " ^ Int.toString((valOf test2)) ^ " => " ^ Bool.toString(bool2) ^ "\n" ^
    "Test3: SOME " ^ Int.toString((valOf test3)) ^ " => " ^ Bool.toString(bool3) ^ "\n")
end;
val _ = sumOptionTest ();

(****************************************)
(*Test Function: sumEither*)
fun sumEitherTest () =
	let
    fun typeCheck x =
      case x of IInt x => x;
    val test1 = sumEither [[IString("100"),IInt(10),IString("33")],[IInt(67),IInt(200),IInt(33)]]
    val bool1 = test1 = IInt 443
    val test2 = sumEither [[IInt(1),IString("2")],[IInt(1)],[],[IString("5")],[IString("6"),IString("7"),IInt(8)]]
    val bool2 = test2 = IInt 30
    val test3 = sumEither [[IString("1"),IInt(2),IString("3"),IInt(4)],[IString("5"),IInt(6),IInt(7),IString("8")],[IString("~1"),IInt(~2),IInt(3),IString("~7")]]
    val bool3 = test3 = IInt 29
  in
  print("*** sumEither Test Results ***\n" ^
    "Test1: IInt " ^ Int.toString((typeCheck test1)) ^ " => " ^ Bool.toString(bool1) ^ "\n" ^
    "Test2: IInt " ^ Int.toString((typeCheck test2)) ^ " => " ^ Bool.toString(bool2) ^ "\n" ^
    "Test3: IInt " ^ Int.toString((typeCheck test3)) ^ " => " ^ Bool.toString(bool3) ^ "\n")
end;
val _ = sumEitherTest ();
