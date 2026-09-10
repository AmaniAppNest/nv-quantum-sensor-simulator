# NV Quantum Sensor Simulator

**A computational framework for designing and testing NV quantum-sensor configurations under realistic physical environments.**

An integrated computational framework connecting finite-element mechanical modeling, NV-center spin dynamics, Lindblad open-system evolution, pulse-sequence simulation, quantum sensing, and physics-informed adaptive control.

> **Core objective:** A researcher can computationally design and test an NV quantum-sensor configuration before implementing the corresponding hardware experiment.

## Reusable and Integrable Python Framework

The simulator is implemented as a reusable Python-based scientific framework rather than as a standalone application tied to a single simulation environment.

It can be used directly for NV quantum-sensing simulations, imported as a Python library into larger scientific workflows, or connected with external multiphysics environments such as COMSOL through compatible Python interoperability and data-exchange workflows.

The FEM, NV spin-dynamics, sensing, and control components are modular and can be used independently or combined into an integrated computational workflow.

---

## Overview

Nitrogen-vacancy (NV) centers in diamond provide a powerful platform for quantum sensing of magnetic, mechanical, thermal, and other physical environments.

The performance of an NV quantum sensor depends not only on the intrinsic spin properties of the defect, but also on the local physical environment, sensor geometry, strain distribution, magnetic field, decoherence processes, and available control protocols.

The **NV Quantum Sensor Simulator** provides a computational framework for studying these coupled effects before experimental implementation.

The project is organized around a modular computational pipeline connecting:

**Physical environment → mechanical fields → NV spin Hamiltonian → Lindblad dynamics → control protocol → quantum response → sensing performance**

The framework combines a scientific foundation with extensions for spatial sensor modeling, multiphysics field interoperability, physical-environment coupling, quantum measurement, adaptive control, and physics-informed reinforcement learning.

*For the detailed extension architecture, see **[Extension Architecture](extention.text.md)**.*

---

## Computational Workflow

The simulator connects the physical environment of an NV sensor to its quantum response and sensing performance through an integrated computational workflow.

![NV Quantum Sensor Simulator computational workflow](docs/images/schematic_workflow.png)

**Figure 1. End-to-end computational workflow of the NV Quantum Sensor Simulator, including physics-informed control optimization for case-specific sensor conditions.**

The computational sequence is:

1. Define the sensor and environmental configuration.
2. Construct the mechanical model using finite-element methods.
3. Compute displacement and strain fields.
4. Map relevant physical quantities into the NV spin model.
5. Construct the NV-center spin Hamiltonian.
6. Propagate the quantum state using Lindblad master-equation dynamics.
7. Evaluate sensing or dynamical-decoupling configurations.
8. Evaluate the resulting quantum response and sensing performance.
9. Use adaptive control or physics-informed reinforcement learning to select control configurations according to the simulated physical response.

---

## Current Capabilities

The repository currently provides:

* NV-center spin-1 Hamiltonian construction.
* Zero-field splitting and Zeeman interactions.
* Effective transverse strain-dependent Hamiltonian terms.
* Lindblad master-equation evolution.
* Pure-dephasing modeling.
* Quantum coherence evaluation.
* Hahn-echo pulse-sequence representation.
* Finite-element mechanical modeling using `scikit-fem`.
* Mechanical displacement and strain-field calculation.
* Mesh-convergence analysis.
* Coupling of FEM-derived strain information to the NV model.
* Spatial NV sensor representation.
* Spatially sampled multiphysics field-data representation.
* Local physical-environment modeling.
* Quantum measurement and normalized sensing-signal evaluation.
* Objective-based adaptive control selection.
* Stochastic control policies implemented with PyTorch.
* REINFORCE policy-gradient updates.
* Physics-informed reward evaluation based on sensing signal and control duration.
* Integration of the control policy with NV Lindblad simulation and sensing evaluation.
* Automated numerical and physics-consistency tests.
* Visualization of representative mechanical and quantum-simulation results.

---

## Finite-Element Mechanical Modeling

The mechanical component uses finite-element methods to calculate displacement and strain fields in a representative sensor environment.

The FEM module includes:

* Geometry definition.
* Mesh generation.
* Elasticity calculations.
* Displacement-field evaluation.
* Strain-field extraction.
* Mesh-convergence studies.
* Transfer of mechanical information to the NV spin model.

### Finite-Element Mechanical Field

![Finite-element mechanical field](docs/images/fem_fields.png)

**Figure 2. Finite-element simulation of the mechanical displacement and strain fields used as the basis for NV strain modeling.**

The mechanical field provides the physical environment from which local strain-dependent effects are introduced into the quantum model.

---

## NV Spin Hamiltonian

The NV electronic ground state is modeled as a spin-1 quantum system.

The Hamiltonian includes the principal contributions:

* Zero-field splitting.
* Zeeman interaction with an external magnetic field.
* An effective transverse strain contribution.

The model can be expressed as:

**H = H_ZFS + H_Z + H_strain**

The implementation uses **QuTiP** for quantum operators and quantum-state evolution.

The Hamiltonian module is separated from the FEM implementation so that different physical environments and field configurations can be evaluated without restructuring the quantum-dynamics layer.

Additional Hamiltonian implementation details are documented in [Extension Architecture](extention.text.md).

---

## Lindblad Quantum Dynamics

Open-system dynamics are modeled using the Lindblad master equation.

The current implementation supports pure dephasing through a collapse operator and evaluates the evolution of the density matrix using QuTiP.

The general form is:

**dρ/dt = −i[H, ρ] + Σₖ (LₖρLₖ† − ½{Lₖ†Lₖ, ρ})**

where:

* **ρ** is the density matrix.
* **H** is the system Hamiltonian.
* **Lₖ** are Lindblad collapse operators describing environmental interactions.
* **†** denotes the Hermitian conjugate.
* **Σₖ** represents the sum over modeled environmental channels.

The implementation provides the open-system quantum-dynamics foundation for studying environmental decoherence, quantum coherence, and control protocols in NV-based sensing.

Additional Lindblad implementation details are documented in [Extension Architecture](extention.text.md).

---

## Pulse Sequences and Dynamical Decoupling

Quantum sensing performance depends strongly on the applied control sequence.

The current implementation includes a basic **Hahn-echo** protocol and a modular pulse-sequence representation for sensing and dynamical-decoupling studies.

The pulse-sequence layer represents:

* Hahn echo.
* Free-evolution intervals.
* π-pulse events.
* Case-dependent control configurations.

The control representation connects with the quantum-dynamics and measurement layers through the adaptive-control architecture.

Additional control implementation details are documented in [Extension Architecture](extention.text.md).

---

## Example Calculations

### NV Coherence Decay

Run:

```bash
python -m examples.coherence_decay
```

This example demonstrates quantum coherence decay under Lindblad dephasing.

![NV coherence decay](docs/images/coherence_decay.png)

**Figure 3. Simulated NV coherence decay under Lindblad dephasing.**

### Finite-Element Visualization

Run:

```bash
python -m examples.fem_visualization
```

This generates a visualization of the mechanical displacement and strain fields obtained from the finite-element model.

### Mesh Convergence

Run:

```bash
python -m examples.mesh_convergence
```

The example evaluates the mechanical response for multiple mesh resolutions and provides a numerical convergence check.

### FEM-to-NV Coupling

Run:

```bash
python -m examples.fem_to_nv
```

This example demonstrates the transfer of FEM-derived strain information into the NV strain-coupling model.

### Hahn Echo

Run:

```bash
python -m examples.hahn_echo
```

This example combines the NV Hamiltonian, Lindblad dephasing, and a Hahn-echo control sequence to evaluate the resulting quantum coherence.

### Physics-Informed Control

Run:

```bash
python examples/physics_informed_control.py
```

This example connects the control-policy layer directly to the NV quantum-simulation stack.

For each admissible control configuration, the example evaluates:

**Control configuration → Lindblad evolution → sensing signal → physics-informed reward**

The stochastic policy samples a control configuration for the current physical state and applies a REINFORCE policy-gradient update using the simulated reward.

The implemented reward combines sensing performance with a control-duration penalty:

**R = sensing signal − duration weight × sequence duration**

This provides a physics-informed learning loop around the existing NV simulation components.

---

## Researcher Use

The intended use of the simulator is to allow a researcher to modify a physical sensor configuration and evaluate its consequences computationally before implementing the corresponding experiment.

A typical workflow includes:

1. Define a mechanical or environmental configuration.
2. Generate the corresponding FEM mesh and physical fields.
3. Evaluate displacement and strain distributions.
4. Select an NV position and orientation.
5. Map local physical quantities into the NV coordinate system.
6. Construct the corresponding spin Hamiltonian.
7. Simulate open-system quantum dynamics.
8. Apply a sensing or dynamical-decoupling sequence.
9. Evaluate a sensing-related observable.
10. Compare alternative sensor configurations or control protocols.
11. Use the resulting physical response as an objective or reward for adaptive control.

*For the detailed extension architecture, see **[Extension Architecture](extention.text.md)**.*

---

## Physics-Informed Adaptive Control

The simulator contains an adaptive-control layer connecting the physical sensor state with admissible quantum-control configurations.

The control architecture can be represented conceptually as:

**s_NV → πθ(a | s_NV) → control configuration → quantum evolution → sensing response → reward**

where the physical state can contain quantities such as:

* Magnetic field.
* Local strain.
* Temperature.
* NV orientation.
* Spatial configuration.
* Environmental and experimental parameters.

The implemented `StochasticControlPolicy` uses a neural network to represent a probability distribution over admissible control configurations.

The policy provides:

* State-dependent action probabilities.
* Categorical sampling of control configurations.
* Log-probability evaluation.
* REINFORCE policy-gradient updates.

The implemented `physics_informed_reward` function evaluates the selected configuration using the simulated sensing signal and sequence duration.

The resulting learning loop is connected to the physical simulator rather than treating reinforcement learning as an independent numerical optimization problem.

The current example demonstrates this integration using NV Hamiltonian construction, Lindblad evolution, sensing-signal evaluation, and policy-gradient optimization.

---

## Validation and Testing

The repository includes automated tests covering the main computational components.

The test suite checks:

* NV Hamiltonian construction.
* Spin-1 operator consistency.
* Magnetic-field response.
* Lindblad evolution.
* Quantum coherence behavior.
* FEM mesh generation.
* Elasticity calculations.
* Strain-field extraction.
* FEM-to-NV strain coupling.
* Hahn-echo representation and evolution.
* Spatial NV sensor modeling.
* Multiphysics field-data representation.
* Physical-environment coupling.
* Quantum measurement functions.
* Adaptive control configuration handling.
* Stochastic control-policy behavior.
* Policy-gradient parameter updates.
* Physics-informed reward behavior.

Run the complete test suite with:

```bash
pytest
```

The complete automated test suite currently passes **44 tests**.

---

## Software Stack

The project is implemented in Python and uses:

* **NumPy** — numerical array operations.
* **SciPy** — scientific computing utilities.
* **Matplotlib** — scientific visualization.
* **QuTiP** — quantum dynamics and open-system simulation.
* **scikit-fem** — finite-element modeling.
* **PyTorch** — stochastic control policies and policy-gradient optimization.
* **pytest** — automated testing.

---

## Repository Structure

```text
nv-quantum-sensor-simulator/
│
├── README.md
├── extention.text.md
├── pyproject.toml
├── .gitignore
│
├── fem/
│   ├── __init__.py
│   ├── geometry.py
│   ├── mesh.py
│   ├── elasticity.py
│   ├── strain_field.py
│   └── field_data.py
│
├── nv/
│   ├── __init__.py
│   ├── hamiltonian.py
│   ├── lindblad.py
│   ├── strain_coupling.py
│   ├── pulse_sequences.py
│   ├── sensor.py
│   ├── environment.py
│   ├── measurement.py
│   └── control.py
│
├── pirl/
│   └── __init__.py
│
├── examples/
│   ├── coherence_decay.py
│   ├── fem_visualization.py
│   ├── mesh_convergence.py
│   ├── fem_to_nv.py
│   ├── hahn_echo.py
│   └── physics_informed_control.py
│
├── tests/
│   ├── test_hahn_echo.py
│   ├── test_hamiltonian.py
│   ├── test_lindblad.py
│   ├── test_fem.py
│   ├── test_strain_coupling.py
│   ├── test_sensor.py
│   ├── test_field_data.py
│   ├── test_environment.py
│   ├── test_measurement.py
│   └── test_control.py
│
├── docs/
│   └── images/
│       ├── schematic_workflow.png
│       ├── fem_fields.png
│       └── coherence_decay.png
│
└── results/
    └── .gitkeep
```

---

## Related Research and Adaptive Control

The adaptive-control design is also informed by previous methodological work on case-dependent execution under predefined structural constraints.

The methodological connection to the NV sensing framework is the use of a state-dependent stochastic policy to select an appropriate execution configuration for the current case.

In the NV context, the physical state describes the sensor condition, while the adaptive-control layer selects among admissible quantum-control configurations. The selected configuration is evaluated through the physical quantum-simulation pipeline.

The connection is therefore methodological rather than domain-specific:

**Observed state → structured execution options → stochastic policy → execution → evaluated outcome**

For NV quantum sensing, the observed state is physical, the execution options are quantum-control configurations, and the outcome is evaluated through quantum dynamics and sensing performance.

This methodological background supports the adaptive-policy design; the primary scientific focus of this repository remains computational NV quantum sensing and physics-informed control.

---

## Project Status

The repository provides a modular computational framework for coupled mechanical and quantum modeling of NV-based quantum sensing.

The current implementation includes:

* Finite-element mechanical modeling.
* NV spin Hamiltonian construction.
* Lindblad open-system dynamics.
* Strain coupling.
* Spatial sensor representation.
* Physical-environment modeling.
* Quantum measurement.
* Adaptive control.
* Physics-informed reinforcement learning.
* Reproducible computational examples.
* Automated validation.

The architecture separates the physical simulation layers from sensing and control layers while connecting them through explicit computational interfaces.

The emphasis is on:

* Physically interpretable models.
* Reproducible numerical simulations.
* Modular scientific software.
* Explicit validation through automated tests.
* Integration of mechanical and quantum models.
* Physics-informed adaptive control.
* Clear separation between scientific foundation and specialized extensions.

---

## License

This project is licensed under the **Apache License 2.0**.
