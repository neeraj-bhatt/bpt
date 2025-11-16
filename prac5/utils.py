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
def run_experiment(name, X, k, filename="output.txt"):
    with open(filename, "a") as f:   # append mode
        f.write(f"\n========== {name} ==========\n")
        f.write(f"n_samples: {X.shape[0]}  dim: {X.shape[1]}\n")

        # Heuristic using KMeans
        t0 = time()
        kmeans = MiniBatchKMeans(n_clusters=k, random_state=42).fit(X)
        t1 = time()
        km_cost = k_center_cost(X, kmeans.cluster_centers_)
        km_time = t1-t0

        f.write("\nKMeans Heuristic:\n")
        f.write(f"   Cost: {km_cost}\n")
        f.write(f"   Time: {km_time}\n")

        # Greedy 2-Approx
        t0 = time()
        centers = farthest_first_k_center_2_factor(X, k)
        t1 = time()
        app_cost = k_center_cost(X, centers)
        app_time = t1-t0

        f.write("\nGreedy 2-Approx:\n")
        f.write(f"   Cost: {app_cost}\n")
        f.write(f"   Time: {t1 - t0}\n")

    return {
        "name": name,
        "kmeans_cost": km_cost,
        "kmeans_time": km_time,
        "ff_cost": app_cost,
        "ff_time": app_time
    }

