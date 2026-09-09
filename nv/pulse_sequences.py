"""Pulse sequences for NV-center control."""


def hahn_echo(tau):
    """Return the timing of a Hahn-echo sequence."""
    if tau <= 0.0:
        raise ValueError("tau must be positive.")

    return [
        ("free_evolution", tau),
        ("pi_pulse", 0.0),
        ("free_evolution", tau),
    ]