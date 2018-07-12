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

keys = list(dataset.keys())[:2000]

new_dataset = {}
for key in keys:
    i_atoms = dataset[key]["atoms"]
    n_atoms = len(i_atoms)
    if n_atoms < 20:
        new_dataset[key] = dataset[key]
dataset = new_dataset

# print(dataset[keys[0]].keys())
# print(dataset[keys[0]]["lattice_system_relax"])

# Find out statistics about the dataset. These are used when initializing the
# MBTR setup.
samples = [dataset[x]["atoms"] for x in keys]
stats = describe.utils.system_stats(samples)
atomic_numbers = stats["atomic_numbers"]
min_distance = stats["min_distance"]

#print(atomic_numbers)

# Define the MBTR settings
k = 2
sigma = 0.02
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
num_samples = mbtr.shape[0]
# scipy.sparse.save_npz(".mbtr.npz", mbtr)

# Create a spectra where all pairwise distances have been merged
merged_mbtr = np.zeros((num_samples, 100))
n_pairs = int(mbtr.shape[1]/n)
for i, i_mbtr in enumerate(mbtr):

    # The individual pairwise spectra are summed up along one axis.
    merged = i_mbtr.reshape((n_pairs, n))
    merged = merged.sum(axis=0).A1
    x = np.arange(merged.shape[0])

    # For plotting the spectra
    #mpl.plot(x, merged)
    #mpl.show()
    merged_mbtr[i, :] = merged

# Create the links
links = []
for i in range(num_samples):
    for j in range(num_samples):

        # Only take the upper diagonal part of the connectivity matrix
        if j > i:
            i_mbtr = merged_mbtr[i, :]
            j_mbtr = merged_mbtr[j, :]
            # i_mbtr = mbtr[i, :]
            # j_mbtr = mbtr[j, :]
            diff = i_mbtr - j_mbtr
            # d = scipy.sparse.linalg.norm(diff)
            d = np.linalg.norm(diff)
            ij_link = {"source": i, "target": j, "value": d}

            # In order to keep the size of the file maintainable, we will discard
            # links that are above a cutoff distance.
            if d < 10:
                links.append(ij_link)

# Creating nodes
nodes = []
sorted_keys = sorted(dataset.keys())
for i in range(num_samples):
    entry = dataset[sorted_keys[i]]
    i_node = {
        "id": i,
        "lattice_system": entry["lattice_system_relax"],
        "aflow_id": sorted_keys[i],
        "formula": entry["atoms"].get_chemical_formula(),
        "spacegroup_relax": entry["spacegroup_relax"],
        "prototype": entry["prototype"],
        "gap_type": entry["gap_type"],
        "bravais_lattice_relax": entry["Bravais_lattice_relax"],
        "gap": entry["gap"],
        "gap_fit": entry["gap_fit"],
        "pearson_symbol_relax": entry["Pearson_symbol_relax"],
        "energy_cell": entry["energy_cell"],
        "icsd": entry["icsd"],
        "natoms": entry["natoms"],
    }
    nodes.append(i_node)

# Saving the graph
graph = {"nodes": nodes, "links": links}
with open("graph.json", "w") as fout:
    json.dump(graph, fout, indent=2)
