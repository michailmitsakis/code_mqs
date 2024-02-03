This code utilizes the open-source adapative experimentation platform, Ax, to perform single-fidelity multi-objective Bayesian optimization in the context of an iterative, 
human-in-the-loop offline experimentation campaign. It is meant to be used with the goal of constructing the Pareto front of the simultaneous optimization two or more measured objectives, 
given a set of experimental parameters forming a continuous search space, while performinga set of experiments in a physical lab or computational simulation.

The default acqusition function for this use case is the qNEHVI function, which can successfully incorporate experimental and statistical noise in the model.

The package also contains different kinds of visualizations of the results.
