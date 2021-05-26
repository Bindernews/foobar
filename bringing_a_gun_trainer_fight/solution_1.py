import collections
import math

DEBUG = False

# Note: this was basically my first attempt, and it's VERY close to a successful solution.
#       Unfortunately it doesn't handle you shooting yourself.


def dbgprint(*args, debug=True, end='\n'):
    if DEBUG and debug:
        print(*args, end=end)

PointBase = collections.namedtuple('PointBase', ('x', 'y'))
class Point(PointBase):
    def len_sq(self):
        return ((self[0]*self[0]) + (self[1]*self[1]))
    def len(self):
        return math.sqrt(self.len_sq())
    def angle(self):
        return math.atan2(self.y, self.x)
    def __add__(self, rhs):
        return Point(self.x + rhs.x, self.y + rhs.y)
    def __sub__(self, rhs):
        return Point(self.x - rhs.x, self.y - rhs.y)
    def __mul__(self, rhs):
        return Point(self.x * rhs.x, self.y * rhs.y)
    def __div__(self, rhs):
        return Point(self.x / rhs.x, self.y / rhs.y)
        
def generate_mirrored_pos(dims, start_pos, mirror_x, mirror_y):
    flip_x = mirror_x % 2 == 1
    flip_y = mirror_y % 2 == 1
    trainer_x = dims.x - start_pos.x if flip_x else start_pos.x
    trainer_y = dims.y - start_pos.y if flip_y else start_pos.y
    return (dims * Point(mirror_x, mirror_y)) + Point(trainer_x, trainer_y)

def solution(dimensions, your_position, trainer_position, distance):
    your_pos = Point(your_position[0], your_position[1])
    trainer_pos = Point(trainer_position[0], trainer_position[1])
    dims = Point(dimensions[0], dimensions[1])
    
    # Determine min and max mirror ranges
    x_mirrors = math.floor(distance / dims.x) + 1
    y_mirrors = math.floor(distance / dims.y) + 1
    dbgprint('X,Y mirrors: (%d, %d)' % (x_mirrors, y_mirrors))
    # Generate all mirrored positions
    distance_sq = distance * distance
    mirrored_trainers = []
    mirrored_yous = []
    for ym in range(-y_mirrors, y_mirrors+1):
        for xm in range(-x_mirrors, x_mirrors+1):
            relative_pos = generate_mirrored_pos(dims, trainer_pos, xm, ym) - your_pos
            if relative_pos.len_sq() <= distance_sq:
                mirrored_trainers.append(relative_pos)
                mirrored_yous.append(generate_mirrored_pos(dims, your_pos, xm, ym) - your_pos)
    # Generate invalid angles (you'd hit yourself)
    death_angles = set()
    for pos in mirrored_yous:
        death_angles.add(pos.angle())
    # Filter out duplicate angles
    good_angles = set()
    for pos in mirrored_trainers:
        good_angles.add(pos.angle())
    dbgprint(death_angles)
    dbgprint(good_angles)
    return len(good_angles - death_angles)
    
    