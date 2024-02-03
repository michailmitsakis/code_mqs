This code utilizes the open-source adapative experimentation platform, Ax, to perform single-fidelity multi-objective Bayesian optimization in the context of an iterative, 
human-in-the-loop offline experimentation campaign. It is meant to be used with the goal of constructing the Pareto front of two or more measured objectives, 
given a set of experimental parameters forming a continuous search space, while performinga set of experiments in a physical lab or computational simulation.

The default state-of-the-art acqusition function used is the qNEHVI function, which can successfully incorporate, known or uknown, experimental and statistical noise into the model. 

The package also contains different kinds of visualizations of the results.
