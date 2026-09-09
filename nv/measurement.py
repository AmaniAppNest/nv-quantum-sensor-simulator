"""Measurement models for NV quantum sensing."""

import numpy as np
import qutip as qt


def population_probability(state, basis_state):
    """Return the population probability of a basis state."""
    if not isinstance(state, qt.Qobj):
        raise TypeError("state must be a QuTiP Qobj.")

    if not isinstance(basis_state, qt.Qobj):
        raise TypeError("basis_state must be a QuTiP Qobj.")

    return float(abs(basis_state.dag() * state) ** 2)


def coherence_signal(state):
    """Return the magnitude of the ground-state coherence."""
    if not isinstance(state, qt.Qobj):
        raise TypeError("state must be a QuTiP Qobj.")

    density_matrix = state * state.dag() if state.isket else state

    return float(abs(density_matrix[1, 0]))


def measurement_signal(state):
    """Return a normalized NV sensing signal."""
    coherence = coherence_signal(state)
    return float(np.clip(2.0 * coherence, 0.0, 1.0))