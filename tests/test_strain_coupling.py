import numpy as np

from nv.strain_coupling import transverse_strain


def test_zero_strain_gives_zero_frequency_shift():
    strain = np.zeros((2, 2))

    result = transverse_strain(
        strain,
        coupling_hz_per_strain=1.0e12,
    )

    assert np.isclose(result, 0.0)


def test_transverse_strain_is_nonnegative():
    strain = np.array(
        [
            [2.0e-6, 1.0e-6],
            [1.0e-6, -2.0e-6],
        ]
    )

    result = transverse_strain(
        strain,
        coupling_hz_per_strain=1.0e12,
    )

    assert result >= 0.0
    assert np.isfinite(result) 