import numpy as np
import qutip as qt

from nv.measurement import (
    coherence_signal,
    measurement_signal,
    population_probability,
)


def test_population_probability_for_basis_state():
    state = qt.basis(3, 1)

    probability = population_probability(state, state)

    assert np.isclose(probability, 1.0)


def test_population_probability_for_orthogonal_state():
    state = qt.basis(3, 1)
    basis_state = qt.basis(3, 0)

    probability = population_probability(state, basis_state)

    assert np.isclose(probability, 0.0)


def test_coherence_signal_for_superposition():
    ms_zero = qt.basis(3, 1)
    ms_plus = qt.basis(3, 0)

    state = (ms_zero + ms_plus).unit()

    coherence = coherence_signal(state)

    assert np.isclose(coherence, 0.5)


def test_measurement_signal_is_normalized():
    ms_zero = qt.basis(3, 1)
    ms_plus = qt.basis(3, 0)

    state = (ms_zero + ms_plus).unit()

    signal = measurement_signal(state)

    assert np.isclose(signal, 1.0)


def test_measurement_signal_for_basis_state():
    state = qt.basis(3, 1)

    signal = measurement_signal(state)

    assert np.isclose(signal, 0.0)