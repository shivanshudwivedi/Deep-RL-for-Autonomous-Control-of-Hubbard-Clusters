"""Check small-cluster numerical invariants without training or running plotting cells.

Loads only the geometry constant and two solver classes from the original notebook.
This is a numerical smoke check, not validation of the physical Hamiltonian or paper.
"""
from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import List

import numpy as np
from scipy.linalg import eigh

ROOT = Path(__file__).resolve().parents[1]
notebook = json.loads((ROOT / "ReinforcementModel.ipynb").read_text())
source = "".join(notebook["cells"][0]["source"])
tree = ast.parse(source)
selected = [
    node for node in tree.body
    if (isinstance(node, ast.ClassDef)
        and node.name in {"SimulationParameters", "ExactDiagonalizationSolver"})
    or (isinstance(node, ast.Assign)
        and any(isinstance(t, ast.Name) and t.id == "GEOMETRIES" for t in node.targets))
]
assert len(selected) == 3, "Notebook structure changed; review the smoke-check extraction"
namespace = {"np": np, "eigh": eigh, "List": List}
exec(compile(ast.Module(body=selected, type_ignores=[]), "notebook-solver", "exec"), namespace)
Parameters = namespace["SimulationParameters"]
Solver = namespace["ExactDiagonalizationSolver"]
results = []
for temperature in (0.0, 0.1, 1.0):
    solver = Solver(Parameters("Tetrahedron", T=temperature))
    assert solver.dim == 70
    assert all(state.bit_count() == 4 for state in solver.basis_states)
    hamiltonian = solver._build_hamiltonian()
    assert np.allclose(hamiltonian, hamiltonian.conj().T)
    values, vectors = eigh(hamiltonian)
    residual = float(np.linalg.norm(hamiltonian @ vectors - vectors * values))
    assert residual < 1e-8
    occupancy = float(solver.solve())
    assert np.isfinite(occupancy) and -1e-12 <= occupancy <= 0.5 + 1e-12
    results.append({"temperature": temperature, "basis_dimension": solver.dim,
                    "eigenpair_residual_norm": residual, "double_occupancy": occupancy})
atomic = Solver(Parameters("Tetrahedron", t0=0.0, T=0.0))
assert abs(atomic.solve()) < 1e-12
print(json.dumps({"scope": "numerical invariants only; not physical validation or trained RL results",
                  "cases": results, "zero_hopping_ground_state_double_occupancy": 0.0}, indent=2))
