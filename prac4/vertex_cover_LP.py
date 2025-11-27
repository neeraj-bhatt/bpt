import numpy as np
import pandas as pd
import random as rd
from scipy.optimize import linprog

# Vertex Cover with greedy approach
def vertex_cover_greedy(edges):
    vertex_cover = set()

    for edge in edges:
        u, v = edge
        if u not in vertex_cover and v not in vertex_cover:
            vertex_cover.add(u)
            vertex_cover.add(v)

    return vertex_cover


# Solves LP relaxation for vertex cover
def lp_relaxation(n, m, edges_list):

    # Define the LP coefficient
    c = np.ones(n)

    # Inequalities (x_u + x_v >= 1 for each edge (u, v))
    ineq_A = np.zeros((m, n))
    ineq_b = -np.ones(m)

    for i, (u, v) in enumerate(edges_list):
        ineq_A[i, u-1] = -1
        ineq_A[i, v-1] = -1
    
    # solve LP problem
    result = linprog(c, A_ub=ineq_A, b_ub=ineq_b, bounds=[(0,1)] * n, method='highs')

    if result.success:
        return result.x
    else:
        print(f"LP relaxation failed for {m} edges : {result.message}")
        return None


# Round LP solution to obtain an approximate vertex cover
def round_lp_solution(lp_solution):
    # Round to 0 or 1 based on a threshold (0.5)
    return {i+1 for i, x in enumerate(lp_solution) if x >= 0.5}


def program(nodes):

    # All possible edges
    all_possible_edges = [(u, v) for u in range(1, nodes + 1) for v in range(u + 1, nodes + 1)]

    max_possible_edges_size = len(all_possible_edges)

    edges_size = range(nodes, max_possible_edges_size+1, nodes)
    approx_factor = []
    for e in edges_size:
        print(f"------Running experiment for {nodes} nodes and {e} edges------")
        edges = rd.sample(all_possible_edges, e)

        # LP relaxation
        lp_solution = lp_relaxation(nodes, e, edges)
        if lp_solution is None:
            print(f"LP Relaxation failed for {e} edges.")
            continue

        lp_optimal_value = np.sum(lp_solution)
        print(f"LP optimal (fractional): {lp_optimal_value:.3f}")

        # Greedy algorithm
        greedy_cover = vertex_cover_greedy(edges)
        greedy_size = len(greedy_cover)
        greedy_factor = greedy_size / lp_optimal_value if lp_optimal_value > 0 else float('inf')

        # LP rounding algorithm
        lp_rounded_cover = round_lp_solution(lp_solution)
        lp_rounded_size = len(lp_rounded_cover)
        lp_rounded_factor = lp_rounded_size / lp_optimal_value if lp_optimal_value > 0 else float('inf')

        print(f"Greedy: {greedy_size} vertices, Factor: {greedy_factor:.3f}, Greedy Cover: {greedy_cover}")
        print(f"LP Rounding: {lp_rounded_size} vertices, Factor: {lp_rounded_factor:.3f}, LP Rounded Cover: {lp_rounded_cover}")

        approx_factor.append({
            'edges':e,
            'greedy_factor':greedy_factor,
            'lp_rounded_factor':lp_rounded_factor
        })
        print(f"Greedy cover: {greedy_cover}, LP cover: {lp_rounded_cover}")
        print()

    return approx_factor

# Initialize an empty list to store all results
all_results = []

# Loop over your nodes
for i in range(10, 21, 10):
    results = program(i)
    for res in results:
        all_results.append({
            "Nodes": i,
            "Edges": res["edges"],
            "Greedy_Factor": res["greedy_factor"],
            "LP_Rounded_Factor": res["lp_rounded_factor"]
        })

# Convert to a DataFrame
df = pd.DataFrame(all_results)

# Optionally, reorder columns
df = df[["Nodes", "Edges", "Greedy_Factor", "LP_Rounded_Factor"]]

# Save to CSV
df.to_csv("results4.csv", index=False)

print("CSV file generated: approximation_summary.csv")