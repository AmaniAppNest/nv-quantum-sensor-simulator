"""Adaptive control interfaces for NV quantum sensing."""

from dataclasses import dataclass

import numpy as np


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