"""Physics-informed control optimization for an NV quantum sensor."""

import numpy as np
import qutip as qt
import torch

from nv.control import (
    ControlConfiguration,
    StochasticControlPolicy,
    physics_informed_reward,
)
from nv.hamiltonian import nv_hamiltonian
from nv.lindblad import evolve_density_matrix
from nv.measurement import measurement_signal


def evaluate_control_configuration(
    configuration,
    hamiltonian,
    initial_state,
    dephasing_rate,
):
    """Evaluate an NV control configuration using Lindblad dynamics."""
    total_duration = configuration.duration

    times = np.linspace(
        0.0,
        total_duration,
        101,
    )

    result = evolve_density_matrix(
        hamiltonian,
        initial_state,
        times,
        dephasing_rate=dephasing_rate,
    )

    sensing_signal = measurement_signal(result.states[-1])

    reward = physics_informed_reward(
        sensing_signal=sensing_signal,
        sequence_duration=total_duration,
        duration_weight=1.0e5,
    )

    return sensing_signal, reward


def main():
    """Run a physics-informed control optimization example."""
    np.random.seed(7)
    torch.manual_seed(7)

    configurations = [
        ControlConfiguration(
            name="short_sequence",
            sequence=(0.25e-6, 0.25e-6),
        ),
        ControlConfiguration(
            name="medium_sequence",
            sequence=(0.50e-6, 0.50e-6),
        ),
        ControlConfiguration(
            name="long_sequence",
            sequence=(0.75e-6, 0.75e-6),
        ),
    ]

    hamiltonian = nv_hamiltonian(
        magnetic_field=[0.0, 0.0, 1.0e-4],
    )

    initial_state = (
        qt.basis(3, 1) + qt.basis(3, 0)
    ).unit()

    dephasing_rate = 1.0e6

    state_dimension = 11

    policy = StochasticControlPolicy(
        state_dimension=state_dimension,
        number_of_configurations=len(configurations),
    )

    optimizer = torch.optim.Adam(
        policy.parameters(),
        lr=0.01,
    )

    physical_state = np.concatenate(
        [
            np.zeros(3),
            np.array([0.0, 0.0, 1.0]),
            np.array([0.0, 0.0, 1.0e-4]),
            np.array([0.0, 300.0]),
        ]
    )

    print("Physics-informed NV control optimization")
    print()

    for configuration in configurations:
        sensing_signal, reward = evaluate_control_configuration(
            configuration=configuration,
            hamiltonian=hamiltonian,
            initial_state=initial_state,
            dephasing_rate=dephasing_rate,
        )

        print(
            f"{configuration.name}: "
            f"duration={configuration.duration:.3e} s, "
            f"sensing_signal={sensing_signal:.6f}, "
            f"reward={reward:.6f}"
        )

    selected_index = policy.sample(physical_state)

    sensing_signal, reward = evaluate_control_configuration(
        configuration=configurations[selected_index],
        hamiltonian=hamiltonian,
        initial_state=initial_state,
        dephasing_rate=dephasing_rate,
    )

    loss = policy.policy_gradient_update(
        state=physical_state,
        configuration_index=selected_index,
        reward=reward,
        optimizer=optimizer,
    )

    selected_configuration = configurations[selected_index]

    print()
    print(f"Selected configuration: {selected_configuration.name}")
    print(f"Sensing signal: {sensing_signal:.6f}")
    print(f"Physics-informed reward: {reward:.6f}")
    print(f"Policy-gradient loss: {loss:.6f}")


if __name__ == "__main__":
    main()