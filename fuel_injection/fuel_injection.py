
   
def solution1(start_n, debug):
    def dbgprint(*args, **kwargs):
        if debug:
            print(*args, **kwargs)
            
    def ones(n):
        return bin(n).count("1")

    n = int(start_n)
    ops_count = 0
    while n > 1:
        # Check if (n + 1) / 2 will be even
        # What if sub makes an odd number
        ops = []
        n_add = n + 1
        c_add = ones(n_add)
        ops.append((c_add, n_add, 'A'))
        n_sub = n - 1
        c_sub = ones(n_sub)
        ops.append((c_sub, n_sub, 'S'))
        if n % 2 == 0:
            n_div = n // 2
            c_div = ones(n_div)
            ops.append((c_div, n_div, 'D'))            
        best = min(ops)
        dbgprint(best[2] + ' ', end='')
        n = best[1]
        ops_count += 1
    dbgprint('')
    return ops_count
    
def solution2(start_n, debug):
    def dbgprint(*args, **kwargs):
        if debug:
            print(*args, **kwargs)

    n = int(start_n)
    ops_count = 0
    while n > 1:
        # Divide by 2 if we can
        if (n % 2) == 0:
            n >>= 1
            dbgprint('D ', end='')
        elif (n & 3) == 1 or n == 3:
            n = n - 1
            dbgprint('S ', end='')
        else:
            n = n + 1
            dbgprint('A ', end='')
        ops_count += 1
    dbgprint('')
    return ops_count


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
