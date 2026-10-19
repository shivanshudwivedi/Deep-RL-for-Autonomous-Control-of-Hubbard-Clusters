# Notebook map and reproduction protocol

Cell indices below are **zero-based JSON cell indices**. They identify independent implementations, not a recommended Run All order.

## Notebook map

| Notebook | Cells | Navigation |
|---|---:|---|
| `ReinforcementModel.ipynb` | 3 | 0: parameters, solver, Gym environment, dueling DQN, replay/training/evaluation. 1: simulated learning curves and comparison plotting helpers. 2: generated accuracy/efficiency/method-comparison figures. |
| `3-D-Hubbard-Model.ipynb` | 11 | 0–2: finite-geometry Hamiltonian/eigenstate programs. 3–4: grand-canonical and chemical-potential scans. 5: mean-field program. 6–9: successive exact-diagonalization/mean-field comparisons and menus. 10: geometry/mean-field plotting program. |
| `Eigen_multi_orbital.ipynb` | 6 | 0: interactive original solver. 1: explanatory Markdown. 2–4: successive simulator/occupation/tetrahedron programs. 5: empty. |

Definitions such as `main`, `SimulationParameters` and `ExactDiagonalizationSolver` recur and overwrite earlier definitions. Use a fresh kernel for the chosen program. Notebook main blocks can start expensive work immediately; inspect them before execution.

## RL development environment

Cell 0 imports NumPy, pandas, PyTorch, legacy Gym, Matplotlib and SciPy. The environment uses the older `reset -> observation` and `step -> (observation, reward, done, info)` API. Do not silently replace Gym with Gymnasium without adapting the environment and training code together.

The numerical smoke dependencies are pinned and tested separately. A fully locked RL environment has not been qualified; the following is a development starting point, not a claim of a tested complete training installation:

```bash
python -m pip install jupyterlab pandas matplotlib torch 'gym==0.26.2'
jupyter lab ReinforcementModel.ipynb
```

Use the existing NumPy/SciPy smoke environment. Review GPU-specific PyTorch installation needs for the target machine. Select cell 0 only and reduce episode counts for a development run; keep the actual configuration in the resulting run manifest. Full training can be expensive because every step diagonalizes a Hamiltonian.

## What a reproducible measured run must retain

1. Commit SHA, selected notebook and cell, Python/package versions, hardware and device.
2. All seeds, train/evaluation split, physical sampling ranges and target distributions.
3. Agent hyperparameters, reward and stopping rules, training episode count and checkpoint digest.
4. Raw per-episode records, evaluation seeds and failure cases; evaluate with the network in evaluation mode to disable training dropout.
5. Baseline implementations, identical evaluation inputs and measured runtime boundaries.
6. Aggregate results across independent seeds with uncertainty intervals.
7. A figure-generation script that consumes those records, rather than synthesizing comparison curves.

The existing code seeds common random generators but does not by itself establish deterministic execution across devices or complete multi-seed reproducibility. The current evaluation helper also needs review of inference/dropout behavior before a qualified benchmark.

## Scope of the small numerical check

Run `python scripts/smoke_solver.py` from the repository. It loads only the geometry constant and two class definitions from cell 0 through an explicit AST selection. It intentionally excludes imports of Gym/PyTorch, training and plotting main blocks.

Checks are small deterministic invariants, not a proof of the many-body model. Passing Hermiticity and eigenpair residuals cannot detect a physically incorrect but Hermitian hopping-sign convention. Reference spectra, fermionic anticommutation/sign tests and thermal reference comparisons are separate required scientific checks.
