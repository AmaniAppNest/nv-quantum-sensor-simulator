"""Physical environment coupling for NV quantum sensors."""

from dataclasses import dataclass

import numpy as np

from nv.hamiltonian import nv_hamiltonian
from nv.sensor import NVSensor


@dataclass(frozen=True)
class NVEnvironment:
    """Represent the local physical environment of an NV sensor."""

    magnetic_field: np.ndarray
    strain: float = 0.0
    temperature: float = 300.0

    def __post_init__(self):
        magnetic_field = np.asarray(self.magnetic_field, dtype=float)

        if magnetic_field.shape != (3,):
            raise ValueError(
                "magnetic_field must contain exactly three components."
            )

        if not np.isfinite(magnetic_field).all():
            raise ValueError("magnetic_field must contain finite values.")

        if not np.isfinite(self.strain):
            raise ValueError("strain must be finite.")

        if not np.isfinite(self.temperature):
            raise ValueError("temperature must be finite.")

        object.__setattr__(self, "magnetic_field", magnetic_field)

    def hamiltonian(self):
        """Return the NV Hamiltonian for the local environment."""
        return nv_hamiltonian(
            magnetic_field=self.magnetic_field,
            strain=self.strain,
        )

    def state_vector(self, sensor: NVSensor):
        """Return the local physical state associated with an NV sensor."""
        return np.concatenate(
            [
                sensor.position,
                sensor.orientation,
                self.magnetic_field,
                [self.strain, self.temperature],
            ]
        )