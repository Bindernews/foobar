# Gearing Up for Destruction
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

## Test Cases
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
