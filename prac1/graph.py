import networkx as nx
import matplotlib.pyplot as plt
import random as rd

file = open("input.txt")
line = file.readline()
n, m = map(int, line.strip().split())
file.close()

# Make sure m is within the maximum possible edges for an undirected graph
max_edges = n * (n - 1) // 2
if m > max_edges:
    raise ValueError(f"Too many edges. Max possible for {n} nodes is {max_edges}")

# Generate all possible undirected edges without self-loops
all_possible_edges = [(u, v) for u in range(1, n + 1) for v in range(u + 1, n + 1)]

# Randomly sample m unique edges
random_edges = rd.sample(all_possible_edges, m)

with open("input.txt", 'a') as ifile:
    for u, v in random_edges:
        ifile.write(f"{u} {v}\n")
ifile.close()

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
