import numpy as np
import qutip as qt

from nv.hamiltonian import nv_hamiltonian


def test_hahn_echo_with_dephasing():
    tau = 1.0e-6
    dephasing_rate = 1.0e6

    hamiltonian = nv_hamiltonian(
        magnetic_field=[0.0, 0.0, 1.0e-3],
    )

    ms_zero = qt.basis(3, 1)
    ms_plus = qt.basis(3, 0)

    initial_state = (ms_zero + ms_plus).unit()
    initial_density_matrix = initial_state.proj()

    pi_pulse = qt.jmat(1, "x")

    collapse_operators = [
        np.sqrt(dephasing_rate) * qt.jmat(1, "z")
    ]

    times = np.linspace(0.0, tau, 101)

    first_evolution = qt.mesolve(
        2.0 * np.pi * hamiltonian,
        initial_density_matrix,
        times,
        c_ops=collapse_operators,
    )

    state_after_first = first_evolution.states[-1]

    pulse_unitary = (-1j * np.pi / 2 * pi_pulse).expm()

    state_after_pulse = (
        pulse_unitary
        * state_after_first
        * pulse_unitary.dag()
    )

    second_evolution = qt.mesolve(
        2.0 * np.pi * hamiltonian,
        state_after_pulse,
        times,
        c_ops=collapse_operators,
    )

    final_state = second_evolution.states[-1]

    coherence = abs(final_state[1, 0])

    assert np.isfinite(coherence)
    assert 0.0 <= coherence <= 0.5 