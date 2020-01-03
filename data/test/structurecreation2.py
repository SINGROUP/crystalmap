"""
Creates a few atomic structures for testing out the creation of a crystal
structure map.
"""
import ase.build
import pickle
from ase.visualize import view

index = 0
geoms = {}
a = 3.567
diamond = ase.build.bulk(
    name="C",
    crystalstructure="diamond",
    a=a,
)
for i in range(10):
    idiam = diamond.copy()
    idiam.rattle(stdev=0.01*a, seed=index)
    idiam.wrap()
    index += 1
    geoms[index] = {
        "atoms": idiam,
        "prototype": "diamond",
        "formula": idiam.get_chemical_formula(),
    }

a = 5.431
si = ase.build.bulk(
    name="Si",
    crystalstructure="diamond",
    a=a,
)
for i in range(10):
    isi = si.copy()
    isi.rattle(stdev=0.01*a, seed=index)
    isi.wrap()
    index += 1
    geoms[index] = {
        "atoms": isi,
        "prototype": "diamond",
        "formula": isi.get_chemical_formula(),
    }

a = 5.64
nacl = ase.build.bulk(
    name="NaCl",
    crystalstructure="rocksalt",
    a=a,
)
for i in range(10):
    inacl = nacl.copy()
    inacl.rattle(stdev=0.01*a, seed=index)
    inacl.wrap()
    index += 1
    geoms[index] = {
        "atoms": inacl,
        "prototype": "rocksalt",
        "formula": inacl.get_chemical_formula(),
    }

a = 4.046
al = ase.build.bulk(
    name="Al",
    crystalstructure="fcc",
    a=a,
)
for i in range(10):
    isys = al.copy()
    isys.rattle(stdev=0.01*a, seed=index)
    isys.wrap()
    index += 1
    geoms[index] = {
        "atoms": isys,
        "prototype": "fcc",
        "formula": isys.get_chemical_formula(),
    }

with open("test.pickle", "wb") as fout:
    pickle.dump(geoms, fout)

# Fe = ase.build.bulk(
    # name="Fe",
    # crystalstructure="bcc",
    # a=2.856,
# )

# Cu = ase.build.bulk(
    # name="Cu",
    # crystalstructure="fcc",
    # a=3.597,
# )

# Cu2 = ase.build.bulk(
    # name="Cu",
    # crystalstructure="fcc",
    # a=3.20,
# )

# GaAs = ase.build.bulk(
    # name="GaAs",
    # crystalstructure="zincblende",
    # a=5.653,
# )

# GaAs2 = ase.build.bulk(
    # name="GaAs",
    # crystalstructure="zincblende",
    # a=5.653,
# )
# GaAs2.rattle(stdev=0.1)
# GaAs2.wrap()

# SiC = ase.build.bulk(
    # name="SiC",
    # crystalstructure="wurtzite",
    # a=3.086,
    # c=10.053,
# )

# CsCl = ase.build.bulk(
    # name="CsCl",
    # crystalstructure="cesiumchloride",
    # a=4.123,
# )

# CsCl2 = ase.build.bulk(
    # name="CsCl",
    # crystalstructure="cesiumchloride",
    # a=4.123,
# )
# CsCl2.rattle(stdev=0.1)
# CsCl2.wrap()

# # view(Si)
# view(Diamond)
# view(Diamond2)
# # view(NaCl)
# # view(Al)
# # view(fe)
# # view(Cu)
# # view(GaAs)
# # view(SiC)
# # view(CsCl)

# geoms = {
    # "Si": {
        # "atoms": Si
    # },
    # "Diamond": {
        # "atoms": Diamond
    # },
    # "Diamond2": {
        # "atoms": Diamond2
    # },
    # "NaCl": {
        # "atoms": NaCl
    # },
    # "NaCl2": {
        # "atoms": NaCl2
    # },
    # "Al": {
        # "atoms": Al
    # },
    # "Fe": {
        # "atoms": Fe
    # },
    # "Cu": {
        # "atoms": Cu
    # },
    # "Cu2": {
        # "atoms": Cu2
    # },
    # "GaAs": {
        # "atoms": GaAs
    # },
    # "GaAs2": {
        # "atoms": GaAs2
    # },
    # "SiC": {
        # "atoms": SiC
    # },
    # "CsCl": {
        # "atoms": CsCl
    # },
    # "CsCl2": {
        # "atoms": CsCl2
    # },
# }
