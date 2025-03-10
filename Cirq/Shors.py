import cirq
import numpy as np
from fractions import Fraction
import math
import random
import collections

# ======================================================
# Helper Functions
# ======================================================

def required_work_qubits(N):
    """
    Compute the minimal number of qubits 'k' required such that 2ᵏ ≥ N.
    
    Math: We need k satisfying 2ᵏ ≥ N so that the work register can represent all integers in {0, 1, ..., N-1}.
    """
    return math.ceil(math.log(N, 2))

def dynamic_permutation_matrix(c, N, num_work_qubits):
    """
    Construct the unitary (permutation matrix) U corresponding to modular multiplication by c modulo N.
    
    For each basis state |y⟩:
      - If y < N, then U|y⟩ = |(c ⋅ y) mod N⟩.
      - If y ≥ N, then U|y⟩ = |y⟩ (i.e. it acts as the identity).
    
    Math: This implements the map f(y) = c ⋅ y mod N for y ∈ {0, …, N-1}, leaving other states unchanged.
    """
    dim = 2 ** num_work_qubits
    M = np.zeros((dim, dim), dtype=complex)
    for y in range(dim):
        if y < N:
            new_y = (c * y) % N
            M[new_y, y] = 1
        else:
            M[y, y] = 1
    return M

def build_modular_exponentiation(first_reg, second_reg, b, N):
    """
    Build the controlled modular exponentiation circuit.
    
    In Shor's algorithm, we wish to compute:
       |x⟩|1⟩ → |x⟩|bˣ mod N⟩.
       
    Write x in binary (for example, with 2 bits: x = x₀ + 2x₁). Then:
       bˣ = b^(x₀ + 2x₁) = b^(x₀) ⋅ b^(2x₁).
       
    For each bit j in the exponent register, define:
       cⱼ = b^(2ʲ) mod N.
       
    Then, if bit j is 1, we multiply the work register by cⱼ.
    
    Math: Each controlled unitary implements Uⱼ|y⟩ = |cⱼ ⋅ y mod N⟩, where cⱼ = b^(2ʲ) mod N.
    """
    circuit = cirq.Circuit()
    for j, control_qubit in enumerate(first_reg):
        c_j = pow(b, 2 ** j, N)
        U = dynamic_permutation_matrix(c_j, N, len(second_reg))
        U_gate = cirq.MatrixGate(U)
        controlled_U = U_gate.controlled(num_controls=1)
        circuit.append(controlled_U.on(control_qubit, *second_reg))
    return circuit

def build_full_circuit(first_reg, second_reg, b, N):
    """
    Construct the full circuit for Shor's algorithm.
    
    Steps:
      1. Initialization:
         - Prepare the exponent register in an equal superposition:
           (1/√(2ⁿ)) ∑ₓ |x⟩, where n = number of exponent qubits.
         - Set the work register to |1⟩.
         Math: The overall state becomes |ψ⟩ = (1/√(2ⁿ)) ∑ₓ |x⟩|1⟩.
      
      2. Modular Exponentiation:
         - Apply controlled operations so that:
           |x⟩|1⟩ → |x⟩|bˣ mod N⟩.
      
      3. Quantum Fourier Transform (QFT):
         - Apply QFT on the exponent register.
         Math: QFT maps |x⟩ → (1/√(2ⁿ)) ∑ᵧ exp(2πi x y / 2ⁿ)|y⟩.
         The measurement outcome y is concentrated around multiples of 2ⁿ / r, where r is the period.
      
      4. Measurement:
         - Measure the exponent register to obtain an outcome y.
         - Use classical post‑processing (continued fractions) to approximate y/2ⁿ ≈ k/r and deduce r.
    """
    circuit = cirq.Circuit()
    
    # --- Step 1: Initialization ---
    # Apply Hadamard gates to create an equal superposition in the exponent register.
    circuit.append(cirq.H.on_each(*first_reg))
    # Initialize the work register to |1⟩ (assumes binary representation; here, the last qubit represents 1).
    circuit.append(cirq.X(second_reg[-1]))
    
    # --- Step 2: Modular Exponentiation ---
    circuit += build_modular_exponentiation(first_reg, second_reg, b, N)
    
    # --- Step 3: Quantum Fourier Transform (QFT) ---
    # Apply the QFT to the exponent register.
    circuit.append(cirq.qft(*first_reg))
    # Manually add SWAP gates to reverse the order of qubits, matching conventional QFT output.
    n = len(first_reg)
    for i in range(n // 2):
        circuit.append(cirq.SWAP(first_reg[i], first_reg[n - 1 - i]))
    
    # --- Step 4: Measurement ---
    # Measure the exponent register; the result will be used to estimate the period r.
    circuit.append(cirq.measure(*first_reg, key='first'))
    return circuit

# ======================================================
# Parameters for Factoring N=15 with b=8
# ======================================================
N = 15          # Composite number to factor (N must be odd and composite)
b = 8           # Chosen base, where gcd(b, N) = 1
n = 2           # Number of exponent qubits; with 2 qubits, 2ⁿ = 4 states.
q = 2 ** n      # q = 2ⁿ, which is the resolution for phase estimation.
min_work = required_work_qubits(N)
work_qubits = max(min_work, 4)  # Ensure the work register can represent numbers up to N - 1.

print("Target N =", N)
print("Test integer b =", b)
print("Number of work qubits =", work_qubits)
print("Number of exponent qubits =", n, "so that q =", q)

# ======================================================
# Build Qubit Registers and Circuit
# ======================================================
first_register = [cirq.LineQubit(i) for i in range(n)]
second_register = [cirq.LineQubit(i + n) for i in range(work_qubits)]
circuit = build_full_circuit(first_register, second_register, b, N)
print("\nImproved Circuit:")
print(circuit)

# ======================================================
# Simulation and Batched Post-Processing
# ======================================================
simulator = cirq.Simulator()
repetitions = 100  # Run the circuit multiple times for statistical confidence.

result = simulator.run(circuit, repetitions=repetitions)
all_measurements = result.measurements['first']  # shape: (repetitions, n)

# ======================================================
# Classical Post-Processing: Extracting the Period r
# ======================================================
# Each measurement gives an integer y, where the QFT ensures y/2ⁿ ≈ k/r for some integer k.
# Using the continued fraction method, we approximate y/2ⁿ and deduce r as the denominator.
candidate_counts = collections.Counter()
for meas in all_measurements:
    # Convert measurement bits (assumed big-endian) to integer y.
    y_val = 0
    for bit in meas:
        y_val = (y_val << 1) | bit
    y_over_q = y_val / q  # This fraction approximates k/r.
    approx_fraction = Fraction(y_over_q).limit_denominator(q)
    r_candidate = approx_fraction.denominator

    # Validate candidate period:
    # 1. r_candidate must be even and less than N.
    # 2. Also, b^(r_candidate/2) mod N should not equal N - 1; otherwise, it leads to trivial factors.
    if r_candidate >= N or r_candidate % 2 != 0:
        continue
    half_r = r_candidate // 2
    mod_val = pow(b, half_r, N)
    if mod_val == N - 1:  # This is a trivial factor case.
        continue
    candidate_counts[r_candidate] += 1

# Select the most common candidate period.
if candidate_counts:
    r, count = candidate_counts.most_common(1)[0]
    print("\nMost common valid candidate period r =", r, "appeared", count, "times out of", repetitions, "shots.")
    
    # Final step: Compute the factors.
    # Math: The factors of N are given by gcd(b^(r/2) ± 1, N).
    half_r = r // 2
    mod_val = pow(b, half_r, N)
    factor1 = math.gcd(mod_val - 1, N)
    factor2 = math.gcd(mod_val + 1, N)
    
    if factor1 not in (1, N) and factor2 not in (1, N):
        print("Success: Factors of", N, "are", factor1, "and", factor2)
    else:
        print("Candidate period r did not yield nontrivial factors upon final validation.")
else:
    print("No valid candidate period was found in", repetitions, "shots.")
