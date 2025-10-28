<div align="center"><a name="readme-top"></a>

# ⚛️ Quantum Computing — Multi-SDK Algorithms & Simulations

[![Python](https://img.shields.io/badge/Python-3.9%2B-528ec5?logo=python&logoColor=white&labelColor=0d1117&style=flat)](https://www.python.org/)
[![Qiskit](https://img.shields.io/badge/Qiskit-0.46%2B-6e40c9?logo=ibm&logoColor=white&labelColor=0d1117&style=flat)](https://qiskit.org/)
[![PyQuil](https://img.shields.io/badge/PyQuil-3.4-149f5c?logo=rigetti-computing&logoColor=white&labelColor=0d1117&style=flat)](https://www.rigetti.com/)
[![Cirq](https://img.shields.io/badge/Cirq-1.3-f39c12?logo=googlecloud&logoColor=white&labelColor=0d1117&style=flat)](https://quantumai.google/)
[![Q#](https://img.shields.io/badge/Microsoft-Q%23-6f42c1?logo=microsoft&logoColor=white&labelColor=0d1117&style=flat)](https://learn.microsoft.com/azure/quantum/)
[![License: MIT](https://img.shields.io/badge/License-MIT-2ECC71?labelColor=0d1117&style=flat)](https://choosealicense.com/licenses/mit/)

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/sabneet-bains/Quantum-Computing)

**Algorithms to amplitudes, demystified.**  
<sup>*A cross-platform collection that makes core quantum algorithms reproducible across Cirq, PyQuil, Qiskit, and Q# — with classical post-processing to verify results.*</sup>

<img src="https://github.com/sabneet-bains/Quantum-Computing/blob/master/Quantum%20Computing.png" alt="2D Cellular Automaton Animation" width="800">

</div>

> [!NOTE]
> <sup>Part of the <b>Foundational & Academic</b> collection: educational tools designed with engineering rigor.</sup>


## 🧭 Table of Contents
- [Overview](#-overview)
- [Project Highlights](#-project-highlights)
- [Repository Structure](#-repository-structure)
- [Highlights by Platform](#-highlights-by-platform)
- [Mathematical Core](#-mathematical-core)
- [Simulation Environments](#-simulation-environments)
- [Research Context](#-research-context)
- [Requirements](#-requirements)
- [Quickstart](#-quickstart)
- [Contributing](#-contributing)
- [Author](#-author)
- [License](#-license)


## 🧠 Overview
This repository implements canonical quantum algorithms across **Cirq (Google)**, **PyQuil (Rigetti)**, **Qiskit (IBM)**, and **Q# (Microsoft QDK)**.  
Each implementation is paired with **classical verification** (e.g., continued fractions for phase estimation) to keep results *auditable and reproducible*.

<div align="right">

[![Back to Top](https://img.shields.io/badge/-⫛_TO_TOP-0d1117?style=flat)](#readme-top)

</div>


## 🌌 Project Highlights

| ⚙️ Algorithm | 🧮 Description | 🧩 Framework |
|:-------------|:---------------|:-------------|
| 🌀 **Quantum Fourier Transform (QFT)** | Basis transform central to phase estimation and Shor. | Cirq, Qiskit |
| 🔢 **Shor’s Algorithm** | Integer factorization via modular exponentiation + QFT. | Cirq, PyQuil, Qiskit |
| 🔍 **Grover’s Search** | Quadratic-speedup unstructured search. | Q# |
| ⚗️ **Hydrogen Simulation** | Ground-state energy via **QPE** or **VQE**. | Q# |
| 🧱 **Custom Unitaries** | Modular arithmetic, controls, and composite gates from first principles. | PyQuil, Qiskit |
| 🧠 **Cross-SDK Benchmarking** | Compares algorithm behavior across four stacks. | All |

<div align="right">

[![Back to Top](https://img.shields.io/badge/-⫛_TO_TOP-0d1117?style=flat)](#readme-top)

</div>


## 📂 Repository Structure

````text
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
````

> [!TIP]
> Folder layout mirrors *algorithm × SDK* separability — enabling focused reading, testing, and porting.

<div align="right">

[![Back to Top](https://img.shields.io/badge/-⫛_TO_TOP-0d1117?style=flat)](#readme-top)

</div>


## 🚀 Highlights by Platform

### 🧩 **Cirq — QFT & Shor**
- **`QFT.py`** — Four-qubit QFT with explicit **QFT · QFT† = I** sanity check.  
- **`Shors.py`** — Full factorization demo (N=15, b=8) plus **continued-fraction** recovery.

### 🧠 **PyQuil — Rigetti QVM**
- **`Quantum_Gates.py`** — Low-level unitaries via `DefGate` for custom arithmetic.  
- **`Shors.py`** — Shor on the QVM with modular exponentiation + classical verification.

### 🔬 **Qiskit — IBM AER**
- **`Quantum_Circuit.py`** — Circuit scaffolding with hybrid classical registers.  
- **`Shors.py`** — QFT, composite unitaries, **AER** simulation, and factor extraction (3×5).

### ⚗️ **Q# — Chemistry & Search**
- **Hydrogen** — Ground-state energy via **QPE/VQE**; `.qs` kernels + C# host.  
- **Grover** — 5-qubit search with custom oracle/reflection operators.

<div align="right">

[![Back to Top](https://img.shields.io/badge/-⫛_TO_TOP-0d1117?style=flat)](#readme-top)

</div>


## 🧩 Mathematical Core

| Concept | Purpose | Implemented In |
|:--------|:--------|:---------------|
| **Quantum Fourier Transform (QFT)** | Period estimation & phase unwrapping. | Cirq, Qiskit |
| **Shor’s Algorithm** | Polynomial-time factoring (quantum subroutine + classical CRT/CF). | Cirq, PyQuil, Qiskit |
| **Grover’s Algorithm** | Amplitude amplification for unstructured search. | Q# |
| **QPE / VQE** | Eigenphase/eigenvalue estimation for Hamiltonians. | Q# (Hydrogen) |

> [!NOTE]
> Classical post-processing (continued fractions, CRT, histogram checks) is used to **audit** quantum outputs.

<div align="right">

[![Back to Top](https://img.shields.io/badge/-⫛_TO_TOP-0d1117?style=flat)](#readme-top)

</div>


## 🧪 Simulation Environments

| Framework | Backend | Description |
|:--|:--|:--|
| **Cirq** | `cirq.Simulator()` | High-fidelity gate simulation for QFT + Shor. |
| **PyQuil** | `get_qc("6q-qvm")` | Rigetti QVM with dynamic `DefGate` unitaries. |
| **Qiskit** | `Aer.get_backend("qasm_simulator")` | IBM AER with transpilation and shot statistics. |
| **Q#** | `QuantumSimulator()` | .NET-based state-vector simulation. |

<div align="right">

[![Back to Top](https://img.shields.io/badge/-⫛_TO_TOP-0d1117?style=flat)](#readme-top)

</div>


## 🧭 Research Context
Part of ongoing graduate work in **Quantum Algorithms & AI-assisted Simulation** — emphasizing **reproducibility**, **cross-SDK verification**, and **pedagogical clarity**.

- **Institutions:** Johns Hopkins University (AI/CS), Drexel University (Physics)  
- **Focus:** QFT, Shor, Grover, QPE/VQE, hybrid pipelines.

<div align="right">

[![Back to Top](https://img.shields.io/badge/-⫛_TO_TOP-0d1117?style=flat)](#readme-top)

</div>


## ⚙️ Requirements

````text
Python >= 3.9
qiskit >= 0.46
cirq >= 1.3
pyquil >= 3.4
Microsoft Quantum Development Kit (Q# + .NET 6+)
````
> [!IMPORTANT]
> Some examples assume local simulators (AER/QVM/QuantumSimulator). Real-hardware backends require credentials.

<div align="right">

[![Back to Top](https://img.shields.io/badge/-⫛_TO_TOP-0d1117?style=flat)](#readme-top)

</div>


## 🚀 Quickstart

````bash
# Qiskit
pip install qiskit==0.46.*   # or latest compatible
python Qiskit/Shors.py

# Cirq
pip install cirq==1.3.*
python Cirq/QFT.py

# PyQuil (Rigetti)
pip install pyquil==3.4.*
python PyQuil/Shors.py

# Q# (Microsoft QDK)
# Install .NET 6+, then:
dotnet tool install -g Microsoft.Quantum.IQSharp
dotnet iqsharp install
dotnet build QSharp/Hydrogen/Hydrogen.sln
dotnet run --project QSharp/Hydrogen/Hydrogen.csproj
````

> [!TIP]
> For deterministic comparisons, fix random seeds and keep **shot counts** identical across SDKs.

<div align="right">

[![Back to Top](https://img.shields.io/badge/-⫛_TO_TOP-0d1117?style=flat)](#readme-top)

</div>


## 🤝 Contributing
Contributions are welcome — from algorithm ports and chemistry benchmarks to doc clarity.

**How to Contribute**
1. **Fork** the repo and create a feature branch.  
2. Follow language-specific conventions (PEP-8 / Q# style) and include inline math/refs where helpful.  
3. Add **round-trip verification** and **plots/logs** for new demos.  
4. Open a **pull request** describing approach, assumptions, and validation.

> [!TIP]
> High-value additions: **VQE baselines across SDKs**, **resource estimation**, **noise models**, **Grover oracles** beyond toy problems.

<div align="right">

[![Back to Top](https://img.shields.io/badge/-⫛_TO_TOP-0d1117?style=flat)](#readme-top)

</div>


<div align="center">
  
##
### 👤 Author  
**Sabneet Bains**  
*Quantum × AI × Scientific Computing*  
[LinkedIn](https://www.linkedin.com/in/sabneet-bains/) • [GitHub](https://github.com/sabneet-bains)

##
### 📄 License  
Licensed under the [MIT License](https://choosealicense.com/licenses/mit/)

<sub>“Quantum systems remind us — superposition is not confusion; it’s compressed possibility.”</sub>

</div>
