import pickle

path = "../../../Articles/article-describe/results/data/crystals/oqmd_all_converged.pickle"
with open(path, "rb") as fin:
    data = pickle.load(fin, encoding='latin1')

# Filter out III-V semiconductors
for sample in data.values():
    print(sample.keys())
    atoms = sample["atoms"]
    band_gap = sample["band_gap"]

    elements = set(atoms.get_chemical_symbols())
    threefive = ""
    break
