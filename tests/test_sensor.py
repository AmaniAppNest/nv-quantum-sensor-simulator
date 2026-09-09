import numpy as np
import pytest

from nv.sensor import NVSensor


def test_sensor_normalizes_orientation():
    sensor = NVSensor(
        position=[1.0, 2.0, 3.0],
        orientation=[1.0, 1.0, 1.0],
    )

    assert np.isclose(np.linalg.norm(sensor.orientation), 1.0)
    assert np.allclose(
        sensor.orientation,
        np.array([1.0, 1.0, 1.0]) / np.sqrt(3.0),
    )


def test_sensor_preserves_position():
    sensor = NVSensor(
        position=[1e-6, 2e-6, 3e-6],
        orientation=[0.0, 0.0, 1.0],
    )

    assert np.allclose(
        sensor.position,
        np.array([1e-6, 2e-6, 3e-6]),
    )


def test_sensor_distance_to_point():
    sensor = NVSensor(
        position=[0.0, 0.0, 0.0],
        orientation=[0.0, 0.0, 1.0],
    )

    distance = sensor.distance_to([3e-6, 4e-6, 0.0])

    assert np.isclose(distance, 5e-6)


def test_sensor_rejects_invalid_position():
    with pytest.raises(ValueError):
        NVSensor(
            position=[0.0, 0.0],
            orientation=[0.0, 0.0, 1.0],
        )


def test_sensor_rejects_zero_orientation():
    with pytest.raises(ValueError):
        NVSensor(
            position=[0.0, 0.0, 0.0],
            orientation=[0.0, 0.0, 0.0],
        )