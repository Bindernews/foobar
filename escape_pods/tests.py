import solution as sol

def test(index, entrances, exits, paths, expected, debug=False, disable=False):
    if disable:
        print("Test %d : DISABLED!!!" % (index))
        return
    sol.DEBUG = debug
    r = sol.solution(entrances, exits, paths)
    if r == expected:
        print("Test %d : OK" % index)
    else:
        print("Test %d : FAIL : %s" % (index, str(r)))

test(1, 
    [0], 
    [3], 
    [
    [0, 7, 0, 0],
    [0, 0, 6, 0],
    [0, 0, 0, 8],
    [9, 0, 0, 0],
    ], 
    6)
test(2, 
    [0, 1], 
    [4, 5], 
    [
    [0, 0, 4, 6, 0, 0],
    [0, 0, 5, 2, 0, 0],
    [0, 0, 0, 0, 4, 4],
    [0, 0, 0, 0, 6, 6], 
    [0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0]
    ],
    16)
test(3,
    [0],
    [1],
    [
    [0, 0], 
    [0, 0],
    ],
    0)
test(4,
    [0, 1],
    [2],
    [
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    ],
    4)
