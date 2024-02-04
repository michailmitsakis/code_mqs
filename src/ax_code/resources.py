"""
Currently updated Ax version: 0.52.0
(original version still in other folder)

#### Resources:
- https://ax.dev/docs/core.html#trial-vs-batched-trial
- https://ax.dev/docs/trial-evaluation.html
- https://ax.dev/docs/bayesopt.html#tradeoff-between-parallelism-and-total-number-of-trials
- https://ax.dev/tutorials/gpei_hartmann_service.html
- https://ax.dev/tutorials/multiobjective_optimization.html
- Offline optimization tutotial: https://www.youtube.com/watch?v=Wyeab_JNBAo
- For more info on qNEHVI and noisy Bayes-Opt in general, see attached papers (e.g. Monte Carlo acquisition function etc.).
- https://botorch.org/docs/models --> See All Models (use Single-Task GPs here) + Noise Explanation

#### How to cite Ax:

AE: A domain-agnostic platform for adaptive experimentation.
Eytan Bakshy, Lili Dworkin, Brian Karrer, Konstantin Kashin, Ben Letham, Ashwin Murthy, Shaun Singh. NeurIPS Systems for ML Workshop, 2018

OR: ==============================

@Article{balandat2019botorch,
  Author = {Balandat, Maximilian and Karrer, Brian and Jiang, Daniel R. and Daulton, Samuel and Letham, Benjamin and Wilson, Andrew Gordon and Bakshy, Eytan},
  Journal = {arxiv e-prints},
  Title = {{BoTorch: A Framework for Efficient Monte-Carlo Bayesian Optimization}},
  Year = {2019},
  url = {https://arxiv.org/abs/1910.06403}
}

"""