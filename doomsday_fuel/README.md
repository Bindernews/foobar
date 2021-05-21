# Doomsday Fuel

## Readme
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

## Initial Analysis
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

## Attempt 1
AAAAHHHH. This took me quite a while to solve, not because the problem was hard but because of the lack of visible test-cases.
The big one that tripped me up was `[[0]] -> [1,1]`. It makes sense, but in my test cases I had the answer as `[0,1]`. AAAHHH.

Anyways, the markov chain thing was one correct solution and I used the math StackExchange page to implement it, combined with
this page https://en.wikipedia.org/wiki/Absorbing_Markov_chain (which is linked in the math StackExchange page). The biggest
frustration with all of this was, as usual, the lack of clear test cases. It took me several days to figure out why I had ONE
test case failing.

