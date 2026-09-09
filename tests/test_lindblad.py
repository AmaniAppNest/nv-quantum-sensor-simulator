import numpy as np
import qutip as qt

from nv.hamiltonian import nv_hamiltonian
from nv.lindblad import evolve_density_matrix, coherence


def test_lindblad_evolution_preserves_trace():
    hamiltonian = nv_hamiltonian(
        magnetic_field=[0.0, 0.0, 0.0],
    )

    state = (qt.basis(3, 1) + qt.basis(3, 0)).unit()
    times = np.linspace(0.0, 2.0e-6, 101)

    result = evolve_density_matrix(
        hamiltonian,
        state,
        times,
        dephasing_rate=1.0e6,
    )

    for density_matrix in result.states:
        assert np.isclose(density_matrix.tr(), 1.0)


def test_lindblad_dephasing_reduces_coherence():
    hamiltonian = nv_hamiltonian(
        magnetic_field=[0.0, 0.0, 0.0],
    )

    state = (qt.basis(3, 1) + qt.basis(3, 0)).unit()
    times = np.linspace(0.0, 2.0e-6, 101)

    result = evolve_density_matrix(
        hamiltonian,
        state,
        times,
        dephasing_rate=1.0e6,
    )

    initial_coherence = coherence(result.states[0])
    final_coherence = coherence(result.states[-1])

    assert final_coherence < initial_coherence 