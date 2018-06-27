"""
Creates a few atomic structures for testing out the creation of a crystal
structure map.
"""
import ase.build
import pickle
from ase.visualize import view

Si = ase.build.bulk(
    name="Si",
    crystalstructure="diamond",
    a=5.431,
)

Diamond = ase.build.bulk(
    name="C",
    crystalstructure="diamond",
    a=3.567,
)

NaCl = ase.build.bulk(
    name="NaCl",
    crystalstructure="rocksalt",
    a=5.64,
)
NaCl.wrap()

Al = ase.build.bulk(
    name="Al",
    crystalstructure="fcc",
    a=4.046,
)

Fe = ase.build.bulk(
    name="Fe",
    crystalstructure="bcc",
    a=2.856,
)

Cu = ase.build.bulk(
    name="Cu",
    crystalstructure="fcc",
    a=3.597,
)

GaAs = ase.build.bulk(
    name="GaAs",
    crystalstructure="zincblende",
    a=5.653,
)

SiC = ase.build.bulk(
    name="SiC",
    crystalstructure="wurtzite",
    a=3.086,
    c=10.053,
)

CsCl = ase.build.bulk(
    name="CsCl",
    crystalstructure="cesiumchloride",
    a=4.123,
)

# view(Si)
# view(Diamond)
# view(NaCl)
# view(Al)
# view(fe)
# view(Cu)
# view(GaAs)
# view(SiC)
# view(CsCl)

geoms = {
    "Si": {
        "atoms": Si
    },
    "Diamond": {
        "atoms": Diamond
    },
    "NaCl": {
        "atoms": NaCl
    },
    "Al": {
        "atoms": Al
    },
    "Fe": {
        "atoms": Fe
    },
    "Cu": {
        "atoms": Cu
    },
    "GaAs": {
        "atoms": GaAs
    },
    "SiC": {
        "atoms": SiC
    },
    "CsCl": {
        "atoms": CsCl
    },
}
with open("test.pickle", "wb") as fout:
    pickle.dump(geoms, fout)
