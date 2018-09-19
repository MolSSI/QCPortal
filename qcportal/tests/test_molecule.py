"""
Tests the imports and exports of the Molecule object.
"""

import numpy as np
import pytest
from . import portal


def test_molecule_constructors():

    ### Water Dimer
    water_psi = portal.data.get_molecule("water_dimer_minima.psimol")
    ele = np.array([8, 1, 1, 8, 1, 1]).reshape(-1, 1)
    npwater = np.hstack((ele, water_psi.geometry))
    water_from_np = portal.Molecule(npwater, name="water dimer", dtype="numpy", frags=[3])

    assert water_psi.compare(water_psi, water_from_np)
    assert water_psi.get_molecular_formula() == "H4O2"

    # Check the JSON construct/deconstruct
    water_from_json = portal.Molecule(water_psi.to_json(), dtype="json")
    assert water_psi.compare(water_psi, water_from_json)

    ### Neon Tetramer
    neon_from_psi = portal.data.get_molecule("neon_tetramer.psimol")
    ele = np.array([10, 10, 10, 10]).reshape(-1, 1)
    npneon = np.hstack((ele, neon_from_psi.geometry))
    neon_from_np = portal.Molecule(npneon, name="neon tetramer", dtype="numpy", frags=[1, 2, 3], units="bohr")

    assert neon_from_psi.compare(neon_from_psi, neon_from_np)

    # Check the JSON construct/deconstruct
    neon_from_json = portal.Molecule(neon_from_psi.to_json(), dtype="json")
    assert neon_from_psi.compare(neon_from_psi, neon_from_json)
    assert neon_from_json.get_molecular_formula() == "Ne4"

    assert water_psi.compare(portal.Molecule(water_psi.to_string()))


def test_molecule_file_constructors():

    mol_psi = portal.data.get_molecule("helium_dimer.psimol")
    mol_json = portal.data.get_molecule("helium_dimer.json")
    mol_np = portal.data.get_molecule("helium_dimer.npy")

    assert mol_psi.compare(mol_json)
    assert mol_psi.compare(mol_np)
    assert mol_psi.get_molecular_formula() == "He2"


def test_water_minima_data():
    mol = portal.data.get_molecule("water_dimer_minima.psimol")
    mol.name = "water dimer"

    assert len(str(mol)) == 662
    assert len(mol.to_string()) == 442

    assert sum(x == y for x, y in zip(mol.symbols, ['O', 'H', 'H', 'O', 'H', 'H'])) == mol.geometry.shape[0]
    assert mol.name == "water dimer"
    assert mol.charge == 0
    assert mol.multiplicity == 1
    assert np.sum(mol.real) == mol.geometry.shape[0]
    assert np.allclose(mol.fragments, [[0, 1, 2], [3, 4, 5]])
    assert np.allclose(mol.fragment_charges, [0, 0])
    assert np.allclose(mol.fragment_multiplicities, [1, 1])
    assert hasattr(mol, "provenance")
    assert np.allclose(
        mol.geometry,
        [[2.81211080, 0.1255717, 0.], [3.48216664, -1.55439981, 0.], [1.00578203, -0.1092573, 0.],
         [-2.6821528, -0.12325075, 0.], [-3.27523824, 0.81341093, 1.43347255], [-3.27523824, 0.81341093, -1.43347255]])
    assert mol.get_hash() == "358ad4bb4620e35cec79b17ec0f40acae1a548cb"


def test_water_minima_fragment():

    mol = portal.data.get_molecule("water_dimer_minima.psimol")

    frag_0 = mol.get_fragment(0, orient=True)
    frag_1 = mol.get_fragment(1, orient=True)
    assert frag_0.get_hash() == "4cd68e5dde15c19fc2f5101d5fc5f19ac8afbc9c"
    assert frag_1.get_hash() == "da635a2e012a9ea876ea54422256bd93124e4271"

    frag_0_1 = mol.get_fragment(0, 1)
    frag_1_0 = mol.get_fragment(1, 0)

    assert mol.symbols[:3] == frag_0.symbols
    assert np.allclose(mol.masses[:3], frag_0.masses)

    assert mol.symbols == frag_0_1.symbols
    assert np.allclose(mol.geometry, frag_0_1.geometry)

    assert mol.symbols[3:] + mol.symbols[:3] == frag_1_0.symbols
    assert np.allclose(mol.masses[3:] + mol.masses[:3], frag_1_0.masses)


def test_pretty_print():

    mol = portal.data.get_molecule("water_dimer_minima.psimol")
    assert isinstance(mol.pretty_print(), str)


def test_to_string():

    mol = portal.data.get_molecule("water_dimer_minima.psimol")
    assert isinstance(mol.to_string(), str)


def test_water_orient():
    # These are identical molecules, should find the correct results

    mol = portal.data.get_molecule("water_dimer_stretch.psimol")
    frag_0 = mol.get_fragment(0, orient=True)
    frag_1 = mol.get_fragment(1, orient=True)

    # Make sure the fragments match
    assert frag_0.get_hash() == frag_1.get_hash()

    # Make sure the complexes match
    frag_0_1 = mol.get_fragment(0, 1, orient=True)
    frag_1_0 = mol.get_fragment(1, 0, orient=True)

    assert frag_0_1.get_hash() == frag_1_0.get_hash()

    mol = portal.data.get_molecule("water_dimer_stretch2.psimol")
    frag_0 = mol.get_fragment(0, orient=True)
    frag_1 = mol.get_fragment(1, orient=True)

    # Make sure the fragments match
    assert frag_0.multiplicity == 1
    assert frag_0.get_hash() == frag_1.get_hash()

    # Make sure the complexes match
    frag_0_1 = mol.get_fragment(0, 1, orient=True)
    frag_1_0 = mol.get_fragment(1, 0, orient=True)

    # Ghost fragments should prevent overlap
    assert frag_0_1.multiplicity == 1
    assert frag_0_1.get_hash() != frag_1_0.get_hash()


def test_molecule_errors():
    mol = portal.data.get_molecule("water_dimer_stretch.psimol")

    data = mol.to_json()
    data["whatever"] = 5
    with pytest.raises(ValueError):
        portal.schema.validate(data, "molecule")


def test_molecule_repeated_hashing():

    mol = portal.Molecule({
        'symbols': ['H', 'O', 'O', 'H'],
        'geometry': [
            1.73178198, 1.29095807, 1.03716028, 1.31566305, -0.007440200000000001, -0.28074722, -1.3143081, 0.00849608,
            -0.27416914, -1.7241109, -1.30793432, 1.02770172
        ]
    })

    h1 = mol.get_hash()
    assert mol.get_molecular_formula() == "H2O2"

    mol2 = portal.Molecule(mol.to_json(), orient=False)
    assert h1 == mol2.get_hash()

    mol3 = portal.Molecule(mol2.to_json(), orient=False)
    assert h1 == mol3.get_hash()
