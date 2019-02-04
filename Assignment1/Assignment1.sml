(*Cpts 355 Homework One*)
(*Created By: Austin Marino*)


(*Problem 1: exists*)
fun exists(n, L) =
	if L = nil orelse L = [] then false
	else if n = hd(L) then true
	else exists(n, tl(L));

(*Problem 1: Part b
	Question: (''a * ''a list) -> bool VS ('a * 'a list) -> bool
	Answer: 'a means "any type", while ''a means "any type that can be compared for equality". ''a means that we are comparing two polymorphic types, meaning that their data type can be anything. 'a would mean that we are comparing two variables that can only ever be one type that is the same.
*)

(*Problem 1: countInList*)
fun countInList [] n = 0
	| countInList (L::rest) n =
	if n = L then 1 + countInList rest n
	else countInList rest n;

(****************************************)
(*Problem 2: listDiff*)
fun listDiff([], []) = []
	| listDiff([], b) = []
	| listDiff(a, []) = a
	| listDiff(a::rest, b) =
		let
			(*Helper Function*)
			fun removeElement(num, []) = []
			| removeElement(num, L::rest) =
			if num = L then rest
			else [L]@removeElement(num, rest);
		in
			if countInList b a = 0 then [a]@listDiff(rest, b)
			else []@listDiff(rest, removeElement(a, b))
	end;


(****************************************)
(*Problem 3: firstN*)
fun firstN [] n = []
	| firstN(L::rest) 0 = []
	| firstN(L::rest) n = [L]@firstN rest (n-1);


(****************************************)
(*Problem 4: buses val*)
val buses = [
("Lentil",["Chinook", "Orchard", "Valley", "Emerald","Providence", "Stadium", "Main", "Arbor", "Sunnyside", "Fountain", "Crestview", "Wheatland", "Walmart", "Bishop", "Derby", "Dilke"]), ("Wheat",["Chinook", "Orchard", "Valley", "Maple","Aspen", "TerreView", "Clay", "Dismores", "Martin", "Bishop", "Walmart", "PorchLight", "Campus"]),
("Silver",["TransferStation", "PorchLight", "Stadium", "Bishop","Walmart", "Shopco", "RockeyWay"]), ("Blue",["TransferStation", "State", "Larry", "TerreView","Grand", "TacoBell", "Chinook", "Library"]),
("Gray",["TransferStation", "Wawawai", "Main", "Sunnyside","Crestview", "CityHall", "Stadium", "Colorado"])
];

(*Problem 4: busFinder*)
fun busFinder stop [] = []
	| busFinder stop (busInfo::rest) =
		let
			(*Helper Functions*)
			fun first(a, _) = a;
			fun second(_, b) = b;
		in
			if exists(stop, (second busInfo)) = true then [first busInfo]@busFinder stop rest
			else []@busFinder stop rest
	end;

(*Problem 4: Part b
	Question: ''a -> ('b * ''a list) list -> 'b list VS ''a -> ('a * ''a list) list -> 'a list
	Answer: The reason the return type is 'b and not 'a is because we are creating a whole new list that will be returned instead of just returning the original list passed in. If that was the case, then the return type would be 'a.
*)



(****************************************)
(*Problem 5: parallelResistors*)
fun parallelResistors [] = 0.0
	| parallelResistors nums =
		let
			(*Helper Function*)
			fun resistorCalculations [] = 0.0
				| resistorCalculations (nums::rest) = (1.0/nums) + resistorCalculations rest;
		in
			1.0 / resistorCalculations nums
	end;


(****************************************)
(*Problem 6: pairNright*)
fun pairNright(num, []) =[[]]
	| pairNright(num, L) =
		let
			(*Helper Functions*)
			fun appendNValues(n, []) = []
				| appendNValues(0, L) = []
				| appendNValues(n, L::rest) = [L]@appendNValues(n-1, rest);
			fun removeNValues(n, []) = []
				| removeNValues(0, L) = L
				| removeNValues(n, L::rest) = removeNValues(n-1, rest);
			(*Helper Variables*)
		    val subL = appendNValues(num, L)
		    val newL = removeNValues(num, L)
		in
		    if length(subL) < num then [subL]
		    else [subL]@pairNright(num, newL)
	end;

(*Problem 6: pairNleft*)
fun pairNleft(num, []) =[[]]
	| pairNleft(num, L) =
		let
			(*Helper Functions*)
			fun compareValues(size, num) =
				let
		    		val result = size mod num
				in
		    		if result = 0 then num
		    		else result
			end;
			fun appendNValues(n, []) = []
				| appendNValues(0, L) = []
				| appendNValues(n, L::rest) = [L]@appendNValues(n-1, rest);
			fun removeNValues(n, []) = []
				| removeNValues(0, L) = L
				| removeNValues(n, L::rest) = removeNValues(n-1, rest);
			(*Helper Variables*)
		    val size = compareValues(length(L), num)
		    val subL = appendNValues(size, L)
		    val newL = removeNValues(size, L)
		in
		    if length(newL) = 0 then [subL]
		    else [subL]@pairNleft(num, newL)
	end;

(**********Test-Functions**********)

(*Test Function: exists*)
fun existsTest()=
	let
		val list1 = [1,2,3,4,5,0,4,3,2,1]
		val list2 = ["a","g","k","w","u"]
		val test1 = exists(4, list1)
		val test2 = exists("h", list2)
		val bool1 = test1 = true
		val bool2 = test2 = false
	in
		print("*** existsTest Test Results ***\n" ^
    	"Test1: " ^ Bool.toString(test1) ^ " => " ^ Bool.toString(bool1) ^ "\n" ^
    	"Test2: " ^ Bool.toString(test2) ^ " => " ^ Bool.toString(bool2) ^ "\n")
end;
val _ = existsTest();

(****************************************)
(*Test Function: countInList*)
fun countInListTest()=
	let
		val list1 = [1,2,3,4,5,0,4,3,2,1]
		val list2 = ["a","g","k","w","u", "u", "h", "u"]
		val test1 = countInList list1 4
		val test2 = countInList list2 "u"
		val bool1 = test1 = 2
		val bool2 = test2 = 3
	in
		print("*** countInListTest Test Results ***\n" ^
    	"Test1: " ^ Int.toString(test1) ^ " => " ^ Bool.toString(bool1) ^ "\n" ^
    	"Test2: " ^ Int.toString(test2) ^ " => " ^ Bool.toString(bool2) ^ "\n")
end;
val _ = countInListTest();

(****************************************)
(*Test Function: listDiff*)
fun listDiffTest()=
	let
		val list1 = [1,2,3,4,5,0,4,3,2,1]
		val list2 = [1,1,2,5,5,6,0,3]
		val list3 = ["a","g","k","w","u", "u", "h", "u"]
		val list4 = ["y","f","h","a","e", "w", "q", "n"]
		val test1 = listDiff(list1, list2)
		val test2 = listDiff(list3, list4)
		val bool1 = test1 = [4, 4, 3, 2]
		val bool2 = test2 = ["g", "k", "u", "u", "u"]
		(*Helper Functions*)
		fun printIntList L = String.concatWith ", " (map Int.toString L);
		fun printStrList L = String.concatWith ", " L;
	in
		print("*** listDiffTest Test Results ***\n" ^
    	"Test1: " ^ printIntList test1 ^ " => " ^ Bool.toString(bool1) ^ "\n" ^
    	"Test2: " ^ printStrList test2 ^ " => " ^ Bool.toString(bool2) ^ "\n")
end;
val _ = listDiffTest();

(****************************************)
(*Test Function: firstN*)
fun firstNTest()=
	let
		val list1 = [1,2,3,4,5,0,4,3,2,1]
		val list2 = ["y","f","h","a","e", "w", "q", "n"]
		val test1 = firstN list1 20
		val test2 = firstN list2 5
		val bool1 = test1 = [1, 2, 3, 4, 5, 0, 4, 3, 2, 1]
		val bool2 = test2 = ["y", "f", "h", "a", "e"]
		(*Helper Functions*)
		fun printIntList L = String.concatWith ", " (map Int.toString L);
		fun printStrList L = String.concatWith ", " L;
	in
		print("*** firstNTest Test Results ***\n" ^
    	"Test1: " ^ printIntList test1 ^ " => " ^ Bool.toString(bool1) ^ "\n" ^
    	"Test2: " ^ printStrList test2 ^ " => " ^ Bool.toString(bool2) ^ "\n")
end;
val _ = firstNTest();

(****************************************)
(*Test Function: busFinder*)
fun busFinderTest () =
	let
		val buses =
		     [("Lentil",["Chinook", "Orchard", "Valley", "Emerald","Providence", "Stadium",
		     "Main", "Arbor", "Sunnyside", "Fountain", "Crestview", "Wheatland", "Walmart",
		     "Bishop", "Derby", "Dilke"]),
		     ("Wheat",["Chinook", "Orchard", "Valley", "Maple","Aspen", "TerreView", "Clay",
		     "Dismores", "Martin", "Bishop", "Walmart", "PorchLight", "Campus"]),
		     ("Silver",["TransferStation", "PorchLight", "Stadium", "Bishop","Walmart",
		     "Shopco", "RockeyWay"]),
		     ("Blue",["TransferStation", "State", "Larry", "TerreView","Grand", "TacoBell",
		     "Chinook", "Library"]),
		     ("Gray",["TransferStation", "Wawawai", "Main", "Sunnyside","Crestview",
		     "CityHall", "Stadium", "Colorado"])]
			val busFinderT1 = ((busFinder "Walmart" buses) = ["Lentil","Wheat","Silver"]) val busFinderT2 = ((busFinder "Shopco" buses) = ["Silver"])
		val test1 = busFinder "Main" buses
		val test2 = busFinder "Chinook" buses
		val bool1 = test1 = ["Lentil", "Gray"]
		val bool2 = test2 = ["Lentil", "Wheat", "Blue"]
		(*Helper Function*)
		fun printStrList L = String.concatWith ", " L;
	in
		print("*** busFinderTest Test Results ***\n" ^
    	"Test1: " ^ printStrList test1 ^ " => " ^ Bool.toString(bool1) ^ "\n" ^
    	"Test2: " ^ printStrList test2 ^ " => " ^ Bool.toString(bool2) ^ "\n")
end;
val _ = busFinderTest();

(****************************************)
(*Test Function: parallelResistors*)
fun parallelResistorsTest()=
	let
		val list1 = [8.0, 8.0, 8.0, 8.0]
		val list2 = [4.0, 4.0, 2.0, 2.0, 2.0, 2.0]
		val test1 = parallelResistors list1
		val test2 = parallelResistors list2
		val bool1 = Real.==(test1, 2.0)
		val bool2 = Real.==(test2, 0.4)
	in
		print("*** parallelResistorsTest Test Results ***\n" ^
    	"Test1: " ^ Real.toString(test1) ^ " => " ^ Bool.toString(bool1) ^ "\n" ^
    	"Test2: " ^ Real.toString(test2) ^ " => " ^ Bool.toString(bool2) ^ "\n")
end;
val _ = parallelResistorsTest();

(****************************************)
(*Test Function: pairNright*)
fun pairNrightTest()=
	let
		val list1 = [1,2,3,4,5,0,4,3,2,1]
		val list2 = ["y","f","h","a","e", "w", "q", "n"]
		val test1 = pairNright(3, list1)
		val test2 = pairNright(5, list2)
		val bool1 = test1 = [[1, 2, 3], [4, 5, 0], [4, 3, 2], [1]]
		val bool2 = test2 = [["y","f","h","a","e"], ["w", "q", "n"]]
	in
		print("*** pairNrightTest Test Results ***\n" ^
    	"Test1: " ^ Bool.toString(bool1) ^ "\n" ^
    	"Test2: " ^ Bool.toString(bool2) ^ "\n")
end;
val _ = pairNrightTest();

(****************************************)
(*Test Function: pairNleft*)
fun pairNleftTest()=
	let
		val list1 = [1,2,3,4,5,0,4,3,2,1]
		val list2 = ["y","f","h","a","e", "w", "q", "n"]
		val test1 = pairNleft(3, list1)
		val test2 = pairNleft(5, list2)
		val bool1 = test1 = [[1], [2, 3, 4], [5, 0, 4], [3, 2, 1]]
		val bool2 = test2 = [["y","f","h"],["a","e","w", "q", "n"]]
	in
		print("*** pairNleftTest Test Results ***\n" ^
    	"Test1: " ^ Bool.toString(bool1) ^ "\n" ^
    	"Test2: " ^ Bool.toString(bool2) ^ "\n")
end;
val _ = pairNleftTest();
