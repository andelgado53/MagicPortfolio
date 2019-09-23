class GraphNode:

    def __init__(self, label):
        self.label = label
        self.neighbors = set()
        self.color = None


a = GraphNode('a')
b = GraphNode('b')
c = GraphNode('c')
d = GraphNode('d')
e = GraphNode('e')
f = GraphNode('f')
g = GraphNode('g')

a.neighbors.add(b)
a.neighbors.add(c)
a.neighbors.add(e)

b.neighbors.add(a)
b.neighbors.add(c)
b.neighbors.add(e)

c.neighbors.add(a)
c.neighbors.add(b)
c.neighbors.add(d)
c.neighbors.add(g)

d.neighbors.add(c)

e.neighbors.add(a)
e.neighbors.add(b)
e.neighbors.add(f)

f.neighbors.add(e)

graph = [a, b, c, d, e, f, g]
max_degree = 0
for g in graph:
    max_degree = max(max_degree, len(g.neighbors))


def pick_color(colors, picked):
    available_colors = colors - picked
    return list(available_colors)[0]


def color_me_graph(graph, degree):
    colors = set(range(degree + 1))
    for node in graph:
        used_colors = set()
        for neigbor in node.neighbors:
            used_colors.add(neigbor.color)
        node.color = pick_color(colors, used_colors)



print(color_me_graph(graph, max_degree))

for g in graph:
    print(g.label + ": " + str(g.color)) 
