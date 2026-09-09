# NV Quantum Sensor Simulator

A computational framework for designing and testing NV quantum-sensor configurations under realistic physical environments.

The framework combines finite-element mechanical modeling, NV spin Hamiltonians, Lindblad open-system dynamics, strain-dependent quantum modeling, dynamical-decoupling protocols, and physics-informed control optimization.

> **Central objective:** Enable a researcher to computationally design and test an NV quantum-sensor configuration before implementing the corresponding hardware experiment.

## ![NV Quantum Sensor Simulator computational workflow]

The simulator connects the physical environment of an NV sensor to its quantum response and sensing performance through a physics-based computational workflow.
<img width="1672" height="941" alt="image" src="https://github.com/user-attachments/assets/8d435713-e08a-47a8-8802-39f69ff38dd1" />

**Figure 1. End-to-end computational workflow of the NV Quantum Sensor Simulator, including physics-informed reinforcement learning for case-specific control optimization.**

The main computational stages are:

1. Physical environment
2. Finite-element mechanical modeling
3. NV quantum model
4. Lindblad open-system dynamics
5. Quantum control and dynamical decoupling
6. Physics-informed reinforcement-learning control
7. NV sensor response and performance evaluation

The workflow is designed so that changes in the physical environment propagate through the mechanical and quantum models and ultimately affect control and sensing performance.

---

## Scientific Motivation

Nitrogen-vacancy centers in diamond provide quantum sensors whose response depends on magnetic fields, mechanical strain, temperature, decoherence, and the applied control protocol.

For realistic sensor configurations, these effects cannot always be treated independently.

Mechanical deformation can generate spatially varying strain fields. The local strain experienced by an NV center depends on its position and orientation. Magnetic fields modify the spin Hamiltonian, while environmental interactions determine the evolution and coherence of the quantum state.

Control sequences then determine how the quantum system responds to the physical environment.

This simulator connects these physical layers within a common computational framework.

---

## Core Computational Framework

The framework integrates four principal computational layers:

| Layer                | Computational role                                            |
| -------------------- | ------------------------------------------------------------- |
| Mechanical modeling  | Finite-element geometry, elasticity, displacement, and strain |
| Quantum modeling     | NV spin Hamiltonian and environmental interactions            |
| Open-system dynamics | Lindblad evolution, decoherence, and quantum coherence        |
| Control optimization | Dynamical decoupling and physics-informed control selection   |

The layers are connected so that physical conditions can influence quantum dynamics and control performance.

---

## NV Spin Hamiltonian

The NV electronic ground state is represented as a spin-1 quantum system.

The Hamiltonian includes:

* Zero-field splitting
* Magnetic-field interaction
* Transverse strain contribution
* Configurable electron gyromagnetic ratio
* Three-component magnetic-field input
* NV-axis-dependent modeling architecture

The implementation uses QuTiP spin operators and represents the Hamiltonian in frequency units.

> [!IMPORTANT]
> The quantum model is not treated as an isolated abstract spin system. Environmental and mechanical parameters are introduced as physical inputs to the Hamiltonian.

A compact representation of the modeled structure is:

> **NV Hamiltonian = zero-field splitting + magnetic interaction + strain interaction**

This provides the basis for evaluating changes in the NV energy structure under different physical conditions.

---

## NV Orientation

NV centers occupy specific crystallographic orientations within diamond.

Consequently, the response of an NV sensor depends not only on the magnitude of an environmental field but also on its orientation relative to the NV quantization axis.

Explicit NV-axis handling is part of the quantum-sensing architecture.

This provides the basis for transforming environmental quantities into the coordinate system relevant to an individual NV center and for extending the simulator toward spatially resolved sensor configurations.

---

## Finite-Element Mechanical Modeling

Mechanical effects are represented using a finite-element model of a diamond cantilever.

The mechanical model includes:

* Parametric cantilever geometry
* Structured triangular mesh generation
* Linear elasticity
* Material parameters
* Fixed boundary conditions
* Applied mechanical traction
* Displacement-field calculation
* Strain-field extraction

The implementation uses `scikit-fem` for finite-element assembly and numerical solution.

The resulting displacement and strain fields provide physical inputs for the NV quantum model.

---

## Mechanical-to-Quantum Coupling

The simulator connects the finite-element strain field to the NV quantum model through strain-dependent frequency contributions.

The strain-processing layer evaluates the transverse component of the local strain tensor and maps it to an effective frequency contribution.

The computational relationship is:

> **Mechanical deformation → strain field → NV quantum Hamiltonian**

This coupling allows mechanical deformation to influence the quantum energy structure rather than treating strain as an unrelated external parameter.

The architecture is designed to support physically resolved NV locations and orientations as the sensor model develops.

---

## Open-System Quantum Dynamics

Real quantum sensors interact with their environment and therefore require an open-system description.

The simulator uses Lindblad master-equation dynamics to model the evolution of the NV density matrix.

The current implementation provides:

* Density-matrix evolution
* Pure dephasing
* Configurable decoherence rate
* Quantum coherence evaluation
* Time-dependent state evolution
* Trace-preserving numerical evolution

The Hamiltonian is converted from frequency units to angular-frequency units for numerical propagation with QuTiP.

> [!NOTE]
> The Lindblad layer provides the connection between the ideal NV Hamiltonian and environmentally affected quantum dynamics.

The main computational object is the density matrix:

> **Quantum state → Lindblad evolution → time-dependent density matrix → coherence**

---

## Dynamical Decoupling

Quantum control is implemented through pulse-sequence modeling.

The current control layer includes a Hahn-echo sequence consisting of:

1. Free evolution
2. pi pulse
3. Second free-evolution period

The sequence can be combined with Lindblad dynamics to evaluate the resulting quantum coherence.

Dynamical decoupling provides the control mechanism required to investigate how pulse timing and quantum evolution affect sensing performance.

---

## Physics-Informed Reinforcement Learning

The control-optimization layer is informed by previous research on case-specific stochastic policies for protocol-compliant execution.

The relevant research work is:

> **DynFair: An Ontology-Grounded Reinforcement Learning Framework for Intrinsically Fair Protocol-Compliant Multi-Faceted Decision Execution — Case-Specific Stochastic Policies for Protocol-Compliant Execution**

This is a separate research project and is **not presented as part of the NV quantum-sensor simulator**.

Its relevance to this framework is the computational concept of adapting an execution policy to the observed case while respecting the admissible execution space.

### Case-Specific Stochastic Policy

For an NV sensor, the observed physical state may include:

* Magnetic-field magnitude and orientation
* Mechanical strain
* Temperature
* Decoherence
* NV orientation
* Available control operations
* Experimental constraints

The policy then selects among physically admissible control configurations.

A compact representation is:

> **Physical state → stochastic control policy → admissible control action**

The policy is therefore case-specific rather than assuming that one control strategy is optimal for every physical environment.

> [!IMPORTANT]
> The term "fairness" in the original DynFair research refers to protocol-compliant execution and is not used here as a social or population-level fairness concept.

The source code associated with the above research framework will be made publicly available upon publication of the corresponding research work.

A formal publication reference and link will be added to this section upon publication.

---

## Physics-Based Control Reward

The reinforcement-learning control layer is designed around physically meaningful objectives.

A multi-objective reward can incorporate:

* Quantum signal performance
* Coherence preservation
* Sensing sensitivity
* Robustness to environmental variation
* Control cost
* Physical validity of the selected operation

Conceptually:

> [!NOTE]
> **Reward = sensing performance + coherence + robustness − control cost**

The exact reward formulation can be adapted to the sensing objective and experimental constraints.

This provides a direct connection between reinforcement learning and measurable properties of the simulated quantum sensor.

---

## Case-Specific Control

A central principle of the control architecture is that the optimal control configuration can depend on the physical state of the sensor.

Changes in:

* Magnetic-field strength
* Magnetic-field orientation
* Mechanical strain
* Temperature
* Decoherence
* NV orientation
* Available control operations
* Experimental constraints

can modify the quantum response and therefore the preferred control strategy.

The computational structure is:

> **Physical state → admissible control configuration → quantum evolution → sensing performance**

This allows control strategies to be evaluated according to the actual physical conditions represented by the simulator.

---

## Sensor Response and Performance

The final stage of the computational workflow evaluates the response of the NV sensor following the selected physical and control configuration.

Relevant quantities include:

* Quantum coherence
* Energy-level structure
* Signal response
* Control performance
* Robustness
* Sensing sensitivity

The performance evaluation provides the basis for comparing alternative sensor configurations and control strategies.

---

## Researcher Use

The framework supports computational investigation of questions such as:

* How does mechanical deformation affect an NV sensor?
* How does local strain modify the NV quantum Hamiltonian?
* How does magnetic-field orientation influence the energy structure?
* How does decoherence affect quantum coherence?
* How do dynamical-decoupling protocols modify the sensor response?
* Which control configuration performs best under a particular physical environment?
* How robust is a sensing protocol to environmental variation?
* How can physical simulation inform adaptive quantum-control decisions?

The resulting simulations can be used to evaluate sensor configurations before corresponding experimental implementation.

---

## Scientific Software Stack

The project is implemented in Python using established scientific-computing libraries.

| Library    | Role                                        |
| ---------- | ------------------------------------------- |
| NumPy      | Numerical arrays and scientific computation |
| SciPy      | Numerical methods                           |
| QuTiP      | Quantum dynamics and open quantum systems   |
| scikit-fem | Finite-element modeling                     |
| Matplotlib | Scientific visualization                    |
| pytest     | Automated validation                        |

---

## Validation

The repository includes automated tests covering the principal computational components.

Current validation includes:

* NV zero-field energy degeneracy
* Magnetic-field-induced level splitting
* Lindblad density-matrix trace preservation
* Decoherence-induced coherence reduction
* Finite-element mesh construction
* Non-zero mechanical displacement
* Finite strain-field values
* Strain-coupling behavior
* Hahn-echo sequence validation

Run the complete test suite with:

```bash
python -m pytest -q
```

Current repository validation:

```text
10 passed
```

---

## Example Calculations

### NV Coherence Decay

```bash
python -m examples.coherence_decay
```

Demonstrates quantum coherence decay under Lindblad dephasing.

### Finite-Element Visualization

```bash
python -m examples.fem_visualization
```

Generates visualization of the mechanical displacement and strain fields.

### Mesh Convergence

```bash
python -m examples.mesh_convergence
```

Evaluates calculated displacement under increasing finite-element mesh resolution.

### FEM-to-NV Coupling

```bash
python -m examples.fem_to_nv
```

Connects the finite-element strain field to the NV Hamiltonian and evaluates the resulting energy structure.

### Hahn-Echo Simulation

```bash
python -m examples.hahn_echo
```

Simulates a Hahn-echo sequence under NV Hamiltonian dynamics and Lindblad dephasing.

---

## Repository Structure

```text
nv-quantum-sensor-simulator/
├── README.md
├── pyproject.toml
├── .gitignore
│
├── fem/
│   ├── __init__.py
│   ├── geometry.py
│   ├── mesh.py
│   ├── elasticity.py
│   └── strain_field.py
│
├── nv/
│   ├── __init__.py
│   ├── hamiltonian.py
│   ├── lindblad.py
│   ├── strain_coupling.py
│   └── pulse_sequences.py
│
├── pirl/
│   └── __init__.py
│
├── examples/
│   ├── coherence_decay.py
│   ├── fem_visualization.py
│   ├── mesh_convergence.py
│   ├── fem_to_nv.py
│   └── hahn_echo.py
│
├── tests/
│   ├── test_hahn_echo.py
│   ├── test_hamiltonian.py
│   ├── test_lindblad.py
│   ├── test_fem.py
│   └── test_strain_coupling.py
│
├── docs/
│   └── images/
│       └── nv-sensor-workflow.png
│
└── results/
    └── .gitkeep
```

---

## Computational Architecture

The software architecture separates the principal physical and computational components.

### Mechanical Layer

Responsible for:

* Geometry
* Mesh generation
* Elasticity solution
* Displacement fields
* Strain fields

### Quantum Layer

Responsible for:

* Spin-1 operators
* NV Hamiltonian
* Magnetic-field interaction
* Strain-dependent contributions
* Lindblad evolution
* Quantum coherence

### Control Layer

Responsible for:

* Pulse sequences
* Dynamical decoupling
* Control constraints
* Physics-informed control optimization

### Evaluation Layer

Responsible for:

* Quantum coherence
* Signal response
* Sensing performance
* Robustness
* Control quality

The modular structure allows individual physical models to be validated independently while remaining connected through the overall sensing workflow.

---

## From Simulation to Sensor Design

The framework is structured around a practical computational question:

> [!IMPORTANT]
> **What sensor configuration and control strategy should be used for a given physical environment?**

The computational process begins with the environment and mechanical configuration, constructs the corresponding quantum model, propagates the open-system dynamics, applies the selected control protocol, and evaluates the resulting sensor response.

This provides a computational pathway from physical modeling to quantum-sensor design.

---

## Relevance to NV Quantum Sensing

The project directly addresses computational aspects of NV-center quantum sensing, including:

* Spin-Hamiltonian modeling
* Magnetic-field interactions
* Mechanical strain effects
* Open quantum-system dynamics
* Decoherence
* Dynamical decoupling
* Finite-element mechanical simulation
* Physics-informed control optimization
* Case-specific control policies
* Computational evaluation of sensing performance

The integration of these components provides a computational framework for studying NV sensors under coupled mechanical, magnetic, environmental, and control conditions.

---

## Related Research

The physics-informed reinforcement-learning architecture is conceptually informed by previous research on case-specific stochastic policies for protocol-compliant execution.

> **DynFair: An Ontology-Grounded Reinforcement Learning Framework for Intrinsically Fair Protocol-Compliant Multi-Faceted Decision Execution — Case-Specific Stochastic Policies for Protocol-Compliant Execution**

The DynFair research is a separate research project.

Its contribution to the present framework is conceptual: an observed case can determine a probability distribution over admissible execution strategies while maintaining protocol constraints.

For the NV application, this principle is translated into a physics-based control setting in which the observed physical state determines the admissible control space and the policy selects a suitable control configuration according to the simulated sensing response.

A formal publication reference and link will be added after publication of the associated research work.

---

## License

This project is released under the license specified in the repository.
