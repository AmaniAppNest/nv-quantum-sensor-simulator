import numpy as np
import pytest

from fem.field_data import FieldData
from nv.sensor import NVSensor


def test_field_data_accepts_spatial_samples():
    field = FieldData(
        positions=[[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]],
        values=[10.0, 20.0],
        name="temperature",
        units="K",
    )

    assert field.n_points == 2
    assert field.name == "temperature"
    assert field.units == "K"


def test_field_data_nearest_value():
    field = FieldData(
        positions=[
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
        ],
        values=[10.0, 20.0],
    )

    assert field.nearest_value([0.9, 0.0, 0.0]) == 20.0


def test_field_data_rejects_invalid_positions():
    with pytest.raises(ValueError):
        FieldData(
            positions=[[0.0, 0.0]],
            values=[10.0],
        )


def test_field_data_rejects_mismatched_values():
    with pytest.raises(ValueError):
        FieldData(
            positions=[
                [0.0, 0.0, 0.0],
                [1.0, 0.0, 0.0],
            ],
            values=[10.0],
        )


def test_field_data_rejects_empty_data():
    with pytest.raises(ValueError):
        FieldData(
            positions=np.empty((0, 3)),
            values=np.empty(0),
        )


def test_field_data_value_at_sensor():
    field = FieldData(
        positions=[
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
        ],
        values=[10.0, 20.0],
    )

    sensor = NVSensor(
        position=[0.9, 0.0, 0.0],
        orientation=[0.0, 0.0, 1.0],
    )

    assert field.value_at_sensor(sensor) == 20.0 