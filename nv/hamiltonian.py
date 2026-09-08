"""NV-center ground-state spin Hamiltonian."""

import numpy as np
import qutip as qt


def spin_1_operators():
    """Return the spin-1 angular momentum operators."""
    sx = qt.jmat(1, "x")
    sy = qt.jmat(1, "y")
    sz = qt.jmat(1, "z")
    return sx, sy, sz


def nv_hamiltonian(
    magnetic_field,
    zero_field_splitting=2.87e9,
    strain=0.0,
    electron_gyromagnetic_ratio=28.02495164e9,
):
    """Construct the NV electronic ground-state Hamiltonian.

    Parameters
    ----------
    magnetic_field:
        Magnetic field vector in tesla.
    zero_field_splitting:
        Ground-state zero-field splitting in hertz.
    strain:
        Effective transverse strain parameter in hertz.
    electron_gyromagnetic_ratio:
        Electron gyromagnetic ratio in hertz per tesla.
    """
    magnetic_field = np.asarray(magnetic_field, dtype=float)

    if magnetic_field.shape != (3,):
        raise ValueError("magnetic_field must contain exactly three components.")

    bx, by, bz = magnetic_field
    sx, sy, sz = spin_1_operators()

    identity = qt.qeye(3)

    h_zero = zero_field_splitting * (
        sz**2 - (2.0 / 3.0) * identity
    )

    h_zeeman = electron_gyromagnetic_ratio * (
        bx * sx + by * sy + bz * sz
    )

    h_strain = strain * (sx**2 - sy**2)

    return h_zero + h_zeeman + h_strain
