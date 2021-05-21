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
        

def solution(pegs):
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

    
