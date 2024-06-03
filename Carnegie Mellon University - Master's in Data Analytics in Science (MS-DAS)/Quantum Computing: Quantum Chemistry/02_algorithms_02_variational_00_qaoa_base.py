# -*- coding: utf-8 -*-
"""02_Algorithms_02_Variational_00_QAOA_Base.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/14OyorlHHZwcG0tfe_eGbBqMo_6LWUx18
"""

# Install relevant packages
!pip install qiskit
!pip install qiskit_aer
!pip install qiskit_algorithms
!pip install pylatexenc
!pip install qiskit_ibm_runtime

## Define the problem from the slides as a graph
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx

# Generating a graph of 4 nodes
n = 5  # Number of nodes in graph
G = nx.Graph()
G.add_nodes_from(np.arange(0, n, 1))
# tuple is (i,j,weight) where (i,j) is the edge
elist = [#(0, 0, 0), (1, 1, 0), (2, 2, 0), (3, 3, 0), (4, 4, 0), # on-site
         (0, 1, 3), (1, 2, 1), (2, 3, 2), (3, 4, 3), (4, 0, 8), # nearest-neighbor
         (1, 3, 4), (0, 3, 7)] # the rest
G.add_weighted_edges_from(elist)

colors = ["r" for node in G.nodes()]
pos = nx.spring_layout(G)

def draw_graph(G, colors, pos):
    default_axes = plt.axes(frameon=True)
    nx.draw_networkx(G, node_color=colors, node_size=600, alpha=0.8, ax=default_axes, pos=pos)
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=edge_labels)

draw_graph(G, colors, pos)

# Computing the weight matrix from the random graph
w = np.zeros([n, n])
for i in range(n):
    for j in range(n):
        temp = G.get_edge_data(i, j, default=0)
        if temp != 0:
            w[i, j] = temp["weight"]
print(w)

# Brute-force explore every possible solution and compute its cost
best_cost_brute = 0
for b in range(2**n):
    x = [int(t) for t in reversed(list(bin(b)[2:].zfill(n)))]
    cost = 0
    for i in range(n):
        for j in range(n):
            cost = cost + w[i, j] * x[i] * (1 - x[j])
    if best_cost_brute < cost:
        best_cost_brute = cost
        xbest_brute = x
    print("case = " + str(x) + " cost = " + str(cost))

colors = ["r" if xbest_brute[i] == 0 else "c" for i in range(n)]
draw_graph(G, colors, pos)
print("\nOne of the best solutions = " + str(xbest_brute) + " cost = " + str(best_cost_brute))

# Generate an Ising Hamiltonian from the weight matrix

from qiskit.quantum_info import SparsePauliOp

def mixed_field_ising_hamiltonian_from_weight_matrix(weight_matrix):
    """Constructs the mixed-field Ising Hamiltonian from a weight matrix."""
    num_qubits = len(weight_matrix)
    # Hamiltonian initialization
    H_terms = []
    H_coeffs = []

    # Add nearest-neighbor ZZ interactions
    for i in range(num_qubits):
      for j in range(i, num_qubits):
        H_term = list("I" * num_qubits)
        if i == j:
          # We assign to the index `num_qubits - i - 1` instead of `i` because
          # Qiskit uses little ENDian notation, so the zeroth qubit's operator
          # is actually the rightmost side of the string
          H_term[num_qubits - i - 1] = "Z"
        else:
          H_term[num_qubits - i - 1] = "Z"
          H_term[num_qubits - j - 1] = "Z"
        # Convert list of strings into a string
        H_terms.append(''.join(H_term))
        H_coeffs.append(weight_matrix[i, j])

    return SparsePauliOp(H_terms, H_coeffs)

def X_hamiltonian(num_qubits, h=1):
    """Constructs the \sum_i X_i Hamiltonian """
    # Hamiltonian initialization
    H_terms = []
    H_coeffs = []

    # Add nearest-neighbor ZZ interactions
    for i in range(num_qubits):
        H_term = list("I" * num_qubits)
        H_term[i] = "X"
        H_terms.append(''.join(H_term)) # Convert list of strings into a string
        H_coeffs.append(h)

    return SparsePauliOp(H_terms, H_coeffs)

hamiltonian = mixed_field_ising_hamiltonian_from_weight_matrix(w)

# Find the ground state by diagonalizing the Hamiltonian, and show that the
# ground state itself and its energy are the same as what you would get from the
# brute-force approach
from qiskit_algorithms import NumPyEigensolver

def sum_upper_triangle(matrix):
    """Sums all the elements in the upper triangle of a square matrix.
        We require this information to convert between the cost function
        and Hamiltonian representations of the MaxCut problem."""
    total = 0
    n = len(matrix)
    for i in range(n):
        for j in range(i + 1, n):
            total += matrix[i][j]
    return total

exact_solver = NumPyEigensolver(k=10)

result = exact_solver.compute_eigenvalues(hamiltonian)
eigenvalues = result.eigenvalues
eigenstates = result.eigenstates

# Ground state is the minimum eigenvalue of the Hamiltonian
ground_state_energy = np.real(min(eigenvalues))
# Get the corresponding eigenstate
minimum_eigenstate = eigenstates[np.argmin(eigenvalues)]

# Convert the eigenstate to a dictionary by mapping bitstrings to amplitudes
bitstrings_amplitudes = {}
for i, amplitude in enumerate(minimum_eigenstate):
    bitstring = format(i, 'b').zfill(len(w))
    bitstrings_amplitudes[bitstring] = amplitude

print("Minimum eigenvalue:", ground_state_energy)
print("Converting from the Hamiltonian to the cost function, this is a cost of : ",
      str(ground_state_energy / -2 + sum_upper_triangle(w) / 2))
print("Corresponding eigenstate")
# Print the bitstrings and their corresponding amplitudes
for bitstring, amplitude in bitstrings_amplitudes.items():
    print("Bitstring:", bitstring, "Amplitude:", amplitude)

## Now use time evolution to get as close to the ground state as possible

from qiskit import QuantumCircuit, transpile
from qiskit.circuit import Parameter
from qiskit.quantum_info import Operator
import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import expm

def adiabatic_state_preparation_circuit(num_qubits, weight_matrix, time,
                                        trotter_steps, measure_all = False):
    """
    Constructs a circuit for adiabatic state preparation, assuming we start in
    the |-...-> ground state of the \sum_i X_i Hamiltonian, and linearly
    increasing the contribution of the input Hamiltonian defined by `weight_matrix`

    Parameters:
    -

    Returns:
    - A Qiskit QuantumCircuit for
    """
    # Time step for Trotterization
    if time > 0:
      dt = time / trotter_steps
    else:
      dt = 0

    # Initialize circuit
    circuit = QuantumCircuit(num_qubits)

    # Initialize in the |-...-> state
    for i in range(num_qubits):
        circuit.h(i)
        circuit.z(i)

    for step in range(trotter_steps):
        # Evolution from the \sum_i h X_i Hamiltonian, where h=1
        for i in range(num_qubits):
            circuit.rx(- 2 * 3 * dt * (1 - (step +1) / trotter_steps), i)
        # Evolution from Ising Hamiltonian encoding our target problem
        for i in range(num_qubits):
            for j in range(i, num_qubits):
                if i == j:
                    circuit.rz(- 2 * weight_matrix[i, i] * dt * (step+1) / trotter_steps, i)
                else:
                    circuit.rzz(- 2 * weight_matrix[i, j] * dt * (step+1) / trotter_steps, i, j)

    if measure_all:
        circuit.measure_all()

    return circuit

time = 4
trotter_steps = 100 * time

circuit = adiabatic_state_preparation_circuit(num_qubits=5, weight_matrix=w, time=time, trotter_steps=trotter_steps)
circuit_with_meas = adiabatic_state_preparation_circuit(num_qubits=5, weight_matrix=w, time=time, trotter_steps=trotter_steps, measure_all=True)
if trotter_steps < 3:
    circuit.draw('mpl', fold=-1)

from qiskit_aer import QasmSimulator
from qiskit.primitives import StatevectorEstimator, StatevectorSampler
from qiskit.quantum_info import SparsePauliOp
import numpy as np


def compute_energy(circuit, hamiltonian):
    """
    Computes the energy of a given quantum circuit using the Estimator primitive.
    """
    job_estimator = StatevectorEstimator().run([(circuit, hamiltonian)])
    return job_estimator.result()[0].data.evs

def sample_counts(circuit):
    """
    Samples the counts of a circuit with measurements already attached
    """
    job_sampler = StatevectorSampler().run([(circuit)])
    return job_sampler.result()[0].data.meas.get_counts()

energy = compute_energy(circuit, hamiltonian)
counts = sample_counts(circuit_with_meas)
print(f"Energy: {energy}")
print(f"Counts: {counts}")

# Sweep over the time
time_list = [i * 0.1 for i in range(100)]
trotter_step_list = [100 for _ in time_list]

energy_list = []
for time, trotter_step in zip(time_list, trotter_step_list):
    qc = adiabatic_state_preparation_circuit(num_qubits=len(w), weight_matrix=w, time=time, trotter_steps=trotter_step)
    energy_list.append(compute_energy(qc, hamiltonian))

import matplotlib.pyplot as plt

plt.plot(time_list, energy_list, label='Adiabatic state preparation')
plt.xlabel('Time')
plt.ylabel('Energy')
plt.legend()

## Now let's adapt our previous work for QAOA
from qiskit import QuantumCircuit, transpile
from qiskit.circuit import Parameter

def qaoa_circuit(num_qubits, weight_matrix, layers, params = None, measure_all = False):
    """
    Constructs a circuit for QAOA. Instead of "trotter steps", since the total
    evolution time is not defined, we call them "layers".

    Parameters:
    -

    Returns:
    - A Qiskit QuantumCircuit for
    """
    if params is None:
      params = [0.1, 0.1]
    # Initialize circuit
    circuit = QuantumCircuit(num_qubits)

    # Initialize in the |-...-> state
    for i in range(num_qubits):
        circuit.h(i)
        circuit.z(i)

    # Alternating layers of Rx(param[0]) and Rz/Rzz(param[1])
    # Evolution from the \sum_i h X_i Hamiltonian, where h=1
    for i in range(num_qubits):
        circuit.rx(- 2 * params[0], i)
    # Evolution from Ising Hamiltonian encoding our target problem
    for i in range(num_qubits):
        for j in range(i, num_qubits):
            if i == j:
                circuit.rz(- 2 * weight_matrix[i, i] * params[1], i)
            else:
                circuit.rzz(- 2 * weight_matrix[i, j] * params[1], i, j)
    if measure_all:
        circuit.measure_all()

    return circuit

num_qubits = 5
layers = 3

circuit = qaoa_circuit(num_qubits, w, layers)
circuit_with_meas = qaoa_circuit(num_qubits, w, layers, measure_all=True)
if trotter_steps < 3:
    circuit.draw('mpl', fold=-1)

from qiskit_algorithms.optimizers import SPSA

num_qubits = 5
layers = 5

def objective_function(params):
    qc = qaoa_circuit(num_qubits, w, layers, params=params)
    energy = compute_energy(qc, hamiltonian)
    return energy

optimizer = SPSA(maxiter=1000)
initial_params = [0.1] * 2  # Initial parameters for the optimizer
result = optimizer.minimize(objective_function, x0=initial_params)

# Print the optimal parameters
print("Result:", result)

