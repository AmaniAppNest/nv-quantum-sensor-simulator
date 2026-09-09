"""Simulate a Hahn-echo sequence for the NV ground state."""

import numpy as np
import qutip as qt

from nv.hamiltonian import nv_hamiltonian


tau = 1.0e-6

hamiltonian = nv_hamiltonian(
    magnetic_field=[0.0, 0.0, 1.0e-3],
)

ms_zero = qt.basis(3, 1)
ms_plus = qt.basis(3, 0)

initial_state = (ms_zero + ms_plus).unit()
pi_pulse = qt.jmat(1, "x")

times_1 = np.linspace(0.0, tau, 101)
times_2 = np.linspace(0.0, tau, 101)

first_evolution = qt.sesolve(
    2.0 * np.pi * hamiltonian,
    initial_state,
    times_1,
)

state_after_first = first_evolution.states[-1]
state_after_pulse = (-1j * np.pi / 2 * pi_pulse).expm() * state_after_first

second_evolution = qt.sesolve(
    2.0 * np.pi * hamiltonian,
    state_after_pulse,
    times_2,
)

final_state = second_evolution.states[-1]

coherence = abs(final_state[1, 0])

print(f"Tau: {tau * 1e6:.2f} µs")
print(f"Final coherence: {coherence:.6f}") 