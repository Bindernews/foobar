import solution as sol

def test(idx, inp, exp, debug=False):
    sol.DEBUG = debug
    r = sol.solution(inp)
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

