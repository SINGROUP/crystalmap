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

Diamond2 = ase.build.bulk(
    name="C",
    crystalstructure="diamond",
    a=3.567,
)
Diamond2.rattle(stdev=0.1)
Diamond2.wrap()

NaCl = ase.build.bulk(
    name="NaCl",
    crystalstructure="rocksalt",
    a=5.64,
)
NaCl.wrap()

NaCl2 = ase.build.bulk(
    name="NaCl",
    crystalstructure="rocksalt",
    a=6,
)
NaCl2.wrap()

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

Cu2 = ase.build.bulk(
    name="Cu",
    crystalstructure="fcc",
    a=3.20,
)

GaAs = ase.build.bulk(
    name="GaAs",
    crystalstructure="zincblende",
    a=5.653,
)

GaAs2 = ase.build.bulk(
    name="GaAs",
    crystalstructure="zincblende",
    a=5.653,
)
GaAs2.rattle(stdev=0.1)
GaAs2.wrap()

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

CsCl2 = ase.build.bulk(
    name="CsCl",
    crystalstructure="cesiumchloride",
    a=4.123,
)
CsCl2.rattle(stdev=0.1)
CsCl2.wrap()

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
    "Diamond2": {
        "atoms": Diamond2
    },
    "NaCl": {
        "atoms": NaCl
    },
    "NaCl2": {
        "atoms": NaCl2
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
    "Cu2": {
        "atoms": Cu2
    },
    "GaAs": {
        "atoms": GaAs
    },
    "GaAs2": {
        "atoms": GaAs2
    },
    "SiC": {
        "atoms": SiC
    },
    "CsCl": {
        "atoms": CsCl
    },
    "CsCl2": {
        "atoms": CsCl2
    },
}
with open("test.pickle", "wb") as fout:
    pickle.dump(geoms, fout)
