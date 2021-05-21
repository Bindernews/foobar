# Fuel Injection Perfection

## Readme
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

## Initial Analysis
This problem boils down to: given a number *n* and 3 operations (+1, -1, /2) get *n* to be 1 in as few operations as possible.
In general dividing by 2 is going to reduce *n* by the most, but since we can only do this if *n* is even, we have to use +1 and
-1 sometimes, the question is when do we +1 and when do we -1? A great example is that if you have 15 it's better to +1 to get to
16 and then /2 until we hit 1.

Intuitively this might make you think that the goal is to get *n* to the nearest power of 2 then divide away, and if you thought
that, *great job*, you're very close but not quite close enough. The problem here is that you can only +1 and -1 making it hard
to efficiently clear out the higher bits. I started this problem at about 9pm local time, so instead of trying to figure out that
problem I chose a good approximation that turns out to work correctly in every test case I've come up with, but not for all the
test cases Google has (😢).

## Solution 1
My solution was that instead of trying to think through the most optimimal way to make things powers of 2, I would optimize for
the number of 0-bits. At each step I would do all available operations (+1, -1, and /2 if possible). I then count the number of
`1` bits in each result, and pick the resulting number with the fewest `1` bits. As I said, this worked perfectly on all the test
cases I could come up with, but obviously I was missing something.

## Solution 2
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
