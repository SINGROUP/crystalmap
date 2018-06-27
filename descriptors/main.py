# import scipy.sparse
from creatembtr import create_parallel
from describe.descriptors import MBTR
import describe.utils
import pickle
import numpy as np
import matplotlib.pyplot as mpl

# Open the dataset
inp = "../data/test/test.pickle"
out = "./"
nsamples = None
ncores = 4
with open(inp, "rb") as fin:
    dataset = pickle.load(fin)

# Find out statistics about the dataset. These are used when initializing the
# MBTR setup.
samples = [dataset[x]["atoms"] for x in dataset.keys()]
stats = describe.utils.system_stats(samples)
atomic_numbers = stats["atomic_numbers"]
min_distance = stats["min_distance"]

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
    mpl.plot(x, merged)
    mpl.show()

# TODO: Create a distance matrix between the spectras of all different samples.
# This should produce a (nsamples x nsamples) array. These distancess could
# then be directly used as input for a graph construction.
