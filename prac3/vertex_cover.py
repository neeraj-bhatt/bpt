import time
import itertools
import random as rd
import matplotlib.pyplot as plt

def vertex_cover_greedy(edges):
    start_time = time.time()

    vertex_cover = set()  # The set to store the vertex cover
    covered = set()       # To mark visited edges

    # Iterate over all the edges
    for edge in edges:
        u, v = edge

        # If neither u nor v is present in covered vertices set
        if u not in covered and v not in covered:
            # Add both u and v to vertex cover
            vertex_cover.add(u)
            vertex_cover.add(v)

            # Add both vertices to covered to mark them as covered
            covered.add(u)
            covered.add(v)

    end_time = time.time()
    cover_size = len(vertex_cover)
    time_taken = end_time - start_time

    # Optionally, print or return results
    print(f"Vertex Cover : {vertex_cover}")
    print(f"Vertex Cover Size: {cover_size}")
    print(f"Time Taken: {time_taken:.6f} seconds\n")

    return vertex_cover



# For vertex cover bruteforce approach
def is_vertex_cover(vertices, edges):
    """Check if the given set of vertices is a vertex cover for the edges"""
    covered_edges = set()
    for vertex in vertices:
        for edge in edges:
            if vertex in edge:
                covered_edges.add(edge)
    return len(covered_edges) == len(edges)

def vertex_cover_brute_force(edges):
    start_time = time.time()

    # Extract unique vertices from the edges
    vertices = set()
    for u, v in edges:
        vertices.add(u)
        vertices.add(v)

    # Generate all possible subsets of vertices
    min_cover = None
    min_cover_size = float('inf')

    for size in range(1, len(vertices) + 1):
        # Try all combinations of 'size' vertices
        for subset in itertools.combinations(vertices, size):
            if is_vertex_cover(subset, edges):
                # If this subset is a vertex cover, check if it's the smallest one
                if len(subset) < min_cover_size:
                    min_cover_size = len(subset)
                    min_cover = subset

    end_time = time.time()
    time_taken = end_time - start_time

    print(f"Vertex Cover Size: {min_cover_size}")
    print(f"Vertex Cover: {min_cover}")
    print(f"Time Taken: {time_taken:.6f} seconds\n")

    return min_cover

nodes = 20
# All possible edges formed by 20 nodes (undirected and without self loops)
all_possible_edges = [(u, v) for u in range(1, nodes + 1) for v in range(u + 1, nodes + 1)]

i = 1
edges_size = range(nodes, nodes*(nodes-1)//2, 20)
approx_factor = []
for n in edges_size:
    print(f"Iteration : {i}")
    print("--------------------------------------")
    edges = rd.sample(all_possible_edges, n)

    cover_brute_force = vertex_cover_brute_force(edges)
    cover_greedy = vertex_cover_greedy(edges)
    size_brute_force = len(cover_brute_force)
    size_greedy = len(cover_greedy)

    approx_factor.append(round(size_greedy/size_brute_force,3))
    i = i+1


plt.figure(figsize=(12, 6))

# Plotting the graph
plt.plot(edges_size, approx_factor, marker='o', linestyle='-', color='g')  # Line plot with dots

# Adding a dashed red line at y=2 (upper bound)
plt.axhline(y=2, color='r', linestyle='--', label='y=2 Approximation Factor roof value')

# Adding labels and title
plt.xlabel('Number of Edges')  # x-axis label
plt.ylabel('Approximation Factor')  # y-axis label
plt.title('Vertex Cover Approximation Factor vs Number of Edges')  # Title of the graph
plt.legend()

# Adding grid (optional)
plt.grid(True)

# Show the plot
plt.show()
