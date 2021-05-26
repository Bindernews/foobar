import collections
import math

DEBUG = False

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
    
def add_position(angles, pos, trainer, max_dist_squared):
    if pos.len_sq() > max_dist_squared:
        return
    theta = pos.angle()
    if angles.get(theta) is None:
        angles[theta] = []
    angles[theta].append((pos, trainer))

def solution(dimensions, your_position, trainer_position, distance):
    your_pos = Point(your_position[0], your_position[1])
    trainer_pos = Point(trainer_position[0], trainer_position[1])
    dims = Point(dimensions[0], dimensions[1])
    
    # Determine min and max mirror ranges
    x_mirrors = int(distance / dims.x) + 1
    y_mirrors = int(distance / dims.y) + 1
    # Generate all mirrored positions
    distance_sq = distance * distance
    angles = {}
    for ym in range(-y_mirrors, y_mirrors+1):
        for xm in range(-x_mirrors, x_mirrors+1):
            add_position(angles, generate_mirrored_pos(dims, trainer_pos, xm, ym) - your_pos, True, distance_sq)
            # Don't try to shoot your real self!
            if xm != 0 or ym != 0:
                add_position(angles, generate_mirrored_pos(dims, your_pos, xm, ym) - your_pos, False, distance_sq)
    
    # Sort positions for each angle by distance, then decide if we shoot at that angle
    good_angles = set()
    for theta in angles.keys():
        angles[theta].sort(key=lambda v: v[0].len_sq())
        # If the closest thing we're shooting at this angle is a trainer then we're good to shoot.
        if angles[theta][0][1]:
            good_angles.add(theta)
    return len(good_angles)
    
    