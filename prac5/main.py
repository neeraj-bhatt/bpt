from utils import k_center_cost, farthest_first_k_center_2_factor, k_center_local_search, run_experiment
from sklearn.cluster import MiniBatchKMeans
from sklearn.datasets import load_iris, load_wine, load_breast_cancer, load_digits, fetch_california_housing
from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt
from time import time
from sklearn.utils import resample


# -----------------Test Dataset------------------------
X, _ = make_blobs(n_samples=2000, centers=5, random_state=42)
k = 5

# --- Heuristic KMeans ---
t0 = time()
localCenters = k_center_local_search(X, k)
t1 = time()
km_cost = k_center_cost(X, localCenters)
print("---------------Experiment on Dummy Dataset---------------")
print("Local Search Heuristic:")
print("   Cost:", km_cost)
print("   Time:", t1 - t0, "seconds")

# --- Greedy 2-approx ---
t0 = time()
greedyCenters = farthest_first_k_center_2_factor(X, k)
t1 = time()
ff_cost = k_center_cost(X, greedyCenters)

print("\nGreedy 2-Approx:")
print("   Cost:", ff_cost)
print("   Time:", t1 - t0, "seconds")


# -------------------Real Dataset---------------------
datasets = [
    ("Iris", load_iris().data, 3),
    ("Wine", load_wine().data, 3),
    ("BreastCancer", load_breast_cancer().data, 2),
    ("Digits", load_digits().data, 10),
    ("CaliforniaHousing", resample(fetch_california_housing().data, n_samples=3000, random_state=42), 6),
]

open("output.txt", "w").close()
results = []
for name, X, k in datasets:
    res = run_experiment(name, X, k)
    results.append(res)
