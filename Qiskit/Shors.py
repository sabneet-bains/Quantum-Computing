import numpy as np
import math
import random
from fractions import Fraction
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import Aer
from qiskit.circuit.library import QFT, UnitaryGate
from qiskit import transpile, assemble

# --------------------------------------------------
# Helper Functions
# --------------------------------------------------

def required_work_qubits(N):
    """
    Compute the minimal number of qubits k such that 2ᵏ ≥ N.
    
    Math: We need k with 2ᵏ ≥ N so that the work register can represent all integers in {0, 1, …, N-1}.
    """
    return math.ceil(math.log(N, 2))

def dynamic_permutation_matrix(c, N, num_work_qubits):
    """
    Construct the permutation matrix U for modular multiplication by c modulo N.
    
    For each basis state |y⟩:
      - If y < N, then U|y⟩ = |(c ⋅ y) mod N⟩.
      - Otherwise, U|y⟩ = |y⟩.
    
    Math: This realizes the map f(y) = c ⋅ y mod N for y ∈ {0, …, N-1}.
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

def build_modular_exponentiation(qc, exp_reg, work_reg, b, N):
    """
    Build the controlled modular exponentiation subroutine.
    
    In Shor’s algorithm we want to compute:
      |x⟩|1⟩ → |x⟩|bˣ mod N⟩.
      
    Write x in binary. For a 2-qubit exponent register:
      x = x₀ + 2⋅x₁  so that bˣ = b^(x₀) ⋅ b^(2⋅x₁).
      
    Define for each exponent qubit j:
      cⱼ = b^(2ʲ) mod N.
      
    For our example (N = 15, b = 8):
      - For j = 0: c₀ = 8 mod 15 = 8.
      - For j = 1: c₁ = 8² mod 15 = 64 mod 15 = 4.
      
    The controlled operation on each qubit multiplies the work register by cⱼ.
    """
    # Calculate constants for j = 0, 1
    c0 = pow(b, 1, N)  # 8 mod 15
    c1 = pow(b, 2, N)  # 64 mod 15 = 4
    
    # Build unitary matrices acting on the work register.
    U_c0 = dynamic_permutation_matrix(c0, N, len(work_reg))
    U_c1 = dynamic_permutation_matrix(c1, N, len(work_reg))
    
    # Create UnitaryGate objects.
    gate_c0 = UnitaryGate(U_c0, label="U8")
    gate_c1 = UnitaryGate(U_c1, label="U4")
    
    # Create controlled versions of these gates.
    cgate_c0 = gate_c0.control(1)
    cgate_c1 = gate_c1.control(1)
    
    # Append controlled gates:
    # Convert work_reg (QuantumRegister) to a list of qubits.
    qc.append(cgate_c0, [exp_reg[0]] + list(work_reg))
    qc.append(cgate_c1, [exp_reg[1]] + list(work_reg))

def build_full_circuit(b, N):
    """
    Build the complete Qiskit circuit for Shor's algorithm.
    
    Steps:
      1. Initialization:
         - Prepare the exponent register in uniform superposition:
           (1/√(2ⁿ)) ∑ₓ |x⟩.
         - Initialize the work register to |1⟩.
      2. Modular Exponentiation:
         - Map |x⟩|1⟩ → |x⟩|bˣ mod N⟩ via controlled operations.
      3. Quantum Fourier Transform (QFT):
         - Apply the QFT on the exponent register.
           Math: QFT: |x⟩ → (1/√(2ⁿ)) ∑ᵧ exp(2πi x y/2ⁿ) |y⟩.
         - The measurement outcome approximates k/r.
      4. Measurement:
         - Measure the exponent register.
    """
    # For a 2-qubit exponent register:
    n = 2
    q = 2 ** n  # q = 4
    min_work = required_work_qubits(N)
    work_qubits = max(min_work, 4)  # Ensure work register can represent {0, …, N-1}
    
    exp_reg = QuantumRegister(n, 'exp')
    work_reg = QuantumRegister(work_qubits, 'work')
    c_reg = ClassicalRegister(n, 'c')
    qc = QuantumCircuit(exp_reg, work_reg, c_reg)
    
    # --- Step 1: Initialization ---
    # Apply Hadamard gates to the exponent register to create superposition.
    qc.h(exp_reg)
    # Initialize work register to |1⟩ (assumed to be represented by applying X to the last qubit).
    qc.x(work_reg[work_qubits - 1])
    
    # --- Step 2: Modular Exponentiation ---
    build_modular_exponentiation(qc, exp_reg, work_reg, b, N)
    
    # --- Step 3: Quantum Fourier Transform (QFT) ---
    # Use Qiskit's built-in QFT. The do_swaps=True parameter automatically reverses qubit order.
    qft_circ = QFT(num_qubits=n, do_swaps=True, approximation_degree=0).to_instruction()
    qc.append(qft_circ, exp_reg)
    
    # --- Step 4: Measurement ---
    qc.measure(exp_reg, c_reg)
    
    return qc, q

# --------------------------------------------------
# Main Parameters and Circuit Construction
# --------------------------------------------------

N = 15           # Composite number to factor
b = 8            # Chosen base (with gcd(b, N) = 1)
qc, q = build_full_circuit(b, N)
print(qc.draw())

# --------------------------------------------------
# Simulation and Classical Post-Processing
# --------------------------------------------------

backend = Aer.get_backend('qasm_simulator')
shots = 100

# Transpile the circuit for the backend.
compiled_circuit = transpile(qc, backend)
# Run the transpiled circuit directly (BackendV2 style).
result = backend.run(compiled_circuit, shots=shots).result()
counts = result.get_counts()
print("Measurement counts:", counts)

# Classical Post-Processing:
# Each measurement outcome is a bit string representing the exponent register.
# The QFT ensures the outcome y satisfies: y/2ⁿ ≈ k/r, for some k.
# We use the continued fraction method to extract the candidate period r.
candidate_counts = {}
for outcome, count in counts.items():
    # Convert the outcome (bit string) to an integer.
    y_val = int(outcome, 2)
    y_over_q = y_val / q
    approx_fraction = Fraction(y_over_q).limit_denominator(q)
    r_candidate = approx_fraction.denominator
    
    # Validate candidate period:
    # 1. r_candidate should be even and less than N.
    # 2. Also, ensure that b^(r_candidate/2) mod N ≠ N - 1 (to avoid trivial factors).
    if r_candidate < N and r_candidate % 2 == 0:
        if pow(b, r_candidate // 2, N) != N - 1:
            candidate_counts[r_candidate] = candidate_counts.get(r_candidate, 0) + count

if candidate_counts:
    # Choose the most common candidate period.
    r, freq = max(candidate_counts.items(), key=lambda item: item[1])
    print("Most common candidate period r =", r, "with frequency", freq)
    half_r = r // 2
    mod_val = pow(b, half_r, N)
    factor1 = math.gcd(mod_val - 1, N)
    factor2 = math.gcd(mod_val + 1, N)
    print("Factors:", factor1, "and", factor2)
else:
    print("No valid candidate period found.")
