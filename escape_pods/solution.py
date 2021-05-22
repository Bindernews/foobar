DEBUG = True

def dbgprint(*args, debug=True, endl='\n'):
    if DEBUG and debug:
        print(*args, endl=endl)

MAX_FLOW = 999999999

class FlowNode:
    def __init__(self, id, graph):
        self.id = id
        self.graph = graph
        self.edges = {}
        self.r_edges = {}

class FlowEdge:
    def __init__(self, src, dst, cap, flow):
        self.src = src
        self.dst = dst
        self.cap = cap
        self.flow = flow
        
class FlowGraph:
    def __init__(self):
        self.nodes = {}
        
    def node(self, node_id):
        n = self.nodes.get(node_id)
        if n is None:
            n = FlowNode(node_id, self)
            self.nodes[node_id] = n
        return n
    
    def edges(self, node_id):
        for e in self.nodes[node_id].edges.values():
            yield e
    
    def add_edge(self, node_id_1, node_id_2, capacity):
        e = FlowEdge(node_id_1, node_id_2, capacity, 0)
        self.nodes[node_id_1].edges[node_id_2] = e
        self.nodes[node_id_2].r_edges[node_id_1] = e
        
    def get_edge(self, node_1, node_2):
        return self.nodes[node_id_1].edges[node_id_2]
        
    def edmonds_karp(self, n_source, n_sink):
        # This is a straightforward implementation of the edmonds-karp algorithm from Wikipeda
        flow = 0
        while True:
            q = []
            q.append(n_source)
            prev = {}
            while len(q) > 0:
                cur = q.pop(0)
                for e in self.edges(cur):
                    #print('Edge %d -> %d cap %d' % (e.src, e.dst, e.cap))
                    if prev.get(e.dst) is None and e.dst != n_source and e.cap > e.flow:
                        prev[e.dst] = e
                        q.append(e.dst)
            if prev.get(n_sink) is not None:
                # We have found an augmenting path
                delta_flow = MAX_FLOW
                e = prev[n_sink]
                while e is not None:
                    delta_flow = min(delta_flow, e.cap - e.flow)
                    e = prev.get(e.src)
                # Update edges by that amount
                e = prev.get(n_sink)
                while e is not None:
                    e.flow += delta_flow
                    e = prev.get(e.src)
                flow += delta_flow
            # Repeat until no augmenting path was found
            if prev.get(n_sink) is None:
                break
        return flow

def solution(entrances, exits, paths):
    # As far as I can tell, this is just the maximum flow problem.
    
    # Initialize the graph
    graph = FlowGraph()
    # Setup one source node and link to entrances
    graph.node(-1)
    for e in entrances:
        graph.node(e)
        graph.add_edge(-1, e, MAX_FLOW)
    # Setup sink node and link from exits
    graph.node(-2)
    for e in exits:
        graph.node(e)
        graph.add_edge(e, -2, MAX_FLOW)
    # Add all nodes
    for i in range(len(paths)):
        graph.node(i)
    # Add all other nodes
    for src in range(len(paths)):
        for dst in range(len(paths[src])):
            cap = paths[src][dst]
            if cap > 0:
                graph.add_edge(src, dst, cap)
    flow = graph.edmonds_karp(-1, -2)
    return flow
