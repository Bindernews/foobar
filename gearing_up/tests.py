from solution import solution

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
    