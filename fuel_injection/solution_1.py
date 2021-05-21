DEBUG = False
def dbgprint(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)

def ones(n):
    return bin(n).count("1")

def solution(start_n):
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
