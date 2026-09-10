"""Adaptive and physics-informed control interfaces for NV sensing."""

from dataclasses import dataclass

import numpy as np
import torch
from torch import nn
from torch.distributions import Categorical


@dataclass(frozen=True)
class ControlConfiguration:
    """Represent an admissible quantum-control configuration."""

    name: str
    sequence: tuple[float, ...]

    def __post_init__(self):
        if not self.name:
            raise ValueError("name must not be empty.")

        sequence = np.asarray(self.sequence, dtype=float)

        if sequence.ndim != 1:
            raise ValueError("sequence must be one-dimensional.")

        if sequence.size == 0:
            raise ValueError("sequence must contain at least one value.")

        if not np.isfinite(sequence).all():
            raise ValueError("sequence must contain finite values.")

        if (sequence < 0.0).any():
            raise ValueError("sequence values must be non-negative.")

        object.__setattr__(self, "sequence", tuple(sequence))

    @property
    def duration(self):
        """Return the total duration of the control sequence."""
        return float(np.sum(self.sequence))


def select_control_configuration(
    configurations,
    objective_values,
):
    """Select the configuration with the highest objective value."""
    if len(configurations) == 0:
        raise ValueError("configurations must not be empty.")

    objective_values = np.asarray(objective_values, dtype=float)

    if objective_values.ndim != 1:
        raise ValueError("objective_values must be one-dimensional.")

    if len(configurations) != objective_values.size:
        raise ValueError(
            "configurations and objective_values must have the same length."
        )

    if not np.isfinite(objective_values).all():
        raise ValueError("objective_values must contain finite values.")

    index = int(np.argmax(objective_values))

    return configurations[index]


class StochasticControlPolicy(nn.Module):
    """Represent a stochastic policy over admissible control configurations."""

    def __init__(
        self,
        state_dimension,
        number_of_configurations,
        hidden_dimension=32,
    ):
        super().__init__()

        if state_dimension <= 0:
            raise ValueError("state_dimension must be positive.")

        if number_of_configurations <= 0:
            raise ValueError(
                "number_of_configurations must be positive."
            )

        if hidden_dimension <= 0:
            raise ValueError("hidden_dimension must be positive.")

        self.state_dimension = int(state_dimension)
        self.number_of_configurations = int(number_of_configurations)
        self.hidden_dimension = int(hidden_dimension)

        self.network = nn.Sequential(
            nn.Linear(self.state_dimension, self.hidden_dimension),
            nn.ReLU(),
            nn.Linear(self.hidden_dimension, self.number_of_configurations),
        )

    def probabilities(self, state):
        """Return the policy probability distribution for a physical state."""
        state = torch.as_tensor(state, dtype=torch.float32)

        if state.ndim != 1 or state.shape[0] != self.state_dimension:
            raise ValueError(
                f"state must contain exactly {self.state_dimension} values."
            )

        if not torch.isfinite(state).all():
            raise ValueError("state must contain finite values.")

        logits = self.network(state)

        return torch.softmax(logits, dim=-1)

    def distribution(self, state):
        """Return a categorical distribution over control configurations."""
        probabilities = self.probabilities(state)

        return Categorical(probs=probabilities)

    def sample(self, state):
        """Sample a control-configuration index from the policy."""
        distribution = self.distribution(state)

        return int(distribution.sample().item())

    def log_probability(self, state, configuration_index):
        """Return the log-probability of a selected configuration."""
        if not 0 <= configuration_index < self.number_of_configurations:
            raise ValueError(
                "configuration_index is outside the valid range."
            )

        distribution = self.distribution(state)
        action = torch.tensor(configuration_index, dtype=torch.long)

        return distribution.log_prob(action)

    # DynFairRL framework
    def policy_gradient_update(
        self,
        state,
        configuration_index,
        reward,
        optimizer,
    ):
        """Apply one REINFORCE policy-gradient update."""
        if not np.isfinite(reward):
            raise ValueError("reward must be finite.")

        log_probability = self.log_probability(
            state,
            configuration_index,
        )

        reward_tensor = torch.as_tensor(
            reward,
            dtype=log_probability.dtype,
            device=log_probability.device,
        )

        loss = -log_probability * reward_tensor

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        return float(loss.detach().item())


def physics_informed_reward(
    sensing_signal,
    sequence_duration,
    duration_weight=0.0,
):
    """Compute a physics-informed reward for an NV control configuration."""
    if not np.isfinite(sensing_signal):
        raise ValueError("sensing_signal must be finite.")

    if not np.isfinite(sequence_duration):
        raise ValueError("sequence_duration must be finite.")

    if not np.isfinite(duration_weight):
        raise ValueError("duration_weight must be finite.")

    if sensing_signal < 0.0 or sensing_signal > 1.0:
        raise ValueError("sensing_signal must be between 0.0 and 1.0.")

    if sequence_duration < 0.0:
        raise ValueError("sequence_duration must be non-negative.")

    return float(
        sensing_signal
        - duration_weight * sequence_duration
    )