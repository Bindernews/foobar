import collections
import math
from fractions import Fraction

DEBUG = True

class Range:
    def __init__(self, mn, mx):
        self.min = Fraction(mn)
        self.max = Fraction(mx)
        
    def set(self, nmin, nmax):
        if nmin > nmax:
            nmin = -1
            nmax = -1
        nmin = round(nmin, 4)
        nmax = round(nmax, 4)
        if self.min != nmin or self.max != nmax:
            self.min = nmin
            self.max = nmax
            return True
        return False
        
    def clone(self):
        return Range(self.min, self.max)
        
    def get_avg(self, round_up):
        avg = (self.min + self.max) * 1000 / 2
        if round_up:
            avg = math.ceil(avg)
        else:
            avg = math.floor(avg)
        return avg / 1000
    
    def __str__(self):
        return "[ %f, %f ]" % (self.min, self.max)
    
    def __repr__(self):
        return str(self)


class State:
    def __init__(self, ranges, pegs, up):
        self.rg = []
        for r in ranges:
            self.rg.append(r.clone())
        self.pegs = pegs
        self.up = up
        
    def propogate(self, i0, delta):
        # Update i1 based on min and max of i0
        i1 = (i0 + delta) % len(self.rg)
        r0 = self.rg[i0]
        r1 = self.rg[i1]
        dist = abs(self.pegs[i0] - self.pegs[i1])
        # new min is larger of current min or (dist - i0.max)
        nmin = max(r1.min, dist - r0.max)
        nmax = min(r1.max, dist - r0.min)
        return not r1.set(nmin, nmax)

    def propogate_ends(self):
        r0 = self.rg[0]
        r1 = self.rg[-1]
        nmin = min(max(r0.min / 2, r1.min), r1.max)
        nmax = max(min(r0.max / 2, r1.max), r1.min)
        mod = r1.set(nmin, nmax)
        mod = mod or r0.set(r1.min * 2, r1.max * 2)
        return not mod
        
    def solve(self):
        # Do initial state solve
        self.propogate_ends()
        for i in range(len(self.rg)-1):
            self.propogate(i, 1)
        # Walk back and forth along the array until the state is stable
        i = len(self.rg)-1
        d = -1
        while True:
            done = self.propogate(i, d)
            i += d
            # Update the ends
            if i == len(self.rg)-1:
                done = self.propogate_ends()
                d = -1
            if i == 0:
                done = self.propogate_ends()
                d = 1
            # Check for error
            if self.rg[i].min < 0 or self.rg[i].max < 0:
                return -1
            if done:
                break
                
        if self.rg[0].min == self.rg[0].max:
            return 1
        else:
            return 0
    
def solution1(pegs):
    ranges0 = []
    for i in range(len(pegs) - 1):
        ranges0.append(Range(1, pegs[i + 1] - pegs[i] - 1))
    ranges0.append(Range(1, ranges0[-1].max))
    
    states = []
    states.append(State(ranges0, pegs, True))
    while True:
        s0 = states[-1]
        r = s0.solve()
        #print(s0.rg)
        
        # No possible solution
        if r == -1:
            # If we reached an error state, backtrack
            while len(states) > 0 and states[-1].up:
                states.pop()
            # Ran out of things to try, return failure
            if len(states) == 0:
                return (-1, -1)
            else:
                # Push new state with "up"
                states.pop()
                st = State(states[-1].rg, pegs, True)
                st.rg[0].min = st.rg[0].get_avg(True)
                states.append(st)
                if DEBUG:
                    print("Stack up %d - %s" % (len(states), str(st.rg)))
            
        # We found a solution!
        elif r == 1:
            #print(s0.rg)
            rg = states[-1].rg[0]
            return rg.max.as_integer_ratio()
        
        # No confirmed solution, but it's possible to find one
        elif r == 0:
            # Try to solve by splitting
            st = State(states[-1].rg, pegs, False)
            st.rg[0].max = st.rg[0].get_avg(False)
            states.append(st)
            if DEBUG:
                print("Stack down %d - %s" % (len(states), str(st.rg)))

def solution2(pegs):
    diffs = [0] + [(pegs[i] - pegs[i - 1]) for i in range(1, len(pegs))]

    def compute_radii(r0):
        v = [r0]
        for i in range(1, len(pegs)):
            v.append(diffs[i] - v[i - 1])
        return v
    
    r0 = Range(2, diffs[1])
    # Constrain values so we shouldn't have any radii below 0
    minM = min(compute_radii(r0.min))
    maxM = min(compute_radii(r0.max))
    if minM < 1:
        r0.min -= (minM)
    if maxM < 1:
        r0.max += (maxM)
    # Compute new ending radii
    r1 = Range(compute_radii(r0.min)[-1], compute_radii(r0.max)[-1])
    # Solve for value where 0th radius = 2*nth radius
    # This becomes a line, as 0th radius goes up/down (depending on if there are an even or odd number of gears)
    # the nth radius goes up at half the speed. "0.5x = mx + b" => "(0.5 - m)x = b" => "x = b / (0.5 - m)"
    # m simply determines if there are an even or odd number of gears  m = (r1.max - r1.min) / (r0.max - r0.min)
    if len(pegs) % 2 == 1:
        m = Fraction(1)
    else:
        m = Fraction(-1)
    b = r1.min - (m * r0.min)
    x = b / (Fraction(0.5) - m)
    #print("m = %f  b = %f  x = %f" % (m, b, x))
    # Finally we test to make sure there are no invalid radii
    for r in compute_radii(x):
        if r < 1:
            return (-1, -1)
    return (x.numerator, x.denominator)
    
    
def solution(pegs):
    return solution2(pegs)
    
def make_test(sln, peg0):
    pegs = [peg0]
    for i in range(1, len(sln)):
        pegs.append(pegs[i - 1] + sln[i] + sln[i - 1])
    return pegs

if False:
    print(make_test([2.5, 3.5, 2.75, 1.25], 3))
    print(make_test([4, 100, 2], 50))
    print(make_test([20, 15, 35, 16, 80, 10], 8))
    print(make_test([2.5, 2, 1.25], 2))

if True:
    print(solution([4, 30, 50]) == (12, 1))
    print(solution([4, 17, 50]) == (-1, -1))
    print(solution([1, 7, 34, 56, 58]) == (-1, -1))
    print(solution([3, 9, 15.25, 19.25]) == (5, 2))
    print(solution([1, 4]) == (2, 1))
    print(solution([50, 154, 256]) == (4, 1))
    print(solution([8, 43, 93, 144, 240, 330]) == (20, 1))
    
