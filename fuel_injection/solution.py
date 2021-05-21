
DEBUG = False
def dbgprint(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)

def solution(start_n):
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

