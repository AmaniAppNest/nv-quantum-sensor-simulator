import numpy as np
import pytest

from nv.control import (
    ControlConfiguration,
    select_control_configuration,
)


def test_control_configuration_validates_sequence():
    configuration = ControlConfiguration(
        name="hahn_echo",
        sequence=(1e-6, 2e-6, 1e-6),
    )

    assert configuration.name == "hahn_echo"
    assert configuration.sequence == (1e-6, 2e-6, 1e-6)
    assert np.isclose(configuration.duration, 4e-6)


def test_control_configuration_rejects_empty_name():
    with pytest.raises(ValueError):
        ControlConfiguration(
            name="",
            sequence=(1e-6,),
        )


def test_control_configuration_rejects_invalid_sequence():
    with pytest.raises(ValueError):
        ControlConfiguration(
            name="invalid",
            sequence=(-1e-6,),
        )


def test_select_control_configuration_returns_best():
    first = ControlConfiguration(
        name="short",
        sequence=(1e-6, 1e-6),
    )

    second = ControlConfiguration(
        name="long",
        sequence=(1e-6, 2e-6, 1e-6),
    )

    selected = select_control_configuration(
        configurations=[first, second],
        objective_values=[0.4, 0.8],
    )

    assert selected == second


def test_select_control_configuration_rejects_empty_input():
    with pytest.raises(ValueError):
        select_control_configuration(
            configurations=[],
            objective_values=[],
        )