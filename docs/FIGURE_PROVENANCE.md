# Figure and experiment provenance

This record distinguishes executable simulation code, illustrative data generators and measured experiment artifacts. It does not alter the original notebooks or their outputs.

| Location | Source evidence | Interpretation |
|---|---|---|
| `ReinforcementModel.ipynb`, cell 0 | Solver-backed environment, `train_rl_agent`, `evaluate_agent`, checkpoint write | Can generate training/evaluation measurements when executed. A committed plotted curve alone does not establish a particular run or checkpoint. |
| `ReinforcementModel.ipynb`, cell 1 | Functions named `simulate_learning_curves`, `simulate_ablation_data`, `simulate_transfer_learning_data`, `simulate_sample_efficiency_data` and other simulated comparisons | Illustrative synthetic comparison data. Do not cite as measured DQN/baseline performance. |
| `ReinforcementModel.ipynb`, cell 2 | Accuracy, efficiency and method-comparison plot generators | Generated comparisons. Require a measured-data lineage before use as benchmark evidence. |
| `3-D-Hubbard-Model.ipynb` | Several numerical and plotting programs with different approximations | Inspect the selected cell's model/solver and inputs. A shared filename is not a shared scientific assumption. |
| `plots1/`, `plots2/`, root PNGs | Committed images without a complete per-file run manifest | Historical figures with incomplete immutable provenance; no new accuracy or speedup claim is made from them. |
| `docs/numerical-smoke.json` | Output of `scripts/smoke_solver.py` on the documented small checks | Numerical sanity output, not a trained-agent result. |

For future measured figures, retain raw data, the generating script, commit and checkpoint digests, seeds, configuration and units together. Mark illustrative figures in their captions and filenames. Do not relabel simulated values as measured values when preparing publication, website or resume material.
