import solution as sol

def test(index, dimensions, your_position, trainer_position, distance, expected, debug=False, disable=False):
    if disable:
        print("Test %d : DISABLED!!!" % (index))
        return
    sol.DEBUG = debug
    r = sol.solution(dimensions, your_position, trainer_position, distance)
    if r == expected:
        print("Test %d : OK" % index)
    else:
        print("Test %d : FAIL : %s" % (index, str(r)))

test(1,
    [3,2], [1,1], [2,1], 4,
    7)
test(2,
    [300,275], [150,150], [185,100], 500,
    9)
test(3,
    [42, 59], [34, 44], [6, 34], 5000,
    30904)
test(4,
    [10, 2], [1, 1], [9, 1], 7,
    0)
test(5,
    [869, 128], [524, 86], [288, 28], 5671
    911)
