# ⚛️ Quantum-Computing Repository  

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)](https://www.python.org/)
[![Qiskit](https://img.shields.io/badge/Qiskit-0.46%2B-purple?logo=ibm)](https://qiskit.org/)
[![PyQuil](https://img.shields.io/badge/PyQuil-3.4-green?logo=rigetti-computing&logoColor=white)](https://www.rigetti.com/)
[![Cirq](https://img.shields.io/badge/Cirq-1.3-orange?logo=googlecloud)](https://quantumai.google/)
[![Q#](https://img.shields.io/badge/Microsoft-Q%23-blueviolet?logo=microsoft)](https://learn.microsoft.com/en-us/azure/quantum/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)


## 🧠 Overview  

**A cross-platform collection of quantum algorithm implementations and simulations**  
developed in **Cirq (Google)**, **PyQuil (Rigetti)**, **Qiskit (IBM)**, and **Q# (Microsoft QDK)**.  

Each project demonstrates algorithmic reproducibility across multiple SDKs —  
bridging theoretical design, reproducible code, and classical post-processing for quantum computation.


## 🌌 Project Highlights  

| ⚙️ Algorithm | 🧮 Description | 🧩 Framework |
|:-------------|:---------------|:--------------|
| 🌀 **Quantum Fourier Transform (QFT)** | Core subroutine used in phase estimation and Shor’s period finding. | Cirq, Qiskit |
| 🔢 **Shor’s Algorithm** | Integer factorization using modular exponentiation + QFT. | Cirq, PyQuil, Qiskit |
| 🔍 **Grover’s Search** | Quadratic-speedup search across unstructured datasets. | Q# |
| ⚗️ **Hydrogen Simulation** | Ground-state energy estimation via Quantum Phase Estimation or VQE. | Q# |
| 🧱 **Custom Unitaries** | Modular arithmetic and controlled operations constructed from first principles. | PyQuil, Qiskit |
| 🧠 **Cross-SDK Benchmarking** | Demonstrates algorithmic consistency across 4 major quantum platforms. | All |


## 📂 Repository Structure  

```
Quantum-Computing/
│
├── Cirq/
│   ├── QFT.py
│   ├── Shors.py
│   └── Theory.pdf
│
├── PyQuil/
│   ├── Quantum_Gates.py
│   ├── Shors.py
│
├── Qiskit/
│   ├── Quantum_Circuit.py
│   ├── Shors.py
│
├── QSharp/
│   ├── Hydrogen/
│   │   ├── Program.qs
│   │   ├── Driver.cs
│   │   ├── Hydrogen.csproj
│   │   └── Hydrogen.sln
│   └── Grover/
│       ├── Operations.qs
│       ├── Reflections.qs
│       ├── Driver.cs
│       ├── Grover.csproj
│       └── Grover.sln
│
└── README.md
```


## 🚀 Highlights by Platform  

### 🧩 **Cirq — Quantum Fourier Transform & Shor’s Algorithm**
- **`QFT.py`** — Four-qubit QFT simulator verifying unitarity (QFT × QFT† = I).  
- **`Shors.py`** — Complete Shor’s Algorithm implementation (N = 15, b = 8) with Cirq’s simulation tools and classical continued-fraction analysis.  
- **`Theory.pdf`** — Companion paper explaining theoretical derivations and implementation rationale.


### 🧠 **PyQuil — Rigetti QVM Implementation**
- **`Quantum_Gates.py`** — Low-level gate and unitary definitions using `DefGate`.  
- **`Shors.py`** — Shor’s algorithm recreated on the Rigetti QVM with dynamic modular exponentiation and post-processing validation.


### 🔬 **Qiskit — IBM Quantum Simulation**
- **`Quantum_Circuit.py`** — Quantum + classical register scaffolding.  
- **`Shors.py`** — Full factoring workflow with `QFT`, custom modular unitaries, AER backend simulation, and factor recovery (3 × 5).  


### ⚗️ **Q# — Quantum Chemistry & Search**
#### 🧪 *Hydrogen Simulation*
- Simulates hydrogen molecular energy via **QPE/VQE** under the Microsoft QDK.
- Combines `.qs` quantum code and C# host driver.  

#### 🔍 *Grover’s Search*
- Implements **Grover’s Algorithm** over a 5-qubit search space using custom reflection operators.  


## 🧩 Mathematical Core  

| Concept | Purpose | Implemented In |
|----------|----------|----------------|
| **Quantum Fourier Transform (QFT)** | Basis transformation used in period estimation. | Cirq, Qiskit |
| **Shor’s Algorithm** | Polynomial-time integer factoring on quantum circuits. | Cirq, PyQuil, Qiskit |
| **Grover’s Algorithm** | Quadratic-speedup database search. | Q# |
| **Quantum Phase Estimation / VQE** | Eigenvalue estimation for physical systems. | Q# (Hydrogen) |


## 🧪 Simulation Environments  

| Framework | Backend | Description |
|------------|----------|--------------|
| **Cirq** | `cirq.Simulator()` | High-fidelity gate simulation of QFT + Shor subroutines. |
| **PyQuil** | `get_qc("6q-qvm")` | Rigetti virtual machine with dynamic `DefGate` unitaries. |
| **Qiskit** | `Aer.get_backend('qasm_simulator')` | IBM AER simulator with transpiled circuits. |
| **Q#** | `QuantumSimulator()` | Microsoft .NET quantum simulation environment. |


## 🧭 Research Context  

This repository forms part of my **graduate research in Quantum Algorithms and AI-driven Simulation** — integrating physics-inspired computation with algorithmic reproducibility across multiple SDKs.

- **Institutions:** Johns Hopkins University (AI / CS), Drexel University (Physics)  
- **Focus Areas:** QFT, Shor, Grover, VQE, hybrid AI-quantum modeling.  


## ⚙️ Requirements  

```
Python ≥ 3.9
qiskit >= 0.46
cirq >= 1.3
pyquil >= 3.4
Microsoft Quantum Development Kit (Q# + .NET 6+)
```


## 📈 Future Work  

- Extend **VQE** implementations across Qiskit and Q#.  
- Integrate **Phase Estimation benchmarks** across frameworks.  
- Develop a **cross-SDK runtime and fidelity benchmarking suite.**  


## 🧠 Author

**Sabneet Bains** — *Quantum × AI × Scientific Computing*  
[LinkedIn](https://www.linkedin.com/in/sabneet-bains/) • [GitHub](https://github.com/sabneet-bains)


## 📄 License

This repository is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).

