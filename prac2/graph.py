import networkx as nx
import matplotlib
matplotlib.use("TkAgg") # incase of ubuntu (agg), cuz it cannot show interacitves that .show() generates
import matplotlib.pyplot as plt
import random as rd
import sys

# used chatgpt to generate random edges in this method
# generate random pair of m edges given n, m value in input.txt file
def generate_random_graph_edges(input_file: str):

    # reads n and m value (no. of nodes and edges)
    with open(input_file) as file:
        line = file.readline()
        n, m = map(int, line.strip().split())

    # Make sure m is within the maximum possible edges for an undirected graph
    max_edges = n * (n - 1) // 2
    if m > max_edges:
        raise ValueError(f"Too many edges. Max possible for {n} nodes is {max_edges}")

    # Generate all possible undirected edges without self-loops
    all_possible_edges = [(u, v) for u in range(1, n + 1) for v in range(u + 1, n + 1)]

    # Randomly sample m unique edges
    random_edges = rd.sample(all_possible_edges, m)

    with open(input_file, 'w') as ifile:
        ifile.write(line)
        for u, v in random_edges:
            ifile.write(f"{u} {v}\n")


def read_edges_from_input(input_file: str):
    edges = []
    with open(input_file) as file:
        file.readline() # skip first line n, m value
        for line in file:
            u, v = map(int, line.strip().split())
            edges.append((u,v))
    return edges


# draw graph by taking edge values from input.txt file
def draw_graph(input_file: str):
    G = nx.Graph()

    edges = read_edges_from_input(input_file)

    G.add_edges_from(edges)

    print(G.edges())
    
    plt.ion()
    nx.draw(G, with_labels=True)
    plt.show()
    plt.pause(5)


def draw_best_vertex_cover_graph(input_file: str, output_file: str):
    best_cover = []

    edges = read_edges_from_input(input_file)

    with open(output_file, 'r') as file:
        for line in file:
            # Check if the line contains the best vertex cover
            if line.startswith("Vertex cover (at most 2 times of optimal):"):
                # Extract the numbers after the colon
                best_cover = list(map(int, line.split(":")[1].strip().split()))
                break  # Stop once we have found the line
    
    G = nx.Graph()
    G.add_edges_from(edges)
    print(G.edges())
    print(best_cover)

    node_color = ['red' if node in best_cover else 'skyblue' for node in G.nodes()]

    nx.draw(G, node_color=node_color, with_labels=True, node_size=500, font_size=10)
    plt.show()

# used chatgpt to learn about use of sys this way
if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == 'generate':
            input_file = sys.argv[2]
            generate_random_graph_edges(input_file)
        elif sys.argv[1] == 'draw':
            input_file = sys.argv[2]
            draw_graph(input_file)
        elif sys.argv[1] == 'vc':
            input_file = sys.argv[2]
            output_file = sys.argv[3]
            draw_best_vertex_cover_graph(input_file, output_file)

