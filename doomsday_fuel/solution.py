from fractions import Fraction
import math

def solution(m, test_debug):
    # Python-3 version of dbgprint
    def dbgprint(*args, debug=True, **kwargs):
        if test_debug and debug:
            print(*args, **kwargs)
    from math import gcd
    
    # Delete above and uncomment these for python-2 compat
    #def dbgprint(*args, **kwargs):
    #    pass
    #from fractions import gcd
    
    # NOTE: All functions that end in _i modify the matrix "in-place", otherwise they return a new matrix
    
    def iter_row(m, r):
        return m[r]
        
    def iter_col(m, c):
        for i in range(len(m)):
            yield m[i][c]
    
    def mrows(m):
        return len(m)
        
    def mcols(m):
        if len(m) == 0:
            return 0
        else:
            return len(m[0])
            
    def mmul(ma, mb):
        mc = []
        rows = mrows(ma)
        cols = mcols(mb)
        assert(mcols(ma) == mrows(mb))
        for r in range(rows):
            new_row = []
            for c in range(cols):
                new_row.append(sum([va * vb for va,vb in zip(iter_row(ma, r), iter_col(mb, c))]))
            mc.append(new_row)
        return mc
        
    def test_mmul():
        ma = [[1,2,3],[4,5,6]]
        mb = [[7,8],[9,10],[11,12]]
        mc = mmul(ma, mb)
        exp = [[58,64],[139,154]]
        dbgprint('mmul correct: %s' % (str(mc == exp)))
        
    def mmul_s(ma, scalar):
        mc = []
        for r in ma:
            mc.append([v * scalar for v in r])
        return mc
        
    def madd_i(ma, mb, scalar=1):
        assert(mrows(ma) == mrows(mb) and mcols(ma) == mcols(mb))
        rows = min(mrows(ma), mrows(mb))
        cols = min(mcols(ma), mcols(mb))
        for r in range(rows):
            for c in range(cols):
                ma[r][c] += mb[r][c] * scalar
        return ma
    
    def mrow_swap_i(ma, r0, r1):
        r0_, r1_ = ma[r0], ma[r1]
        ma[r0], ma[r1] = r1_, r0_
        return ma
    
    def mrow_scale_i(ma, row, scalar):
        for c in range(len(ma[row])):
            ma[row][c] *= scalar
        return ma
    
    def mrow_addmul_i(ma, src, dst, scalar):
        src_row = ma[src]
        dst_row = ma[dst]
        for c in range(len(dst_row)):
            dst_row[c] = dst_row[c] + (src_row[c] * scalar)
        return ma
    
    def mrref_i(ma):
        rows = mrows(ma)
        cols = mcols(ma)
        lead = 0
        # Put into triangular form
        for r in range(0, rows):
            i = r
            while ma[i][lead] == 0:
                i += 1
                if i == rows:
                    i = r
                    lead += 1
                    if lead == cols:
                        break
            mrow_swap_i(ma, i, r)
            if ma[r][lead] != 0:
                mrow_scale_i(ma, r, 1/ma[r][lead])
            for i in range(rows):
                if i != r:
                    mrow_addmul_i(ma, r, i, -ma[i][lead])
            lead += 1
        return ma
        
    def test_rref():
        ma = [  [1, 2, -1, -4],
                [2, 3, -1, -11],
                [-2, 0, -3, 22]]
        mrref_i(ma)
        mprint(ma)
        
    def mcopy(ma):
        mc = [[v for v in ma[r]] for r in range(len(ma))]
        return mc
        
    def tofrac(v):
        return Fraction(v).limit_denominator(2147483649)
        
    def make_stochastic(ma):
        '''
        Takes a matrix and puts it into stochastic form.
        Returns both the new matrix and an array of ar[new_index] = old_index.
        '''
        mc = []
        ordering = [i for i in range(len(ma))]
        totals = []

        real_rows = 0
        # Get row sums so we can easily reorder
        for r in range(len(ma)):
            total = tofrac(sum(ma[r]))
            totals.append(total)
            if total > 0:
                real_rows += 1
                
        # Add in rows by default
        for r in range(len(ma)):
            total = totals[r]
            # If our total is 0 then make it an "absorbing" row otherwise normalize
            if total == 0:
                mc.append([tofrac(1 if r == c else 0) for c in range(len(ma[0]))])
            else:
                mc.append([tofrac(ma[r][c]) / total for c in range(len(ma[0]))])
        # Now rearrange to make sure all rows are good
        def _swap(r1, r2):
            mc[r1], mc[r2] = mc[r2], mc[r1]
            ordering[r1], ordering[r2] = ordering[r2], ordering[r1]
            totals[r1], totals[r2] = totals[r2], totals[r1]
            for r in range(len(mc)):
                mc[r][r1], mc[r][r2] = mc[r][r2], mc[r][r1]
        
        # Swap rows until all normal ones are at the front and identities are at the back
        row = 1
        while row < real_rows:
            # If the current row isn't "real" then swap until it is
            if totals[row] == 0:
                # Swap the next "real" row down until it's in this row, maintain ordering
                row2 = row + 1
                while totals[row2] == 0:
                    row2 += 1
                while row2 > row:
                    _swap(row2, row2 - 1)
                    row2 -=1
            row += 1
        return mc, ordering, real_rows
    
    def make_identity(rows):
        mc = []
        for i in range(rows):
            mc.append([1 if j == i else 0 for j in range(rows)])
        return mc
    
    def mconcat_right(ma, mb):
        mc = []
        for r in range(len(ma)):
            mc.append(ma[r] + mb[r])
        return mc
        
    def mclip(ma, row_min=0, row_max=-1, col_min=0, col_max=-1):
        if row_max < 0:
            row_max = mrows(ma) - 1 - row_max
        if col_max < 0:
            col_max = mcols(ma) - 1 - col_max
        #print('Clipping mat size (%d, %d) to (%d - %d, %d - %d)' % (mrows(ma), mcols(ma), row_min, row_max, col_min, col_max))
        mc = []
        for r in range(row_min, row_max):
            mc.append([ma[r][c] for c in range(col_min, col_max)])
        return mc
    
    def minverse(ma):
        ''' Returns the inverse of matrix :ma: '''
        mb = mconcat_right(ma, make_identity(len(ma)))
        mrref_i(mb)
        mc = mclip(mb, 0, -1, mcols(ma), -1)
        return mc
        
    def mprint(ma, debug=True):
        for r in ma:
            s = '[' + ', '.join(['%s'%str(v) for v in r]) + ']'
            dbgprint(s, debug=debug)
        dbgprint('', debug=debug)
    
    def lcm(ar):
        ''' Returns the least common multiple of list ar '''
        lcm = 1
        for v in ar:
            lcm = lcm * (v // gcd(lcm, v))
        return lcm
    
    # Using this Stack Exchange answer as math reference because I'm bad at math
    # https://math.stackexchange.com/questions/2337832/
    
    # Find fundamental matrix (N), then multiply by the absorbing states (R) and take the first row
    # of that resulting matrix (Pr) to get the result for each final state.
    # N = inverse(I - Q)
    # Pr = (N*R)[0,*]
    norm, ordering, terminal_start = make_stochastic(m)
    # terminal_start = first row of "terminals"
    
    # Early exit if we have no transition data
    if terminal_start == 0:
        numerators = [(1 if i == 0 else 0) for i in range(mrows(norm))]
        return numerators + [1]
    
    mI = mclip(norm, terminal_start, -1, terminal_start, -1)
    mQ = mclip(norm, 0, terminal_start, 0, terminal_start)
    mR = mclip(norm, 0, terminal_start, terminal_start, -1)
    mN_0 = madd_i(make_identity(terminal_start), mQ, -1)  # mNorm0 = (copy(mI) + (-1 * mQ))
    mN = minverse(mN_0)
    mP = mmul(mN, mR)
    
    mprint(norm)
    #mprint(mN)
    #mprint(mR)
    mprint(mP)
    
    # Now make the denominators all the same
    fracs = [tofrac(mP[0][c]) for c in range(mcols(mP))]
    denom = lcm([f.denominator for f in fracs])
    numerators = [f.numerator * (denom / f.denominator) for f in fracs]
    dbgprint(numerators)
    return numerators + [denom]    

