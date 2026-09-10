import numpy as np
import pytest
import torch

from nv.control import (
    ControlConfiguration,
    StochasticControlPolicy,
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


def test_stochastic_control_policy_returns_probabilities():
    policy = StochasticControlPolicy(
        state_dimension=5,
        number_of_configurations=3,
    )

    state = np.zeros(5)
    probabilities = policy.probabilities(state)

    assert isinstance(probabilities, torch.Tensor)
    assert probabilities.shape == (3,)
    assert torch.all(probabilities >= 0.0)
    assert torch.isclose(
        probabilities.sum(),
        torch.tensor(1.0),
    )


def test_stochastic_control_policy_samples_valid_configuration():
    policy = StochasticControlPolicy(
        state_dimension=5,
        number_of_configurations=3,
    )

    state = np.zeros(5)
    configuration_index = policy.sample(state)

    assert 0 <= configuration_index < 3


def test_stochastic_control_policy_returns_log_probability():
    policy = StochasticControlPolicy(
        state_dimension=5,
        number_of_configurations=3,
    )

    state = np.zeros(5)
    log_probability = policy.log_probability(
        state,
        configuration_index=1,
    )

    assert isinstance(log_probability, torch.Tensor)
    assert log_probability.ndim == 0
    assert torch.isfinite(log_probability)


def test_stochastic_control_policy_rejects_invalid_state():
    policy = StochasticControlPolicy(
        state_dimension=5,
        number_of_configurations=3,
    )

    with pytest.raises(ValueError):
        policy.probabilities(np.zeros(4))


def test_stochastic_control_policy_updates_with_reward():
    policy = StochasticControlPolicy(
        state_dimension=5,
        number_of_configurations=3,
    )

    optimizer = torch.optim.Adam(
        policy.parameters(),
        lr=0.01,
    )

    state = np.zeros(5)
    configuration_index = 1

    before = [
        parameter.detach().clone()
        for parameter in policy.parameters()
    ]

    policy.policy_gradient_update(
        state=state,
        configuration_index=configuration_index,
        reward=1.0,
        optimizer=optimizer,
    )

    after = list(policy.parameters())

    assert any(
        not torch.equal(
            before_parameter,
            after_parameter.detach(),
        )
        for before_parameter, after_parameter in zip(before, after)
    )


def test_physics_informed_reward_prefers_higher_sensing_signal():
    from nv.control import physics_informed_reward

    high_signal = physics_informed_reward(
        sensing_signal=0.9,
        sequence_duration=2.0e-6,
        duration_weight=1.0e5,
    )

    low_signal = physics_informed_reward(
        sensing_signal=0.6,
        sequence_duration=2.0e-6,
        duration_weight=1.0e5,
    )

    assert high_signal > low_signal


def test_physics_informed_reward_penalizes_longer_sequences():
    from nv.control import physics_informed_reward

    short_sequence = physics_informed_reward(
        sensing_signal=0.8,
        sequence_duration=1.0e-6,
        duration_weight=1.0e5,
    )

    long_sequence = physics_informed_reward(
        sensing_signal=0.8,
        sequence_duration=3.0e-6,
        duration_weight=1.0e5,
    )

    assert short_sequence > long_sequence


def test_physics_informed_reward_rejects_invalid_signal():
    from nv.control import physics_informed_reward

    with pytest.raises(ValueError):
        physics_informed_reward(
            sensing_signal=1.2,
            sequence_duration=1.0e-6,
        )