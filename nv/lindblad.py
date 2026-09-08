"""Lindblad dynamics for the NV-center ground state."""

import numpy as np
import qutip as qt


def dephasing_collapse_operator(rate):
    """Return a pure-dephasing collapse operator."""
    sz = qt.jmat(1, "z")
    return np.sqrt(rate) * sz


def evolve_density_matrix(
    hamiltonian,
    initial_state,
    times,
    dephasing_rate=0.0,
):
    """Evolve an NV density matrix under Lindblad dynamics."""
    collapse_operators = []

    if dephasing_rate > 0.0:
        collapse_operators.append(
            dephasing_collapse_operator(dephasing_rate)
        )

    result = qt.mesolve(
        2.0 * np.pi * hamiltonian,
        initial_state,
        times,
        c_ops=collapse_operators,
    )

    return result


def coherence(rho):
    """Return the magnitude of the ground-state coherence."""
    return abs(rho[1, 0])
