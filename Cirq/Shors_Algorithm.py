'''Quantum Fourier Transform Simulator for Shor's Algorithm'''

import cirq
import numpy as np

# define the initial four qubits
q0 = cirq.GridQubit(0, 0) # |0〉
q1 = cirq.GridQubit(0, 1) # |0〉
q2 = cirq.GridQubit(1, 0) # |0〉
q3 = cirq.GridQubit(1, 1) # |0〉

def main():
    '''Simulates the Four-qubit QFT Circuit'''

    # create and append the quantum circuit
    circuit = cirq.Circuit()
    circuit.append(initialize_QFT(False)) # i.e., QFT
    circuit.append(initialize_QFT(True)) # i.e., QFT†
    print("\n ┼─────────────────────────────────┼\n",
    "│ Four-qubit QFT Circuit (N = 2⁴) │\n",
    "┼─────────────────────────────────┼\n\n")
    print(circuit)

    # simulate the circuit and print the resulting state vector
    result = cirq.Simulator().simulate(circuit)
    print("\n\n⦿  Final State Vector |ψ₄〉:\n\n")
    print(np.around(result.final_state_vector, 7))

def initialize_QFT(inv=False):
    '''Initializes the Four-qubit QFT Circuit'''

    if inv is True:
        sign = -1 # i.e., QFT†
    else:
        sign = 1 # i.e., QFT

    # GATE 1: apply Hadamard to q0
    yield cirq.H(q0)

    # GATE 2: apply controlled R₂ between q0 and q1
    yield cirq.CZPowGate(exponent=sign*0.5)(q0,q1)

    # GATE 3: apply controlled R₃ between q0 and q2
    yield cirq.CZPowGate(exponent=sign*0.25)(q0,q2)

    # GATE 4: apply controlled R₄ between q0 and q3
    yield cirq.CZPowGate(exponent=sign*0.125)(q0,q3)

    # GATE 5: apply Hadamard to q1
    yield cirq.H(q1)

    # GATE 6: apply controlled R₂ between q1 and q2
    yield cirq.CZPowGate(exponent=sign*0.5)(q1,q2)

    # GATE 7: apply controlled R₃ between q1 and q3
    yield cirq.CZPowGate(exponent=sign*0.25)(q1,q3)

    # GATE 8: apply Hadamard to q2
    yield cirq.H(q2)

    # GATE 9: apply controlled R₂ between q2 and q3
    yield cirq.CZPowGate(exponent=sign*0.5)(q2,q3)

    # GATE 10: apply Hadamard to q3
    yield cirq.H(q3)

    # GATE 11: apply swap between q1 and q2
    yield cirq.SWAP(q1,q2)

    # GATE 12: apply final swap between q0 and q3
    yield cirq.SWAP(q0,q3)

if __name__ == '__main__':
    main()
