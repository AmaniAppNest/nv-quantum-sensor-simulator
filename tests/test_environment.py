import numpy as np
import pytest

from nv.environment import NVEnvironment
from nv.sensor import NVSensor


def test_environment_accepts_physical_state():
    environment = NVEnvironment(
        magnetic_field=[0.0, 0.0, 1.0e-3],
        strain=1.0e-6,
        temperature=300.0,
    )

    assert np.allclose(
        environment.magnetic_field,
        [0.0, 0.0, 1.0e-3],
    )
    assert environment.strain == 1.0e-6
    assert environment.temperature == 300.0


def test_environment_builds_hamiltonian():
    environment = NVEnvironment(
        magnetic_field=[0.0, 0.0, 1.0e-3],
        strain=1.0e-6,
    )

    hamiltonian = environment.hamiltonian()

    assert hamiltonian.shape == (3, 3)


def test_environment_state_vector():
    sensor = NVSensor(
        position=[1.0e-6, 2.0e-6, 3.0e-6],
        orientation=[0.0, 0.0, 1.0],
    )

    environment = NVEnvironment(
        magnetic_field=[1.0e-3, 2.0e-3, 3.0e-3],
        strain=1.0e-6,
        temperature=300.0,
    )

    state = environment.state_vector(sensor)

    assert state.shape == (11,)
    assert np.allclose(state[:3], sensor.position)
    assert np.allclose(state[3:6], sensor.orientation)
    assert np.allclose(state[6:9], environment.magnetic_field)
    assert state[9] == environment.strain
    assert state[10] == environment.temperature


def test_environment_rejects_invalid_magnetic_field():
    with pytest.raises(ValueError):
        NVEnvironment(
            magnetic_field=[0.0, 0.0],
        )


def test_environment_rejects_nonfinite_temperature():
    with pytest.raises(ValueError):
        NVEnvironment(
            magnetic_field=[0.0, 0.0, 0.0],
            temperature=np.nan,
        )