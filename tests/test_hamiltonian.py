import numpy as np

from nv.hamiltonian import nv_hamiltonian


def test_zero_field_degeneracy():
    hamiltonian = nv_hamiltonian(
        magnetic_field=[0.0, 0.0, 0.0],
    )

    energies = np.sort(hamiltonian.eigenenergies())

    assert np.isclose(energies[1], energies[2])


def test_axial_magnetic_field_splits_levels():
    hamiltonian = nv_hamiltonian(
        magnetic_field=[0.0, 0.0, 1.0e-3],
    )

    energies = np.sort(hamiltonian.eigenenergies())

    splitting = energies[2] - energies[1]

    assert np.isclose(splitting, 2.0 * 28.02495164e9 * 1.0e-3) 