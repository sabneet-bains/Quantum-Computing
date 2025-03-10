import numpy as np
import math
from fractions import Fraction
import random
import collections

from pyquil import Program, get_qc
from pyquil.gates import H, X, MEASURE, SWAP, CPHASE
from pyquil.quil import DefGate

# --------------------------------------------------
# Helper Functions
# --------------------------------------------------

def required_work_qubits(N):
    """
    Compute the minimal number of qubits k such that 2ᵏ ≥ N.
    
    Math: We need k satisfying 2ᵏ ≥ N so that the work register can represent all integers 0, 1, …, N-1.
    """
    return math.ceil(math.log(N, 2))

def dynamic_permutation_matrix(c, N, num_work_qubits):
    """
    Construct the unitary (permutation matrix) U corresponding to modular multiplication by c modulo N.
    
    For each basis state |y⟩:
      - If y < N, U|y⟩ = |(c ⋅ y) mod N⟩.
      - Else, U|y⟩ = |y⟩.
    
    Math: Implements f(y) = c ⋅ y mod N for y ∈ {0, …, N-1}.
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

def controlled_gate(U):
    """
    Given a unitary U (of dimension d×d), return the controlled-U matrix
    of dimension (2d)×(2d) with the standard block-diagonal structure:
         CU = [[I, 0],
               [0, U]].
    """
    d = U.shape[0]
    I = np.eye(d)
    zero = np.zeros((d, d))
    CU = np.block([[I, zero],
                   [zero, U]])
    return CU

def build_modular_exponentiation(p, exp_qubits, work_qubits, b, N):
    """
    Build the controlled modular exponentiation subroutine.
    
    In Shor’s algorithm we need to perform:
         |x⟩|1⟩ → |x⟩|bˣ mod N⟩.
    For a 2-qubit exponent register, write:
         x = x₀ + 2⋅x₁  so that bˣ = b^(x₀) * b^(2⋅x₁).
         
    Define for each exponent qubit j:
         cⱼ = b^(2ʲ) mod N.
         
    For our example (N = 15, b = 8):
         - j = 0: c₀ = 8 mod 15 = 8.
         - j = 1: c₁ = 8² mod 15 = 64 mod 15 = 4.
         
    We then create controlled gates (using our controlled_gate function)
    acting on the work register (which has 2^(work_qubits) dimensions).
    """
    num_work = len(work_qubits)
    # For j = 0:
    c0 = pow(b, 1, N)  # 8 mod 15
    # For j = 1:
    c1 = pow(b, 2, N)  # 64 mod 15 = 4

    # Build the 2^(work_qubits)×2^(work_qubits) unitary matrices
    U_c0 = dynamic_permutation_matrix(c0, N, num_work)
    U_c1 = dynamic_permutation_matrix(c1, N, num_work)
    
    # Construct controlled versions (dimension 2*2^(work_qubits) x 2*2^(work_qubits))
    CU_c0 = controlled_gate(U_c0)
    CU_c1 = controlled_gate(U_c1)
    
    # Define the gates in PyQuil using DefGate.
    gate_name0 = "C_U8"
    def_gate0 = DefGate(gate_name0, CU_c0)
    CU8 = def_gate0.get_constructor()
    
    gate_name1 = "C_U4"
    def_gate1 = DefGate(gate_name1, CU_c1)
    CU4 = def_gate1.get_constructor()
    
    # Add these gate definitions to the program.
    p += def_gate0
    p += def_gate1
    
    # Append the controlled gates.
    # In our circuit, the exponent register is [0,1] and the work register is [2,3,4,5].
    # Apply CU8 with control exp_qubits[0] and targets = work_qubits.
    p.inst(CU8(exp_qubits[0], *work_qubits))
    # Apply CU4 with control exp_qubits[1] and targets = work_qubits.
    p.inst(CU4(exp_qubits[1], *work_qubits))
    
def qft_pyquil(qubits):
    """
    Construct a Quantum Fourier Transform on the given list of qubits.
    
    Math: QFT: |x⟩ → (1/√(2ⁿ)) Σᵧ exp(2πi x y / 2ⁿ)|y⟩.
    For 2 qubits, a simple circuit is used.
    """
    p = Program()
    n = len(qubits)
    # Apply H and controlled phase gates.
    for i in range(n):
        p.inst(H(qubits[i]))
        for j in range(i+1, n):
            angle = np.pi / (2 ** (j - i))
            p.inst(CPHASE(angle, qubits[i], qubits[j]))
    # Reverse the order of qubits with SWAP gates.
    for i in range(n // 2):
        p.inst(SWAP(qubits[i], qubits[n-1-i]))
    return p

def build_full_program(b, N):
    """
    Build the complete PyQuil program for Shor's algorithm.
    
    Steps:
      1. Initialization:
         - Exponent register: prepare uniform superposition: (1/√(2ⁿ)) Σₓ |x⟩.
         - Work register: initialize to |1⟩.
      2. Modular Exponentiation:
         - Compute |x⟩|1⟩ → |x⟩|bˣ mod N⟩ using controlled modular operations.
      3. QFT on exponent register.
      4. Measurement of exponent register.
    """
    prog = Program()
    
    # Define qubit indices:
    # Use 2 qubits for exponent register: [0, 1]
    # Use at least 4 qubits for work register: we choose [2, 3, 4, 5]
    exp_qubits = [0, 1]
    work_qubits = [2, 3, 4, 5]
    total_qubits = exp_qubits + work_qubits  # [0,1,2,3,4,5]
    
    # Classical memory for measuring exponent register:
    ro = prog.declare('ro', 'BIT', len(exp_qubits))
    
    # --- Step 1: Initialization ---
    # Apply Hadamard to exponent register for uniform superposition.
    for q in exp_qubits:
        prog.inst(H(q))
    # Initialize work register to |1⟩.
    # We encode |1⟩ by applying an X gate to the least-significant bit (here, qubit 5).
    prog.inst(X(work_qubits[-1]))
    
    # --- Step 2: Modular Exponentiation ---
    build_modular_exponentiation(prog, exp_qubits, work_qubits, b, N)
    
    # --- Step 3: QFT on the exponent register ---
    prog += qft_pyquil(exp_qubits)
    
    # --- Step 4: Measurement ---
    for i, q in enumerate(exp_qubits):
        prog.inst(MEASURE(q, ro[i]))
    
    return prog, 2 ** len(exp_qubits)

# --------------------------------------------------
# Main Parameters and Program Construction
# --------------------------------------------------

N = 15          # Composite number to factor.
b = 8           # Chosen base (with gcd(b,15)=1).
prog, q = build_full_program(b, N)
print("PyQuil Program:")
print(prog)

# --------------------------------------------------
# Simulation and Classical Post-Processing
# --------------------------------------------------

# Use a 6-qubit QVM.
qc = get_qc("6q-qvm")
# Run the program.
shots = 100
result = qc.run(prog, trials=shots)
# The result is an array of shape (shots, number_of_exponent_qubits).
print("Raw measurement results:")
print(result)

# Combine measurement outcomes into counts.
counts = collections.Counter()
for outcome in result:
    # outcome is an array of bits corresponding to the exponent register.
    # Convert array to a bit-string. Assuming the order is as declared.
    bitstring = ''.join(str(bit) for bit in outcome)
    counts[bitstring] += 1
print("Measurement counts:", dict(counts))

# --------------------------------------------------
# Classical Post-Processing:
# --------------------------------------------------
# Each measurement outcome corresponds to an integer y, where y/2ⁿ ≈ k/r.
# Use continued fraction method to extract candidate period r.
candidate_counts = {}
for outcome, count in counts.items():
    y_val = int(outcome, 2)
    y_over_q = y_val / q
    approx_fraction = Fraction(y_over_q).limit_denominator(q)
    r_candidate = approx_fraction.denominator
    # Validate candidate period:
    # 1. r_candidate must be even and less than N.
    # 2. b^(r_candidate/2) mod N should not equal N - 1.
    if r_candidate < N and r_candidate % 2 == 0:
        if pow(b, r_candidate // 2, N) != N - 1:
            candidate_counts[r_candidate] = candidate_counts.get(r_candidate, 0) + count

if candidate_counts:
    r, freq = max(candidate_counts.items(), key=lambda item: item[1])
    print("Most common candidate period r =", r, "with frequency", freq)
    half_r = r // 2
    mod_val = pow(b, half_r, N)
    factor1 = math.gcd(mod_val - 1, N)
    factor2 = math.gcd(mod_val + 1, N)
    print("Factors:", factor1, "and", factor2)
else:
    print("No valid candidate period found.")
