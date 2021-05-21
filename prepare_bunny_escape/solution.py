import collections

def solution(map, test_debug=False):
    def dbgprint(*args, debug=True, **kwargs):
        if test_debug and debug:
            print(*args, **kwargs)
    # Delete above and uncomment these for python-2 compat
    #def dbgprint(*args, **kwargs):
    #    pass
    
    Point = collections.namedtuple('Point', ['x', 'y'])
    
    class Graph:
        def __init__(self):
            self.nodes = {}
        
        def add_node(self, pos):
            n = self.nodes.get(pos)
            if not n:
                n = Node(pos.x, pos.y)
                self.nodes[pos] = n
            return n
        
        def get_node(self, pos):
            return self.nodes.get(pos)
            
        def add_edge(self, n1, n2, back=False):
            self.nodes[n1].edges.add(n2)
            if back:
                self.nodes[n2].edges.add(n1)
        
        def iter_edges(self, node):
            src_node = self.nodes[node]
            for dst_node in src_node.edges:
                yield self.nodes[dst_node]
        
        def distance_bfs(self, start_node, debug=False):
            # Reset all distances
            for node in self.nodes.values():
                node.distance = 9999999
                node.visited = False
            start_node_ref = self.get_node(start_node)
            start_node_ref.distance = 1
            start_node_ref.visited = True
            queue = [self.nodes[start_node]]
            while len(queue) > 0:
                node_ref = queue.pop(0)
                dbgprint('(%d,%d) > ' % (node_ref.x, node_ref.y), debug=debug, end='')
                for neighbor_ref in self.iter_edges(node_ref.point()):
                    if not neighbor_ref.visited:
                        neighbor_ref.visited = True
                        neighbor_ref.distance = min(neighbor_ref.distance, node_ref.distance + 1)
                        queue.append(neighbor_ref)
            dbgprint('', debug=debug)
    
    class Node:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.edges = set()
            self.visited = False
            self.distance = -1
            
        def point(self):
            return Point(self.x, self.y)
            
        def clone(self):
            n = Node(self.x, self.y)
            n.edges = list(self.edges)
            n.visited = self.visited
            return n
    
    class GridMap:
        def __init__(self, w, h, src_grid=None):
            self.w = w
            self.h = h
            if src_grid:
                self.grid = [list(src_grid[i]) for i in range(h)]
            else:
                self.grid = [[0 for j in range(w)] for i in range(h)]
                
        def at(self, pos, default=1):
            if pos.x < 0 or pos.y < 0 or pos.x >= self.w or pos.y >= self.h:
                return default
            else:
                return self.grid[pos.y][pos.x]
        
        def put(self, pos, value):
            if pos.x >= 0 and pos.y >= 0 and pos.x < self.w and pos.y < self.h:
                self.grid[pos.y][pos.x] = value
                return True
            else:
                return False
                
        def clone(self):
            return GridMap(self.w, self.h, self.grid)
            
        def points_around(self, pos, allow_oob=True):
            pts = [Point(pos.x-1, pos.y), Point(pos.x+1, pos.y), Point(pos.x, pos.y-1), Point(pos.x, pos.y+1)]
            if allow_oob:
                return pts
            else:
                return [pt for pt in pts if self.at(pt, None) != None]
            
        def to_graph(self, start_pos=Point(0,0)):
            # Flood fill algorithm to link nodes
            stack = [start_pos]
            seen = set(start_pos)
            graph = Graph()
            graph.add_node(start_pos)
            while len(stack) > 0:
                pos = stack.pop()
                for pos1 in self.points_around(pos):
                    if self.at(pos1) == 0:
                        # Add edge
                        graph.add_node(pos1)
                        graph.add_edge(pos, pos1, True)
                        # Add new pos to stack 
                        if pos1 not in seen:
                            seen.add(pos1)
                            stack.append(pos1)
            return graph
                            
        def flood_iter(self, start_pos, allow_oob=False, dfs=True):
            stack = [start_pos]
            seen = set(start_pos)
            while len(stack) > 0:
                if dfs:
                    pos = stack.pop()
                else: # BFS mode
                    pos = stack.pop(1)
                for pos1 in self.points_around(pos, allow_oob):
                    yield (pos, pos1, (pos1 in seen))
                    if self.at(pos1) == 0 and pos1 not in seen:
                        stack.append(pos1)
                    seen.add(pos1)
                    
        def distance_bfs(self, start_pos):
            queue = [start_pos]
            # Initialize the distance map
            dist_map = self.clone()
            for y in range(len(self.h)):
                for x in range(len(self.w)):
                    dist_map.put(Point(x,y), -1)
        
        def print_grid(self):
            for y in range(self.h):
                dbgprint(str(self.grid[y]))
            
    
    # begin
    grid0 = GridMap(len(map[0]), len(map), map)
    # Shortest possible length
    shortest_possible = grid0.w + grid0.h - 1
    
    # Generate all configs
    configs = [grid0]
    for pos0, pos1, seen in grid0.flood_iter(Point(0,0), False):
        if grid0.at(pos1, -1) == 1 and not seen:
            walls = 0
            for pt in grid0.points_around(pos1, True):
                walls += grid0.at(pt)
            if walls < 3:
                new_config = grid0.clone()
                new_config.put(pos1, 0)
                configs.append(new_config)
    
    best_distance = 99999
    best_index = -1
    best_graph = None
    dbgprint('Config count: %d' % len(configs))
    for i in range(len(configs)):
        config = configs[i]
        #config.print_grid()
        #dbgprint('')
        graph = config.to_graph()
        graph.distance_bfs(Point(0,0))
        end_node = graph.get_node(Point(grid0.w-1, grid0.h-1))
        graph_dist = end_node.distance if end_node else 999999
        if graph_dist < best_distance:
            best_distance = graph_dist
            best_index = i
            best_graph = graph
    
    if test_debug:
        best_graph.distance_bfs(Point(0,0), debug=True)
    configs[i].print_grid()
    
    return best_distance    
    # end
    
