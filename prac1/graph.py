import networkx as nx
import matplotlib.pyplot as plt

edges = []

with open("input.txt") as file:
    for line in file:
        u, v = map(int, line.strip().split())
        if u == v:
            continue
        else:
            edges.append((u,v))

G = nx.Graph()
G.add_edges_from(edges)

print(G.edges())

nx.draw(G, with_labels=True)

plt.show()