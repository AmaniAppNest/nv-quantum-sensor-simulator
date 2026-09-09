"""Map FEM strain tensors to an effective NV strain parameter."""

import numpy as np


def transverse_strain(strain_tensor, coupling_hz_per_strain=0.0):
    """Return an effective transverse strain in hertz."""
    strain_tensor = np.asarray(strain_tensor, dtype=float)

    if strain_tensor.shape[-2:] != (2, 2):
        raise ValueError("strain_tensor must have a final 2x2 tensor dimension.")

    epsilon_xx = strain_tensor[..., 0, 0]
    epsilon_yy = strain_tensor[..., 1, 1]
    epsilon_xy = strain_tensor[..., 0, 1]

    transverse_component = np.sqrt(
        (epsilon_xx - epsilon_yy) ** 2
        + (2.0 * epsilon_xy) ** 2
    )

    return coupling_hz_per_strain * transverse_component 