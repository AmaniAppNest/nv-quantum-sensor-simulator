# NV Quantum Sensor Simulator

A computational framework for designing and testing NV quantum-sensor configurations under realistic physical environments.

The framework combines finite-element mechanical modeling, NV spin Hamiltonians, Lindblad open-system dynamics, strain-dependent quantum modeling, dynamical-decoupling protocols, and physics-informed control optimization.

> **Central objective:** Enable a researcher to computationally design and test an NV quantum-sensor configuration before implementing the corresponding hardware experiment.

## Computational Workflow:![NV Quantum Sensor Simulator computational workflow]

The simulator connects the physical environment of an NV sensor to its quantum response and sensing performance through an integrated computational workflow.

 <img width="1672" height="941" alt="image" src="https://github.com/user-attachments/assets/9a7d1e33-1880-4b9c-bb6b-bb0d6f744fb2" />


**Figure 1. End-to-end computational workflow of the NV Quantum Sensor Simulator, including physics-informed control optimization for case-specific sensor conditions.**

The main computational stages are:

1. Physical environment
2. Finite-element mechanical modeling
3. NV quantum model
4. Lindblad open-system dynamics
5. Quantum control and dynamical decoupling
6. Physics-informed control optimization
7. NV sensor response and performance evaluation

The workflow is designed so that changes in the physical environment can propagate through the mechanical and quantum models and affect the resulting control and sensing response.

---

## Scientific Motivation

Nitrogen-vacancy centers in diamond provide quantum sensors whose response depends on magnetic fields, mechanical strain, temperature, decoherence, and the applied control protocol.

For realistic sensor configurations, these effects cannot always be treated independently.

Mechanical deformation can generate spatially varying strain fields. The local strain experienced by an NV center depends on its position and orientation. Magnetic fields modify the spin Hamiltonian, while environmental interactions influence the evolution and coherence of the quantum state.

Control sequences then determine how the quantum system responds to the physical environment.

This simulator connects these physical layers within a common computational framework, providing a computational pathway from environmental conditions to quantum response and sensor performance.

---

## Core Computational Framework

The framework integrates four principal computational layers:

| Layer                | Computational role                                                                  |
| -------------------- | ----------------------------------------------------------------------------------- |
| Mechanical modeling  | Geometry, finite-element mesh, elasticity, displacement, and strain                 |
| Quantum modeling     | NV spin Hamiltonian, magnetic-field interaction, and strain-dependent contributions |
| Open-system dynamics | Lindblad evolution, decoherence, and quantum coherence                              |
| Control optimization | Dynamical decoupling and physics-informed control selection                         |

The layers are connected so that physical conditions can influence quantum dynamics and control performance.

---

## NV Spin Hamiltonian

The NV electronic ground state is represented as a spin-1 quantum system.

The Hamiltonian model includes:

* Zero-field splitting
* Magnetic-field interaction
* Transverse strain contribution
* Configurable electron gyromagnetic ratio
* Three-component magnetic-field input

The implementation uses QuTiP spin operators and represents the Hamiltonian in frequency units.

> [!IMPORTANT]
> The quantum model is connected to physical environmental parameters rather than treating the NV center as an isolated abstract spin system.

A compact representation of the modeled structure is:

> **NV Hamiltonian = zero-field splitting + magnetic interaction + strain interaction**

This provides the basis for evaluating changes in the NV energy structure under different magnetic and mechanical conditions.

---

## NV Orientation

The response of an NV center depends on the orientation of the NV quantization axis relative to the applied magnetic field and local mechanical environment.

The simulator therefore treats the magnetic field as a three-component vector rather than as a scalar magnitude.

This provides the basis for orientation-aware quantum-sensing configurations in which local physical quantities can be related to the coordinate system of an individual NV center.

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
### Finite-element mechanical field

![Finite-element mechanical field](docs/images/fem_fields.png)

Figure: Finite-element simulation of the mechanical field used as the basis for NV strain modeling.

---

## Mechanical-to-Quantum Coupling

The simulator connects the finite-element strain field to the NV quantum model through strain-dependent frequency contributions.

The strain-processing layer evaluates the transverse component of the local strain tensor and maps it to an effective frequency contribution.

The computational relationship is:

> **Mechanical deformation → strain field → NV quantum Hamiltonian**

This coupling allows mechanical deformation to influence the quantum energy structure rather than treating strain as an unrelated external parameter.

The architecture also provides a basis for incorporating spatially resolved NV locations and orientation-dependent mechanical effects.

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

The computational flow is:

> **Initial quantum state → Lindblad evolution → time-dependent density matrix → coherence**

This provides a numerical basis for studying how environmental decoherence modifies the quantum sensor response.

---

## Dynamical Decoupling

Quantum control is represented through pulse-sequence modeling.

The current control layer includes a Hahn-echo sequence consisting of:

1. Free evolution
2. Pi pulse
3. Second free-evolution period

The sequence can be combined with Lindblad dynamics to evaluate the resulting quantum coherence.

Dynamical decoupling provides a control mechanism for investigating how pulse timing and quantum evolution affect the sensor response.

The same control layer provides a foundation for evaluating alternative pulse protocols under different physical conditions.

---

## Physics-Informed Control Optimization

The simulator is designed so that physical simulation results can provide the state information required for adaptive control and optimization.

Relevant state information may include:

* Magnetic-field strength
* Magnetic-field orientation
* Mechanical strain
* Temperature
* Decoherence
* NV orientation
* Available control operations
* Experimental constraints

These quantities can be obtained from the physical simulation and, where appropriate, from sensor or experimental data.

An optimization or reinforcement-learning layer can then use the observed physical state to evaluate or select an appropriate control configuration.

The computational structure is:

> **Physical state → quantum response → control evaluation → sensing performance**

This allows control decisions to be evaluated against the actual physical conditions of the sensor rather than against an isolated abstract model.

The approach is particularly relevant to physics-informed machine learning, where physical constraints and simulated quantum responses can be incorporated into the learning or optimization process.

---

## Physics-Based Control Objectives

Control optimization can be formulated around measurable physical objectives rather than an abstract optimization target.

Relevant objectives include:

* Quantum signal performance
* Coherence preservation
* Sensing sensitivity
* Robustness to environmental variation
* Control cost
* Physical validity of the selected operation

A conceptual multi-objective formulation is:

> [!NOTE]
> **Reward = sensing performance + coherence + robustness − control cost**

The exact objective can be adapted to the sensing task and experimental constraints.

This formulation provides a pathway for integrating physics-based optimization or reinforcement-learning methods with the simulated quantum sensor.

---

## Sensor Response and Performance

The final stage evaluates the response of the NV sensor under the selected physical and control configuration.

Relevant observables and performance measures include:

* Quantum coherence
* Energy-level structure
* Signal response
* Control response
* Robustness
* Sensing sensitivity

These quantities provide the basis for comparing alternative sensor configurations and control strategies.

The objective is not simply to simulate quantum dynamics, but to use the resulting dynamics to inform practical sensor-design decisions.

---

## Sensor Data and Adaptive Learning

The framework can operate with physical states obtained from simulation as well as with suitable sensor or experimental measurements.

A sensor state may contain information describing the current physical environment, such as:

* Magnetic-field conditions
* Local mechanical strain
* Temperature
* Decoherence characteristics
* NV orientation
* Experimental control constraints

This information can be passed to an optimization or machine-learning layer to evaluate control configurations for the observed condition.

The resulting architecture provides a pathway from **physical sensing data to quantum modeling and adaptive control**.

This separation between the physical model and the learning layer also allows different optimization approaches to be investigated without changing the underlying NV quantum and mechanical models.

---

## Researcher Use

The framework supports computational investigation of questions such as:

* How does mechanical deformation affect an NV sensor?
* How does local strain modify the NV quantum Hamiltonian?
* How does magnetic-field orientation influence the energy structure?
* How does decoherence affect quantum coherence?
* How do dynamical-decoupling protocols modify the sensor response?
* Which control configuration is most suitable for a particular physical environment?
* How robust is a sensing protocol to environmental variation?
* How can physical simulation inform adaptive quantum-control decisions?
* How can simulated or measured sensor states be used for physics-informed control optimization?

The resulting simulations can be used to evaluate sensor configurations and control strategies before corresponding experimental implementation.

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
``
Demonstrates quantum coherence decay under Lindblad dephasing.

<img width="1280" height="960" alt="image" src="https://github.com/user-attachments/assets/48abbdb4-0b5f-475d-a158-26187cecdc9e" />

Figure: Simulated NV coherence decay under Lindblad dephasing.



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

The computational process begins with the environmental and mechanical configuration, constructs the corresponding quantum model, propagates the open-system dynamics, applies the selected control protocol, and evaluates the resulting sensor response.

When sensor or experimental data are available, the same framework can use the observed physical state as an input to control evaluation and adaptive optimization.

This provides a computational pathway from physical modeling and sensing data to quantum-sensor design.

---

## Relevance to NV Quantum Sensing

The project addresses several computational aspects relevant to NV-center quantum sensing:

* Spin-Hamiltonian modeling
* Magnetic-field interactions
* Mechanical strain effects 
* Open quantum-system dynamics
* Decoherence
* Dynamical decoupling
* Finite-element mechanical simulation
* Physics-informed control optimization
* Adaptive control under physical constraints
* Sensor-data-driven computational modeling
* Computational evaluation of sensing performance

The integration of these components provides a computational framework for studying NV sensors under coupled mechanical, magnetic, environmental, and control conditions.

---

## Related Research and Adaptive Control

The broader adaptive-control direction is also conceptually informed by previous research on case-dependent execution under predefined structural constraints.

**DynFair: An Ontology-Grounded Reinforcement Learning Framework for Intrinsically Fair Protocol-Compliant Multi-Faceted Decision Execution — Case-Specific Stochastic Policies for Protocol-Compliant Execution**

DynFair studies how a predefined decision can be executed correctly under different observed structural conditions.

In simple terms, the research considers how the execution of a predefined decision can adapt to the requirements of the current case while respecting the valid structural constraints of the system.

This concept can be integrated into the NV sensing context, where the observed physical state defines the current sensor condition and an adaptive control method can determine an appropriate control configuration within the physical and experimental constraints.

The connection is therefore methodological: **the physical model and sensor data describe the current case, while an adaptive learning or optimization layer can determine an appropriate execution strategy for that case.**

This provides a potential bridge between quantum-sensor simulation, sensor data, physics-informed machine learning, and adaptive quantum control.

The source code associated with the DynFair research will be made publicly available upon publication of the corresponding research work. A formal publication reference and link will be added here upon publication.

---

## License

This project is released under the license specified in the repository.
