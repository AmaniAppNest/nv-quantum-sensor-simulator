# NV Quantum Sensor Simulator — Extension Architecture

The **NV Quantum Sensor Simulator** is structured as a modular computational framework for designing, simulating, testing, and evaluating NV quantum-sensor configurations under defined physical conditions.

The architecture separates the **Core Computational Layer** from specialized extension layers. This separation is an engineering design choice: it keeps the central physical and numerical models reusable while providing clear interfaces through which additional sensor, multiphysics, sensing, control, and learning capabilities can be integrated.

The extensions are not separate projects. They are computational layers built around the same NV simulation workflow.

## Why the Framework Is Split into Core and Extensions

The simulator contains several scientific domains that interact but do not need to be implemented as one tightly coupled software component.

For example:

* the NV Hamiltonian should not depend on a particular FEM solver;
* a mechanical-field representation should not depend on a particular quantum-dynamics implementation;
* a sensing model should consume simulated quantum states without redefining the quantum model;
* a control policy should operate on physical states and evaluated sensing responses rather than directly modifying the underlying physics implementation.

The architecture therefore provides a common computational core with explicit extension points.

```text
Core Computational Layer
        |
        +── Spatial Sensor Modeling
        |
        +── Multiphysics Field Interfaces
        |
        +── Physical Environment Coupling
        |
        +── Quantum Sensing
        |
        +── Adaptive Control
        |
        +── Physics-Informed Learning
        |
        v
Integrated NV Sensor Workflow
```

This organization allows a researcher or engineering team to introduce a specialized computational component, test it independently, and integrate it into the existing workflow without redesigning the complete simulator.

The same interface can therefore support different physical models, sensor configurations, field sources, sensing observables, control strategies, and optimization methods.

## Core Computational Layer

The core layer contains the computational models required by the simulator itself.

It provides:

* NV spin Hamiltonian construction
* spin-1 quantum operators
* magnetic-field interactions
* effective strain coupling
* Lindblad open-system evolution
* decoherence modeling
* pulse-sequence representation
* finite-element mechanical modeling
* displacement and strain-field calculation
* numerical field representation
* scientific visualization
* automated validation

The core layer provides the physical and numerical interfaces used by the extension layers.

The separation is intentional: extensions consume and produce defined computational states rather than duplicating the underlying scientific models.

## Extension 1 — Spatial NV Sensor Modeling

The spatial-sensor extension introduces an explicit physical representation of the NV sensing location.

Implementation:

```text
nv/sensor.py
```

The `NVSensor` model represents:

* Cartesian sensor position
* three-dimensional NV orientation
* normalized orientation
* validated spatial coordinates
* distance from the sensor to a Cartesian point

The spatial representation provides the reference required for connecting an NV sensor with spatially varying physical fields.

The interface can be summarized as:

```text
Sensor Configuration
        |
        v
NV Position + Orientation
        |
        v
Local Physical Conditions
        |
        v
Quantum Sensor Model
```

Validation:

```text
tests/test_sensor.py
```

The tests cover:

* orientation normalization
* position preservation
* distance calculation
* invalid-position handling
* zero-orientation rejection

This extension establishes the spatial layer required for moving from an abstract NV quantum system toward physically positioned sensor configurations.

## Extension 2 — Multiphysics Interoperability

The multiphysics extension provides a solver-independent representation of spatially sampled physical-field data.

Implementation:

```text
fem/field_data.py
```

The `FieldData` model provides:

* spatial sample coordinates
* physical-field values
* field names
* field units
* dimensional validation
* nearest-position lookup
* field retrieval at an NV sensor location

The interface is:

```text
Physical / Multiphysics Solver
        |
        v
Spatial Field Data
        |
        v
FieldData
        |
        v
NV Sensor Position
        |
        v
Local Physical Field
```

Validation:

```text
tests/test_field_data.py
```

The tests cover:

* field-data construction
* field metadata
* nearest-position lookup
* invalid spatial input
* mismatched field data
* empty-data rejection
* retrieval of field values at an NV sensor position

The interface is deliberately independent of a specific FEM solver.

The built-in Python FEM implementation provides one source of field data. External multiphysics environments can provide equivalent spatial field data through compatible data-exchange and Python interoperability workflows.

This design allows the quantum-sensing model to remain independent of the physical-field solver used to generate the environment.

## Extension 3 — Physical Environment Coupling

The physical-environment extension connects local environmental conditions with the NV quantum model.

Implementation:

```text
nv/environment.py
```

The `NVEnvironment` model represents local conditions including:

* magnetic-field components
* effective strain
* temperature
* validated physical parameters
* NV Hamiltonian construction
* combined sensor-environment state representation

The computational connection is:

```text
Spatial NV Sensor
        |
        v
Local Physical Environment
        |
        +── Magnetic Field
        |
        +── Strain
        |
        +── Temperature
        |
        v
NV Hamiltonian
        |
        v
Quantum Dynamics
```

Validation:

```text
tests/test_environment.py
```

The tests cover:

* physical-environment construction
* magnetic-field validation
* temperature validation
* Hamiltonian construction
* sensor-environment state representation

This extension separates the description of the local physical state from the quantum-dynamics implementation.

That separation makes it possible to evaluate different physical conditions using the same NV quantum model.

## Extension 4 — Quantum Sensing and Measurement

The quantum-sensing extension converts simulated quantum states into sensing observables.

Implementation:

```text
nv/measurement.py
```

The measurement layer provides:

```python
population_probability(state, basis_state)
coherence_signal(state)
measurement_signal(state)
```

These interfaces provide computational access to:

* population probabilities
* ground-state coherence
* normalized sensing signals

The measurement layer is intentionally separated from quantum-state evolution.

```text
NV Quantum State
        |
        v
Measurement Model
        |
        v
Sensing Observable
        |
        v
Performance Evaluation
```

Validation:

```text
tests/test_measurement.py
```

The tests cover:

* selected-basis population probability
* orthogonal-state probability
* coherence evaluation
* normalized measurement signal
* zero signal for a basis state

This provides a defined interface between quantum simulation and sensor-performance evaluation.

It also allows sensing models to evolve independently from the underlying quantum-dynamics implementation.

## Extension 5 — Adaptive Quantum Control

The adaptive-control extension provides mechanisms for evaluating and selecting admissible control configurations according to a defined objective.

Implementation:

```text
nv/control.py
```

The `ControlConfiguration` model represents:

* a control-configuration name
* a sequence of non-negative control intervals
* total sequence duration

The direct selection interface is:

```python
select_control_configuration(
    configurations,
    objective_values,
)
```

The computational workflow is:

```text
Physical State
        |
        v
Admissible Control Configurations
        |
        v
Quantum Simulation
        |
        v
Sensing Response
        |
        v
Objective Evaluation
        |
        v
Control Selection
```

Validation:

```text
tests/test_control.py
```

The tests cover:

* valid control configuration construction
* sequence-duration calculation
* configuration validation
* sequence-value validation
* objective-based selection
* empty-configuration rejection

The control layer separates the definition and selection of control configurations from the underlying quantum-dynamics implementation.

This provides a controlled interface for comparing different sensing protocols and control configurations against simulated physical performance.

## Extension 6 — Physics-Informed Reinforcement Learning

The physics-informed learning extension connects adaptive policy optimization to the physical state and sensing response generated by the simulator.

Implementation:

```text
nv/control.py
```

The current control-learning interface contains:

* `StochasticControlPolicy`
* state-dependent action probabilities
* categorical control-configuration sampling
* action log-probability evaluation
* REINFORCE policy-gradient updates
* physics-informed reward calculation

The policy operates on the physical sensor state represented by the framework.

```text
Physical Sensor State
        |
        v
Stochastic Control Policy
        |
        v
Admissible Control Configuration
        |
        v
Configured Quantum Evolution
        |
        v
Sensing Response
        |
        v
Physics-Informed Reward
        |
        v
Policy Update
```

The policy network produces a probability distribution over admissible control configurations.

The implemented reward function is:

```python
physics_informed_reward(
    sensing_signal,
    sequence_duration,
    duration_weight,
)
```

with the structure:

```text
Reward =
Sensing Signal
-
Duration Weight × Sequence Duration
```

The policy-gradient interface is:

```python
policy_gradient_update(
    state,
    configuration_index,
    reward,
    optimizer,
)
```

This connects machine-learning optimization directly to the physical simulation workflow.

The learning layer therefore operates around the simulator rather than replacing the underlying physical model.

## Integrated Computational Path

The complete extension architecture connects the major computational layers:

```text
Physical / Multiphysics Configuration
                |
                v
        Spatial NV Sensor
                |
                v
       Local Physical State
                |
                v
        NV Spin Hamiltonian
                |
                v
      Lindblad Quantum Dynamics
                |
                v
       Control Configuration
                |
                v
       Quantum-Sensing Response
                |
                v
      Performance Evaluation
                |
                v
     Adaptive Control / Learning
```

Each layer has a defined computational responsibility.

This separation supports:

* independent component validation
* replacement of individual models
* comparison of alternative configurations
* integration of external physical-field data
* evaluation of sensing performance
* adaptive control optimization

## Example 1 — NV Coherence Decay

Run:

```bash
python -m examples.coherence_decay
```

The example evaluates NV coherence decay under the configured Lindblad dephasing model.

## Example 2 — Finite-Element Visualization

Run:

```bash
python -m examples.fem_visualization
```

The example evaluates and visualizes the mechanical displacement and strain fields generated by the FEM model.

## Example 3 — Mesh Convergence

Run:

```bash
python -m examples.mesh_convergence
```

The example evaluates the FEM response across mesh resolutions and provides a numerical convergence check.

## Example 4 — FEM-to-NV Coupling

Run:

```bash
python -m examples.fem_to_nv
```

The example transfers FEM-derived field information to the NV sensor environment and evaluates the corresponding local physical condition.

## Example 5 — Hahn Echo

Run:

```bash
python -m examples.hahn_echo
```

The example combines the NV Hamiltonian, Lindblad dynamics, and Hahn-echo sequence representation to evaluate the resulting quantum coherence.

## Example 6 — Physics-Informed Control

Run:

```bash
python examples/physics_informed_control.py
```

The example evaluates admissible control configurations through their configured sequence durations, Lindblad quantum evolution, sensing response, and physics-informed reward.

The learning workflow is:

```text
Control Configuration
        |
        v
Lindblad Evolution
        |
        v
Sensing Signal
        |
        v
Physics-Informed Reward
        |
        v
Policy-Gradient Update
```

A representative execution is:

```text
Physics-informed NV control optimization

short_sequence: duration=5.000e-07 s, sensing_signal=0.759607, reward=0.709607
medium_sequence: duration=1.000e-06 s, sensing_signal=0.576997, reward=0.476997
long_sequence: duration=1.500e-06 s, sensing_signal=0.438287, reward=0.288287

Selected configuration: long_sequence
Sensing signal: 0.438287
Physics-informed reward: 0.288287
Policy-gradient loss: 0.000033
```

The example demonstrates the integration of quantum simulation, sensing evaluation, control configuration, and physics-informed policy optimization.

## Validation and Verification

The framework includes automated tests across the major computational layers.

The validation coverage includes:

```text
NV Hamiltonian
Lindblad Dynamics
Pulse Sequences
FEM Modeling
Strain Coupling
Field Data
Spatial NV Sensors
Physical Environment
Quantum Measurement
Adaptive Control
Physics-Informed Learning
```

Run the complete validation suite with:

```bash
pytest
```

The current suite passes:

```text
44 passed
```

The validation strategy checks numerical behavior, physical-model interfaces, input constraints, state representations, control behavior, and learning-policy operations.

This provides a reproducible engineering check when modifying or integrating computational components.

## Extension Design Principles

The extension architecture follows several principles.

### Solver Independence

The NV quantum model does not depend on a particular FEM or multiphysics solver.

### Physical State as an Interface

Physical quantities provide the connection between sensor configuration, environmental modeling, quantum dynamics, sensing, and control.

### Explicit Computational Boundaries

Each major scientific capability has a defined module and validation layer.

### Replaceable Components

A physical model, sensing model, control strategy, or learning policy can be evaluated independently without restructuring the entire simulator.

### Reproducible Testing

Each extension is accompanied by automated validation and a corresponding computational example where applicable.

### Integration Rather Than Duplication

Extensions connect to existing scientific models instead of reproducing the same numerical functionality in separate components.

## Engineering and Product Integration

The architecture is designed for computational testing of sensor configurations before corresponding hardware implementation.

A typical engineering workflow is:

```text
Sensor Configuration
        |
        v
Physical Environment
        |
        v
Multiphysics Simulation
        |
        v
NV Quantum Simulation
        |
        v
Sensing Evaluation
        |
        v
Control Optimization
        |
        v
Configuration Comparison
```

This supports systematic evaluation of how sensor position, orientation, magnetic field, strain, temperature, decoherence, sensing protocol, and control configuration affect the simulated sensor response.

The modular structure also allows a development team to integrate additional physical models or computational methods through defined interfaces rather than coupling the entire system to one solver or algorithm.

## Multiphysics and External Solver Interoperability

The field-data interface is designed to remain independent of the FEM solver that generates the physical-field data.

The built-in Python FEM implementation provides a native computational path for mechanical displacement and strain modeling.

The same interoperability layer can accommodate compatible field data from established multiphysics environments such as:

* COMSOL Multiphysics
* ANSYS
* other compatible finite-element or multiphysics solvers

through appropriate data-exchange formats and Python interoperability mechanisms.

The resulting computational path is:

```text
External FEM / Multiphysics Solver
                |
                v
        Field Data Exchange
                |
                v
         FieldData Interface
                |
                v
          NV Sensor Position
                |
                v
       Local Physical Environment
                |
                v
        NV Quantum Simulation
                |
                v
        Sensing / Control
```

This solver-independent architecture allows the NV simulation layer to operate with physical-field data generated by different computational environments while preserving a common interface for sensor evaluation.

## Framework Extension Workflow

A new scientific capability can be integrated through the same architecture:

```text
Scientific Requirement
        |
        v
Extension Model
        |
        v
Existing Framework Interface
        |
        +── Numerical Implementation
        |
        +── Validation Tests
        |
        +── Reproducible Example
        |
        v
Integrated NV Sensor Workflow
```

The objective is to make each additional capability independently testable while maintaining compatibility with the complete sensor-simulation pipeline.

The resulting architecture provides a practical computational basis for building, testing, integrating, and evaluating NV quantum-sensing capabilities across different physical and engineering configurations.
