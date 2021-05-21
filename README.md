

# Google Foobar Challenge
I received Google's Foobar challenge after searching for "C++ move semantics". This was strange to me, given that I've searched MANY
other programming things over the years, and lots of things that are vastly more complex than C++ move semantics, but Google's
algorithms are basically magic. Just for fun I accepted the challenge, and started.

# Level 1
I started, predictably, at Level 1, and I've already forgotten what the challenge was. It was trivially simple, and took me less
than 20 minutes. I quickly moved on to Level 2.

# Level 2
Level 2 required that I solve 2 problems instead of one, and they were more difficult than Level 1, well sorta.

## Gearing Up for Destruction
My first Level 2 problem took me a while. Unfortunately I didn't copy down the problem statement but it basically goes like this:

You have a series of pegs located at integer positions from 1 to 10000, and each peg will have a gear on it.
The goal is to determine the *radius* of the first gear such that it will be twice the radius of the final gear.

My initial solution was to use a backtracking algorithm to narrow down the possibilites, and it passed most of
the tests once I got a few rounding errors worked out. Unfortunately it didn't pass all the tests. After some 
consideration I knew there MUST be a way to mathematically calculate the value, and I was going to use a system
of equations (solved using Gaussian elimination) or maybe finding the meeting point of two lines. Then I decided
to search a little more and found a Stack Overflow post about it. I wasn't really sure if it counted as cheating,
so I decided not to read any answers directly but I did Ctrl+F for "line" to see if I was on the right track, which
I totally was, and before I closed out I noticed the text "y = mx + b", which was enough to cause my brain to switch
gears and make it a single line equation `y = 2mx + b` which, when solving for `x`, becomes `x = b / (0.5 - m)`.
Using this I was able to immediately calculate the mid point where the two lines crossed instead of iteratively
finding it using the backtracking solution that I'd originally implemented.

So I was done, right? Wrong. It still didn't pass the tests, in fact it was failing the EXACT same tests that my
original version was failing. What could be wrong??? The answer was fractions. I was using floats, and once I
did `from fractions import Fraction` and converted all my floats to fraction objects, it worked perfectly, meaning
that if I'd used fractions in my backtracking solution, I could have saved myself hours of time spent re-learning
highschool math. On the plus side I re-learned useful high-school math and received a good reminder that sometimes
the easiest solution to a problem is to work smarter instead of trying to have the computer solve all your problems
for you.

### Test Cases
Here are some extra test cases if you just want more things to test against. I just copied my Python test code here,
reformat for your own stuff.

```
print(solution([4, 30, 50]) == (12, 1))
print(solution([4, 17, 50]) == (-1, -1))
print(solution([1, 7, 34, 56, 58]) == (-1, -1))
print(solution([3, 9, 15.25, 19.25]) == (5, 2))
print(solution([1, 4]) == (2, 1))
print(solution([50, 154, 256]) == (4, 1))
print(solution([8, 43, 93, 144, 240, 330]) == (20, 1))
```

## Elevator Maintenance
The problem description for this one was something about updating elevator software correctly, but it's really just
version parsing and comparing.

Parsing is fairly trivial, just watch out for things like "2.0" being different from "2.0.0". I dealt with the problem
by using `None` for empty fields, but thinking about it now I probably could have used `-1` instead which would have
saved me a little extra conversion code when comparing values. Speaking of comparison, I used the fact that Python
will compare tuples to just generate `(major, minor, patch)` tuples for each `Version` and compared them. You can
see the whole thing in the code, but the only really tricky part was adding in the `-1` values in place of `None`
in the tuples. You have to explicitly check for `is None` becuase otherwise `0` will turn into `-1` and that would
be bad. Anyways, this one took me only about 30 minutes, which was a relief after the previous problem.

# Level 3
Level 3 is where I started to actually copy the problem descriptions, and you'll see most of the contents of `readme.txt`
replicated for your convenience, although I am leaving off the duplicate test cases to keep things clear.

## Fuel Injection Perfection

### Readme
```
Fuel Injection Perfection
=========================

Commander Lambda has asked for your help to refine the automatic quantum antimatter fuel injection system for the LAMBCHOP doomsday device. It's a great chance for you to get a closer look at the LAMBCHOP -- and maybe sneak in a bit of sabotage while you're at it -- so you took the job gladly. 

Quantum antimatter fuel comes in small pellets, which is convenient since the many moving parts of the LAMBCHOP each need to be fed fuel one pellet at a time. However, minions dump pellets in bulk into the fuel intake. You need to figure out the most efficient way to sort and shift the pellets down to a single pellet at a time. 

The fuel control mechanisms have three operations: 

1) Add one fuel pellet
2) Remove one fuel pellet
3) Divide the entire group of fuel pellets by 2 (due to the destructive energy released when a quantum antimatter pellet is cut in half, the safety controls will only allow this to happen if there is an even number of pellets)

Write a function called solution(n) which takes a positive integer as a string and returns the minimum number of operations needed to transform the number of pellets to 1. The fuel intake control panel can only display a number up to 309 digits long, so there won't ever be more pellets than you can express in that many digits.

For example:
solution(4) returns 2: 4 -> 2 -> 1
solution(15) returns 5: 15 -> 16 -> 8 -> 4 -> 2 -> 1
Quantum antimatter fuel comes in small pellets, which is convenient since the many moving parts of the LAMBCHOP each need to be fed fuel one pellet at a time. However, minions dump pellets in bulk into the fuel intake. You need to figure out the most efficient way to sort and shift the pellets down to a single pellet at a time. 

The fuel control mechanisms have three operations: 

1) Add one fuel pellet
2) Remove one fuel pellet
3) Divide the entire group of fuel pellets by 2 (due to the destructive energy released when a quantum antimatter pellet is cut in half, the safety controls will only allow this to happen if there is an even number of pellets)

Write a function called solution(n) which takes a positive integer as a string and returns the minimum number of operations needed to transform the number of pellets to 1. The fuel intake control panel can only display a number up to 309 digits long, so there won't ever be more pellets than you can express in that many digits.

For example:
solution(4) returns 2: 4 -> 2 -> 1
solution(15) returns 5: 15 -> 16 -> 8 -> 4 -> 2 -> 1
```

### Initial Analysis
This problem boils down to: given a number *n* and 3 operations (+1, -1, /2) get *n* to be 1 in as few operations as possible.
In general dividing by 2 is going to reduce *n* by the most, but since we can only do this if *n* is even, we have to use +1 and
-1 sometimes, the question is when do we +1 and when do we -1? A great example is that if you have 15 it's better to +1 to get to
16 and then /2 until we hit 1.

Intuitively this might make you think that the goal is to get *n* to the nearest power of 2 then divide away, and if you thought
that, *great job*, you're very close but not quite close enough. The problem here is that you can only +1 and -1 making it hard
to efficiently clear out the higher bits. I started this problem at about 9pm local time, so instead of trying to figure out that
problem I chose a good approximation that turns out to work correctly in every test case I've come up with, but not for all the
test cases Google has (😢).

### Solution 1
My solution was that instead of trying to think through the most optimimal way to make things powers of 2, I would optimize for
the number of 0-bits. At each step I would do all available operations (+1, -1, and /2 if possible). I then count the number of
`1` bits in each result, and pick the resulting number with the fewest `1` bits. As I said, this worked perfectly on all the test
cases I could come up with, but obviously I was missing something.

### Solution 2
I came back to the problem with a fresh perspective the next day (good thing they gave me a few days for each problem). The
problem with my original solution is that there must be some edge cases where I'm doing the wrong thing, and Google managed
to pick a bunch of edge-cases to test that. So it's back to the drawing board, but not quite. Our initial analysis still holds:
we want to get to a power of 2, but the big ah-ha moment for me was that it doesn't have to be the CLOSEST power of 2. Let's
assume we take the "divide by 2" option whenever we can, only adding or subtracting if that's not an option. My original
algorithm was doing that already, and it makes logical sense as it's our most "powerful" operation, and since +1 and -1 act
on the 0th bit, we ONLY want to change bit 0 if we can't divide by 2.

Now the big question, when do we add and when do we subtract? Well if there are a bunch of 1s at the low bits then we want
to add, but if there are few 1s then we want to subtract. Now this sounds *exactly* like my first attempt, so let's get
a little more specific. What if we focus ONLY on the 2 lowest bits? We only have 2 possible values: 11 and 01
(10 is out because then we would divide by 2). In the first case we should add, and in the second we should subtract.

Why the first 2 bits, you ask? Because instead of optimizing for the lowest number of 1 bits, we're now optimizing for
the MOST division operations. Divisions are the fastest/most powerful, and if we try to look at 3 or 4 bits, we find
that the outcomes don't change except for one small edge-case, the number 3. If *n* is exactly 3 (not just the lowest 2 bits)
then we want to subtract instead of add.

### Test Cases
My test setup for this one is a little more complicated, but the output is nicer looking, and it even gives me
an easy way to debug certain test cases. Test number 4 specifically fails on my original method and succeedes
with the correct solution (fun fact: #4 is actually just the first 212 characters of 2^10000, lucky me it worked
as a good test case).

```
def test(idx, inp, exp, debug=False):
    r = solution2(inp, debug)
    if r == exp:
        print("Test %d : OK" % idx)
    else:
        print("Test %d : FAIL : %s" % (idx, str(r)))

test(1, '15', 5)
test(2, '4', 2)
test(3, '18', 5, True) # 9 > 8 > 4 > 2 > 1
test(4, '19950631168807583848837421626835850838234968318861924548520089498529438830221946631919961684036194597899331129423209124271556491349413781117593785932096323957855730046793794526765246551266059895520550086918193311', 944)
test(5, int('0xFFFF', 16), 17)
test(6, '50', 7)
test(7, '30', 6)
test(8, '62', 7, True)
test(9, '64', 6)
test(10, '3', 2)
```

## Prepare the Bunnies' Escape

### Readme
```
Prepare the Bunnies' Escape
===========================

You're awfully close to destroying the LAMBCHOP doomsday device and freeing Commander Lambda's bunny workers, but once they're free of the work duties the bunnies are going to need to escape Lambda's space station via the escape pods as quickly as possible. Unfortunately, the halls of the space station are a maze of corridors and dead ends that will be a deathtrap for the escaping bunnies. Fortunately, Commander Lambda has put you in charge of a remodeling project that will give you the opportunity to make things a little easier for the bunnies. Unfortunately (again), you can't just remove all obstacles between the bunnies and the escape pods - at most you can remove one wall per escape pod path, both to maintain structural integrity of the station and to avoid arousing Commander Lambda's suspicions. 

You have maps of parts of the space station, each starting at a work area exit and ending at the door to an escape pod. The map is represented as a matrix of 0s and 1s, where 0s are passable space and 1s are impassable walls. The door out of the station is at the top left (0,0) and the door into an escape pod is at the bottom right (w-1,h-1). 

Write a function solution(map) that generates the length of the shortest path from the station door to the escape pod, where you are allowed to remove one wall as part of your remodeling plans. The path length is the total number of nodes you pass through, counting both the entrance and exit nodes. The starting and ending positions are always passable (0). The map will always be solvable, though you may or may not need to remove a wall. The height and width of the map can be from 2 to 20. Moves can only be made in cardinal directions; no diagonal moves are allowed.
```

### Initial Analysis
One of the sample test cases looks like this:
```
[[0, 0, 0, 0, 0, 0],
 [1, 1, 1, 1, 1, 0],
 [0, 0, 0, 0, 0, 0],
 [0, 1, 1, 1, 1, 1],
 [0, 1, 1, 1, 1, 1],
 [0, 0, 0, 0, 0, 0]]
```

And as you can see removing the wall at (1,0) would make the path shorter. Removing the wall at (1,1) would ALSO make the path shorter but not as
short as the removing the wall at (1,0). My initial take is that this is a graph problem. Generate different possible configurations and then
find the shortest path for each using BFS. The problem is that we are time-limited so we need to eliminate as many possible configurations as we
can before trying to generate possible configurations. This leads me to the first self-made test-case.

```
[[0,1,1,1,1,0,0,0],
 [0,0,0,0,0,1,1,0],
 [1,1,1,1,0,1,1,0],
 [1,1,1,1,0,1,1,0],
 [0,0,0,0,0,1,1,0],
 [0,1,1,1,1,1,1,0],
 [0,1,1,1,1,1,1,0],
 [0,0,0,0,0,0,0,0]]
```

Removing either (0,5) or (1,6) will solve the problem. This leads to two conclusions: we have to check ALL directions (we can't assume that
going up will be an invalid move), and there are rules we can use to exclude certain configurations before we try to test them. This second
point is only useful for optimizing performance, and I'm fairly confident I could implement it by generating a new configuration for every wall
where that wall is removed.

My current rules for removing a wall are:
- Wall must be reachable from a corridor (no reason to remove it otherwise)
- Wall must not be surrounded on 3 sides (otherwise removing it will have no effect)
- Don't remove corners (going down-left is the same as going left-down)
  - I'm going to ignore this to start with because it's annoying to detect and depends on the direction you're coming from.
    Also in the example above it would only save 7 new configurations, whereas the other rules save many more.

### Attempt 1
This time I was right on the money, although my code code definitely be cleaner. I created a graph and node class
when I could have just stored that information in a secondary grid. The basic idea is really exactly as I described
it: generate a set of possible configurations then perform a BFS on each to find the length of the configuration.
One thing I ran into is that some configurations may not be able to reach the end, so assuming that my end node
existed caused my program to crash. Test case #4 tests for that.

### Test Cases
```python
def test(index, inp, expected, debug=False):
    r = solution1(inp, debug)
    if r == expected:
        print("Test %d : OK" % index)
    else:
        print("Test %d : FAIL : %s" % (index, str(r)))

test(1, [
    [0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1],
    [0, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0]
    ], 11)
test(2, [
    [0, 1, 1, 0],
    [0, 0, 0, 1],
    [1, 1, 0, 0],
    [1, 1, 1, 0]
    ], 7)
test(3, [
    [0,1,1,1,1,0,0,0],
    [0,0,0,0,0,1,1,0],
    [1,1,1,1,0,1,1,0],
    [1,1,1,1,0,1,1,0],
    [0,0,0,0,0,1,1,0],
    [0,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,0],
    [0,0,0,0,0,0,0,0]
    ], 17)
test(4, [
    [0,1,1],
    [1,0,0],
    [1,1,0]
    ], 5)
```

## Doomsday Fuel

### Readme
```
Doomsday Fuel
=============

Making fuel for the LAMBCHOP's reactor core is a tricky process because of the exotic matter involved. It starts as raw ore, then during processing, begins randomly changing between forms, eventually reaching a stable form. There may be multiple stable forms that a sample could ultimately reach, not all of which are useful as fuel. 

Commander Lambda has tasked you to help the scientists increase fuel creation efficiency by predicting the end state of a given ore sample. You have carefully studied the different structures that the ore can take and which transitions it undergoes. It appears that, while random, the probability of each structure transforming is fixed. That is, each time the ore is in 1 state, it has the same probabilities of entering the next state (which might be the same state).  You have recorded the observed transitions in a matrix. The others in the lab have hypothesized more exotic forms that the ore can become, but you haven't seen all of them.

Write a function solution(m) that takes an array of array of nonnegative ints representing how many times that state has gone to the next state and return an array of ints for each terminal state giving the exact probabilities of each terminal state, represented as the numerator for each state, then the denominator for all of them at the end and in simplest form. The matrix is at most 10 by 10. It is guaranteed that no matter which state the ore is in, there is a path from that state to a terminal state. That is, the processing will always eventually end in a stable state. The ore starts in state 0. The denominator will fit within a signed 32-bit integer during the calculation, as long as the fraction is simplified regularly. 

For example, consider the matrix m:
[
  [0,1,0,0,0,1],  # s0, the initial state, goes to s1 and s5 with equal probability
  [4,0,0,3,2,0],  # s1 can become s0, s3, or s4, but with different probabilities
  [0,0,0,0,0,0],  # s2 is terminal, and unreachable (never observed in practice)
  [0,0,0,0,0,0],  # s3 is terminal
  [0,0,0,0,0,0],  # s4 is terminal
  [0,0,0,0,0,0],  # s5 is terminal
]
So, we can consider different paths to terminal states, such as:
s0 -> s1 -> s3
s0 -> s1 -> s0 -> s1 -> s0 -> s1 -> s4
s0 -> s1 -> s0 -> s5
Tracing the probabilities of each, we find that
s2 has probability 0
s3 has probability 3/14
s4 has probability 1/7
s5 has probability 9/14
So, putting that together, and making a common denominator, gives an answer in the form of
[s2.numerator, s3.numerator, s4.numerator, s5.numerator, denominator] which is
[0, 3, 2, 9, 14].
```

### Initial Analysis
Oh boy, this is a LOT to unpack, but it turns out that it's not quite as complicated as it first appears, if you remember your linear algebra class
or can google (heh) your way to victory, this problem is quite solvable. At first the problem may seem impossible if you're not good at statistics
and probabilities (hint: I'm not, I only ever took 1 statistics class in high-school and scrapped by because I got college credit for it).
The first thing I searched was "state machine probability", because that's what this is. It's a state machine and we want to find the probabilities
of reaching certain end states. This quickly lead to the idea of "markov chains", which is where the linear algebra comes in.

This website (https://brilliant.org/wiki/markov-chains) may help explain how markov chains work, and I'm a bit rusty with the math, but I'm pretty
sure this is the way to go. I also found this site (https://flylib.com/books/en/2.71.1.298/1/) which talks about markov chains in the context
of game programming, which might help later. After searching a little more, I found this post (https://math.stackexchange.com/questions/2337832/)
which appears to have been asked by someone else doing the Google Foobar challenge (given that the input matrix the asker gave is the same as one
of the sample cases). The answer is excellent because it gives a clear explanation on how to solve this type of mathematical problem.

### Attempt 1
AAAAHHHH. This took me quite a while to solve, not because the problem was hard but because of the lack of visible test-cases.
The big one that tripped me up was `[[0]] -> [1,1]`. It makes sense, but in my test cases I had the answer as `[0,1]`. AAAHHH.

Anyways, the markov chain thing was one correct solution and I used the math StackExchange page to implement it, combined with
this page https://en.wikipedia.org/wiki/Absorbing_Markov_chain (which is linked in the math StackExchange page). The biggest
frustration with all of this was, as usual, the lack of clear test cases. It took me several days to figure out why I had ONE
test case failing.


