import numpy as np
import random as rd
from scipy.optimize import linprog

# Vertex Cover with greedy approach - FIXED
def vertex_cover_greedy(edges):
    vertex_cover = set()
    
    # Make a copy of edges to work with
    remaining_edges = edges.copy()
    
    # while remaining_edges:
    #     # Count degree of each vertex in remaining edges
    #     degree = {}
    #     for u, v in remaining_edges:
    #         degree[u] = degree.get(u, 0) + 1
    #         degree[v] = degree.get(v, 0) + 1
        
    #     # Find vertex with maximum degree
    #     max_vertex = max(degree.items(), key=lambda x: x[1])[0]
        
    #     # Add to cover and remove all incident edges
    #     vertex_cover.add(max_vertex)
    #     remaining_edges = [(u, v) for u, v in remaining_edges if u != max_vertex and v != max_vertex]

    for edge in edges:
        u, v = edge
        if u not in vertex_cover and v not in vertex_cover:
            vertex_cover.add(u)

    return vertex_cover
    


# Solves LP relaxation for vertex cover - FIXED
def lp_relaxation(n, m, edges_list):
    # Define the LP coefficient (minimize sum of x_i)
    c = np.ones(n)

    # Constraints: x_u + x_v >= 1 for each edge (u, v)
    # We express as -x_u - x_v <= -1
    ineq_A = np.zeros((m, n))
    ineq_b = -np.ones(m)  # -1 for each constraint

    for i, (u, v) in enumerate(edges_list):
        ineq_A[i, u-1] = -1  # Negative coefficients
        ineq_A[i, v-1] = -1
    
    # Solve LP problem: minimize c.x subject to A_ub.x <= b_ub
    result = linprog(c, A_ub=ineq_A, b_ub=ineq_b, bounds=[(0, 1)] * n, method='highs')

    if result.success:
        print("LP solution:", np.round(result.x, 3))
        return result.x
    else:
        print(f"LP relaxation failed for {m} edges: {result.message}")
        return None


# Round LP solution to obtain an approximate vertex cover - FIXED
def round_lp_solution(lp_solution):
    # Convert back to 1-based vertex numbering
    return {i+1 for i, x in enumerate(lp_solution) if x >= 0.5}


# Calculate approximation factor
def approximation_factor(greedy_cover, lp_cover):
    if len(lp_cover) == 0:
        print("LP cover is empty, skipping approximation factor calculation.")
        return 0
    return len(greedy_cover) / len(lp_cover)


def program(nodes):
    # All possible edges
    all_possible_edges = [(u, v) for u in range(1, nodes + 1) for v in range(u + 1, nodes + 1)]
    
    # Use reasonable edge sizes for testing
    max_possible_edges = len(all_possible_edges)
    step_size = max(1, max_possible_edges // 5)  # 5 steps
    edges_size = list(range(nodes, min(max_possible_edges + 1, nodes * 4), step_size))
    
    # Ensure we test some sparse and dense graphs
    if edges_size[-1] < max_possible_edges:
        edges_size.append(max_possible_edges)
    
    approx_factor = []
    
    for e in edges_size:
        if e > len(all_possible_edges):
            continue
            
        print(f"------Running experiment for {nodes} nodes and {e} edges------")
        edges = rd.sample(all_possible_edges, e)

        # LP
        lp_solution = lp_relaxation(nodes, e, edges)
        if lp_solution is None:
            print(f"LP Relaxation failed for {e} edges.")
            continue
            
        lp_cover = round_lp_solution(lp_solution)

        # Greedy
        greedy_cover = vertex_cover_greedy(edges)
        
        factor = approximation_factor(greedy_cover, lp_cover)
        approx_factor.append(factor)
        print(f"Greedy cover size: {len(greedy_cover)}, LP cover size: {len(lp_cover)}, Approximation factor: {factor:.2f}")
        print(f"Greedy cover: {greedy_cover}, LP cover: {lp_cover}")
        print()
    
    return approx_factor


# Test with a smaller graph first to verify
print("Testing with small graph...")
test_edges = [(1, 2), (1, 3), (2, 3), (2, 4), (3, 4)]
n = 4
m = 5

lp_sol = lp_relaxation(n, m, test_edges)
if lp_sol is not None:
    lp_cov = round_lp_solution(lp_sol)
    greedy_cov = vertex_cover_greedy(test_edges)
    print(f"Test case - Greedy: {greedy_cov}, LP: {lp_cov}")
    print(f"Test case - Greedy size: {len(greedy_cov)}, LP size: {len(lp_cov)}")
    print()

# Run main program
print("Running main program...")
app_factor = program(10)  # Start with smaller graph
print("Approximation factors:", app_factor)