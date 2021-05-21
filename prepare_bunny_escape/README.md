# Prepare the Bunnies' Escape

## Readme
```
Prepare the Bunnies' Escape
===========================

You're awfully close to destroying the LAMBCHOP doomsday device and freeing Commander Lambda's bunny workers, but once they're free of the work duties the bunnies are going to need to escape Lambda's space station via the escape pods as quickly as possible. Unfortunately, the halls of the space station are a maze of corridors and dead ends that will be a deathtrap for the escaping bunnies. Fortunately, Commander Lambda has put you in charge of a remodeling project that will give you the opportunity to make things a little easier for the bunnies. Unfortunately (again), you can't just remove all obstacles between the bunnies and the escape pods - at most you can remove one wall per escape pod path, both to maintain structural integrity of the station and to avoid arousing Commander Lambda's suspicions. 

You have maps of parts of the space station, each starting at a work area exit and ending at the door to an escape pod. The map is represented as a matrix of 0s and 1s, where 0s are passable space and 1s are impassable walls. The door out of the station is at the top left (0,0) and the door into an escape pod is at the bottom right (w-1,h-1). 

Write a function solution(map) that generates the length of the shortest path from the station door to the escape pod, where you are allowed to remove one wall as part of your remodeling plans. The path length is the total number of nodes you pass through, counting both the entrance and exit nodes. The starting and ending positions are always passable (0). The map will always be solvable, though you may or may not need to remove a wall. The height and width of the map can be from 2 to 20. Moves can only be made in cardinal directions; no diagonal moves are allowed.
```

### Initial Analysis
One of the sample test cases looks like this:
```
[[0, 0, 0, 0, 0, 0],
 [1, 1, 1, 1, 1, 0],
 [0, 0, 0, 0, 0, 0],
 [0, 1, 1, 1, 1, 1],
 [0, 1, 1, 1, 1, 1],
 [0, 0, 0, 0, 0, 0]]
```

And as you can see removing the wall at (1,0) would make the path shorter. Removing the wall at (1,1) would ALSO make the path shorter but not as
short as the removing the wall at (1,0). My initial take is that this is a graph problem. Generate different possible configurations and then
find the shortest path for each using BFS. The problem is that we are time-limited so we need to eliminate as many possible configurations as we
can before trying to generate possible configurations. This leads me to the first self-made test-case.

```
[[0,1,1,1,1,0,0,0],
 [0,0,0,0,0,1,1,0],
 [1,1,1,1,0,1,1,0],
 [1,1,1,1,0,1,1,0],
 [0,0,0,0,0,1,1,0],
 [0,1,1,1,1,1,1,0],
 [0,1,1,1,1,1,1,0],
 [0,0,0,0,0,0,0,0]]
```

Removing either (0,5) or (1,6) will solve the problem. This leads to two conclusions: we have to check ALL directions (we can't assume that
going up will be an invalid move), and there are rules we can use to exclude certain configurations before we try to test them. This second
point is only useful for optimizing performance, and I'm fairly confident I could implement it by generating a new configuration for every wall
where that wall is removed.

My current rules for removing a wall are:
- Wall must be reachable from a corridor (no reason to remove it otherwise)
- Wall must not be surrounded on 3 sides (otherwise removing it will have no effect)
- Don't remove corners (going down-left is the same as going left-down)
  - I'm going to ignore this to start with because it's annoying to detect and depends on the direction you're coming from.
    Also in the example above it would only save 7 new configurations, whereas the other rules save many more.

## Attempt 1
This time I was right on the money, although my code code definitely be cleaner. I created a graph and node class
when I could have just stored that information in a secondary grid. The basic idea is really exactly as I described
it: generate a set of possible configurations then perform a BFS on each to find the length of the configuration.
One thing I ran into is that some configurations may not be able to reach the end, so assuming that my end node
existed caused my program to crash. Test case #4 tests for that.

## Test Cases
```python
def test(index, inp, expected, debug=False):
    r = solution1(inp, debug)
    if r == expected:
        print("Test %d : OK" % index)
    else:
        print("Test %d : FAIL : %s" % (index, str(r)))

test(1, [
    [0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1],
    [0, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0]
    ], 11)
test(2, [
    [0, 1, 1, 0],
    [0, 0, 0, 1],
    [1, 1, 0, 0],
    [1, 1, 1, 0]
    ], 7)
test(3, [
    [0,1,1,1,1,0,0,0],
    [0,0,0,0,0,1,1,0],
    [1,1,1,1,0,1,1,0],
    [1,1,1,1,0,1,1,0],
    [0,0,0,0,0,1,1,0],
    [0,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,0],
    [0,0,0,0,0,0,0,0]
    ], 17)
test(4, [
    [0,1,1],
    [1,0,0],
    [1,1,0]
    ], 5)
```
