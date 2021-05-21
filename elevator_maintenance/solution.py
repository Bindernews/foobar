

class Version:
    def __init__(self, major, minor, patch):
        self.major = major
        self.minor = minor
        self.patch = patch
        self.original = None
        
    @staticmethod
    def parse(s):
        parts = s.split('.')
        major = Version._int_none(parts, 0)
        minor = Version._int_none(parts, 1)
        patch = Version._int_none(parts, 2)
        v = Version(major, minor, patch)
        v.original = s
        return v
        
    @staticmethod
    def _int_none(ar, i):
        if i < len(ar):
            return int(ar[i])
        else:
            return None
            
    def _as_tuple(self, default):
        return (self.major,
            default if self.minor is None else self.minor,
            default if self.patch is None else self.patch)
        
    def __lt__(self, rhs):
        lh = self._as_tuple(-1)
        rh = rhs._as_tuple(-2)
        #print("%s < %s : %s < %s = %s" % (str(self), str(rhs), str(lh), str(rh), str(lh < rh)))
        return lh < rh
        
    def __eq__(self, rhs):
        return self.major == rhs.major and self.minor == rhs.minor and self.patch == rhs.patch
        
    def __str__(self):
        s = '%d' % self.major
        if self.minor is not None:
            s += '.%d' % self.minor
        if self.patch is not None:
            s += '.%d' % self.patch
        return s
    
def solution(lst):
    vers = [Version.parse(s) for s in lst]
    vers.sort()
    return [str(v) for v in vers]

