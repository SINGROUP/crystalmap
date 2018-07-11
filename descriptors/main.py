# import scipy.sparse
from creatembtr import create_parallel
from describe.descriptors import MBTR
import describe.utils
import pickle
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as mpl
import scipy.sparse.linalg
import json

# Open the dataset
inp = "../data/30k/aflowlib_all_combined.pickle"
out = "./"
nsamples = None
ncores = 4
with open(inp, "rb") as fin:
    dataset = pickle.load(fin)
dataset_new = {}
keys = list(dataset.keys())[0:100]
keys_new = []
for key in keys:
    if len(dataset[key]["atoms"]) < 10:
        dataset_new[key] = dataset[key]
        keys_new.append(key)

dataset = dataset_new
keys = keys_new
print(len(keys_new))

# Find out statistics about the dataset. These are used when initializing the
# MBTR setup.
samples = [dataset[x]["atoms"] for x in keys]
stats = describe.utils.system_stats(samples)
atomic_numbers = stats["atomic_numbers"]
min_distance = stats["min_distance"]

#print(atomic_numbers)

# Define the MBTR settings
k = 2
sigma = 0.01
decay = 0.5
n = 100
mbtr = MBTR(
    atomic_numbers=atomic_numbers,
    k=[k],
    periodic=True,
    grid={
        "k1": {
            "min": min(atomic_numbers)-1,
            "max": max(atomic_numbers)+1,
            "sigma": sigma,
            "n": n,
        },
        "k2": {
            "min": 0,
            "max": 1/min_distance,
            "sigma": sigma,
            "n": n,
        },
        "k2": {
            "min": 0,
            "max": 1,
            "sigma": sigma,
            "n": n,
        },
    },
    weighting={
        "k2": {
            "function": lambda x: np.exp(-decay*x),
            "threshold": 1e-2
        },
        "k3": {
            "function": lambda x: np.exp(-decay*x),
            "threshold": 1e-2
        },
    },
    flatten=True,
)

mbtr = create_parallel(dataset, ncores, nsamples, mbtr)
# scipy.sparse.save_npz(".mbtr.npz", mbtr)

# Create a spectra where all pairwise distances have been merged
n_pairs = int(mbtr.shape[1]/n)
for i_mbtr in mbtr:

    # The individual pairwise spectra are summed up along one axis.
    merged = i_mbtr.reshape((n_pairs, n))
    merged = merged.sum(axis=0).A1
    x = np.arange(merged.shape[0])

    # For plotting the spectra
    #mpl.plot(x, merged)
    #mpl.show()

# TODO: Create a distance matrix between the spectras of all different samples.
# This should produce a (nsamples x nsamples) array. These distancess could
# then be directly used as input for a graph construction.

num_samples = mbtr.shape[0]
links = []

for i in range(num_samples):
    for j in range(num_samples):
        i_mbtr = mbtr[i,:]
        j_mbtr = mbtr[j,:]
        diff = i_mbtr - j_mbtr
        d = scipy.sparse.linalg.norm(diff)
        ij_link = {"source":i,"target":j,"value":10*np.exp(-d*0.1)}
        if ij_link["value"] > 1:
            links.append(ij_link)
        #print(d)

nodes = []

for i in range(num_samples):
    i_node = {"id":i}
    nodes.append(i_node)

graph = {"nodes":nodes,"links":links}

with open("graph.json","w") as fout:
    json.dump(graph,fout,indent=2)