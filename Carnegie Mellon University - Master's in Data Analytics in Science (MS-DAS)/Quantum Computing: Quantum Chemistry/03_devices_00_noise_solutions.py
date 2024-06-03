# -*- coding: utf-8 -*-
"""03_Devices_00_Noise_Solutions.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1tbVOzlj_LPHcrIwPbHq3xAXR4M_6W0K9
"""

# Install relevant packages
!pip install qiskit
!pip install qiskit_aer
!pip install --verbose dynacir==0.1.4

from dynacir.dynacir_noisemodel import get_secret_noise_model
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

qc = QuantumCircuit(5)
qc.h(0)
qc.measure_all()

secret_noise_model = get_secret_noise_model()

simulator = AerSimulator()

job = simulator.run(qc, noise_model = secret_noise_model, shots = 10000)
job.result().get_counts()

# There are 3 kinds of errors
# 1. Single-qubit Rz and SX gates -- a little extra rotation around the Z axis
# 2. Two-qubit CX gates -- depolarizing on BOTH qubits
# 3. Measurements -- single-qubit readout error

# Now it's time to identify the CX gate error
# Naively, let's start off by applying CX to the well understood state |00>
qc = QuantumCircuit(2)
qc.cx(0, 1)
qc.measure_all()
job = simulator.run(qc, noise_model = secret_noise_model, shots = 100000)
print(job.result().get_counts())
# I'm supposed to get all shots in |00>
# but what I get is the following:
# {'11': 107, '01': 1113, '10': 1063, '00': 97717}
# Now let's try start off by applying CX to the well understood state |10>
qc = QuantumCircuit(2)
qc.x(0)
qc.cx(0, 1)
qc.measure_all()
job = simulator.run(qc, noise_model = secret_noise_model, shots = 100000)
print(job.result().get_counts())
# I'm supposed to get all shots in |11>
# but what I get is the following:
# {'01': 4945, '00': 394, '10': 4796, '11': 89865}

# Let's identify the measurement error first
# Prepare the |1> state and see how many end up in the |0> state
qc_1 = QuantumCircuit(1, 1)
qc_1.x(0)
qc_1.measure(0, 0)
job = simulator.run(qc_1, noise_model = secret_noise_model, shots = 100000)
print(job.result().get_counts())

# Prepare the |0> state and see how many end up in the |1> state
qc_0 = QuantumCircuit(1, 1)
qc_0.measure(0, 0)
job = simulator.run(qc_0, noise_model = secret_noise_model, shots = 100000)
print(job.result().get_counts())

# We get
# {'0': 4934, '1': 95066}
# {'1': 992, '0': 99008}
# Therefore, P(0|1) is ~0.05, and P(1|0) is ~0.01

import numpy as np
from qiskit_aer.noise import NoiseModel, errors
from qiskit.quantum_info.operators import Operator

def get_secret_noise_model():
    # Create the noise model
    noise_model = NoiseModel()

    # Add readout error
    readout_error = errors.readout_error.ReadoutError([[0.99, 0.01], [0.05, 0.95]])
    noise_model.add_all_qubit_readout_error(readout_error)

    # Add coherent error
    unitary_operator = Operator([[1, 0],[0, np.exp(1j*0.001)]])
    error_gate = errors.coherent_unitary_error(unitary_operator)
    noise_model.add_all_qubit_quantum_error(error_gate, ['rz', 'sx'], warnings=False)

    # Add depolarizing error
    depolarizing_error = errors.depolarizing_error(0.005, 2)
    noise_model.add_all_qubit_quantum_error(depolarizing_error, "cx")

    return noise_model

secret_noise_model = get_secret_noise_model()