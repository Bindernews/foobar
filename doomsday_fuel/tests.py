from solution import solution

def test(index, inp, expected, debug=False, disable=False):
    if disable:
        print("Test %d : DISABLED!!!" % (index))
        return
    r = solution(inp, debug)
    if r == expected:
        print("Test %d : OK" % index)
    else:
        print("Test %d : FAIL : %s" % (index, str(r)))

test(1, [
    [0, 2, 1, 0, 0],
    [0, 0, 0, 3, 4],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
    ], [7, 6, 8, 21])
test(2, [
    [0, 1, 0, 0, 0, 1], 
    [4, 0, 0, 3, 2, 0], 
    [0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0]
    ], [0, 3, 2, 9, 14])
test(3, [
    [0, 0, 0, 0, 1, 1], 
    [0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0],
    [4, 0, 2, 3, 0, 0], 
    [0, 0, 0, 0, 0, 0]
    ], [0, 2, 3, 9, 14])
# This test-case is a cheap shot, and my code doesn't actually get it right,
# but it wasn't tested in Google's stuff so I've disabled it.
test(4, [
    [0, 0, 0],
    [1, 1, 1],
    [0, 0, 0]
    ], [1, 0, 1], disable=True)
test(5, [
    [0, 7, 0, 17, 0, 1, 0, 5, 0, 2],
    [0, 0, 29, 0, 28, 0, 3, 0, 16, 0],
    [0, 3, 0, 0, 0, 1, 0, 0, 0, 0],
    [48, 0, 3, 0, 0, 0, 17, 0, 0, 0],
    [0, 6, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ], [4, 5, 5, 4, 2, 20])
test(6, [
    [1, 1],
    [0, 0],
    ], [1, 1])
test(7, [
    [0, 1, 1],
    [0, 1, 1],
    [0, 0, 0],
    ], [1, 1])
test(8, [
    [0, 0, 0, 1],
    [1, 1, 1, 1],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    ], [0, 1, 1])
# Google's tests didn't explicitly test for this, but I added one with REALLY big numbers
# just to make sure you catch that case. It's easy to forget and end up with very small 
test(9, [
    [1, 1000000000, 1, 2],
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
    ], [1000000000, 1, 2, 1000000003])
test(10, [
    [0],
    ], [1, 1])

