This package utilizes the open-source adaptive experimentation platform, Ax, to perform single-fidelity multi-objective Bayesian optimization in the context of an iterative, human-in-the-loop offline experimentation campaign.

It is meant to be used with the goal of constructing the Pareto front of two or more measured objectives, given a set of experimental parameters forming a continuous search space, while performinga set of experiments in a physical lab or computational simulation.

After thorough exploration of the Ax platform, the optimal set of acquisition function, model and generation strategy, given a set of initial training data.

The default state-of-the-art acqusition function used is the qNEHVI function, which can successfully incorporate, known or uknown, experimental and statistical noise into the model.

The package also contains different kinds of visualizations of the results.

- Updated Ax to latest version, careful with new dependencies (original version still in other folder).
- **Also check possible Claude/ChatGPT output for this README.**
