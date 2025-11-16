import numpy as np
from sklearn.metrics import pairwise_distances
from sklearn.cluster import MiniBatchKMeans
from time import time


# Compute k-center cost: max distance from any point to the closest chosen center
def k_center_cost(X, centers):
    D = pairwise_distances(X, centers)
    return np.min(D, axis=1).max()

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

# Function to run the experiment on five real dataset
def run_experiment(name, X, k):
    print(f"\n========== {name} ==========")
    print("n_samples:", X.shape[0], "dim:", X.shape[1])

    # Heuristic using KMeans
    t0 = time()
    kmeans = MiniBatchKMeans(n_clusters=k, random_state=42).fit(X)
    t1 = time()
    km_cost = k_center_cost(X, kmeans.cluster_centers_)

    print("\nKMeans Heuristic:")
    print("   Cost:", km_cost)
    print("   Time:", t1 - t0)

    # Greedy 2-Approx
    t0 = time()
    centers = farthest_first_k_center_2_factor(X, k)
    t1 = time()
    ff_cost = k_center_cost(X, centers)

    print("\nGreedy 2-Approx:")
    print("   Cost:", ff_cost)
    print("   Time:", t1 - t0)
