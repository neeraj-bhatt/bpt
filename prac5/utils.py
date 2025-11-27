import numpy as np
import pandas as pd
from sklearn.metrics import pairwise_distances
from sklearn.cluster import MiniBatchKMeans
from time import time
from copy import deepcopy


# Compute k-center cost: max distance from any point to the closest chosen center
def k_center_cost(X, centers):
    D = pairwise_distances(X, centers)
    return np.min(D, axis=1).max()

# Local Search Heuristic
def k_center_local_search(X, k, max_iter=20):
    # start with greedy solution
    current_centers = farthest_first_k_center_2_factor(X, k)

    current_cost = k_center_cost(X, current_centers)
    
    for _ in range(max_iter):
        improved = False
        for i in range(k):
            for j in range(len(X)):
                new_centers = deepcopy(current_centers)
                new_centers[i] = X[j]  # swap center i with point j
                
                new_cost = k_center_cost(X, new_centers)
                if new_cost < current_cost:
                    current_cost = new_cost
                    current_centers = new_centers
                    improved = True
                    break
            if improved:
                break
        
        if not improved:
            break
        
    return current_centers



# Greedy 2-approximation: Farthest-First Traversal
def farthest_first_k_center_2_factor(X, k):
    n = X.shape[0]
    centers = []

    # Pick an arbitrary first center
    centers.append(X[np.random.randint(0, n)])

    for _ in range(1, k):
        D = pairwise_distances(X, np.array(centers))
        farthest_idx = np.argmax(np.min(D, axis=1))
        centers.append(X[farthest_idx])

    return np.array(centers)


# Initialize an empty DataFrame
results_df = pd.DataFrame(columns=[
    "name", "n_samples", "dim",
    "localsearch_cost", "localsearch_time",
    "ff_cost", "ff_time"
])

# Function to run the experiment on five real dataset
def run_experiment(name, X, k):
    # Heuristic
    t0 = time()
    localSearchcenters = k_center_local_search(X, k)
    t1 = time()
    ls_cost = k_center_cost(X, localSearchcenters)
    ls_time = t1 - t0

    # Greedy 2-Approx
    t0 = time()
    greedyCenters = farthest_first_k_center_2_factor(X, k)
    t1 = time()
    ff_cost = k_center_cost(X, greedyCenters)
    ff_time = t1 - t0

    # Create a dictionary for this row
    row = {
        "name": name,
        "n_samples": X.shape[0],
        "dim": X.shape[1],
        "localsearch_cost": ls_cost,
        "localsearch_time": ls_time,
        "ff_cost": ff_cost,
        "ff_time": ff_time
    }

    # Append to the DataFrame
    global results_df
    results_df = pd.concat([results_df, pd.DataFrame([row])], ignore_index=True)
    results_df.to_csv("results5.csv", index=False)



