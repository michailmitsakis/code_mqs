Ni-W Cathode Electrodes - Electrodeposition Optimization with Ax

Overview

This package provides a step-by-step walkthrough of optimizing an electrodeposition process using Bayesian optimization with the the open-source adaptive experimentation platform, Ax, to perform single-fidelity multi-objective Bayesian optimization in the context of an iterative, human-in-the-loop offline experimentation campaign. It is meant to be used with the goal of constructing the Pareto front of two or more measured objectives, given a set of experimental parameters forming a continuous search space, while performing a set of experiments in a physical lab or computational simulation environment.

Specifically, the package loads in experimental electrodeposition data, sets up an Ax optimization experiment by defining a 4-parameter search space, attaches the training data to the experiment, and leverages Bayesian optimization to intelligently suggest new trial parameterizations for evaluation. After completing trials and refitting the model, visualizations and metrics such as cross validation, contour plots, tradeoff curves, slice plots, and hypervolume traceplots are generated to analyze model performance and the multi-objective optimization trace.

The goal of this work is to showcase the common workflow of applying Bayesian optimization and constructing the Pareto tradeoff curve for multiobjective optimization on a real-world system - including data handling, model tuning, parameter suggestions, trial evaluation, diagnostics, and analysis. This provides a template that can be adapted to optimize other processes by modifying the input data and parameter search space.

Contents

The Jupyter notebook provided here contains Python code blocks alongside detailed Markdown commentary that walks through the Ax optimization process, as well as the analysis and visualizations generated. 

It begins by importing the necessary Python libraries, including Ax, Matplotlib, Pandas, and NumPy. The experimental electrodeposition data is then preprocessed by loading it in, setting aside input parameters (X) and output objectives (y), and converting it into Pandas dataframes.

An AxClient is constructed to manage the optimization experiment. The search space is defined by specifying the name, type, and bounds for the 4 process parameters to optimize. The optimization is configured to minimize the electrode overpotential while constraining the overpotential slope. Training data is attached to the experiment by passing trials specifying parameterizations and corresponding objectives. Given the Ax platform documentation, the optimal model and generation strategy are provided for this use-case, given a set of initial training data. Further, the default state-of-the-art acqusition function used is the qNEHVI function, which can successfully incorporate known or uknown, experimental and statistical noise into the model.

With the client and experiment set up, Bayesian optimization is used to suggest new trial parameterizations. After evaluating trials in the real system, the newly observed objectives are fed back into the client to complete the trials and eventually construct the Pareto front. Diagnostics are computed such as cross validation, objective contours, tradeoff curves, slice plots, and hypervolume over iterations.

The provided analysis and visualizations offer templates for model performance assessment and multi-objective optimization tracing. The code can be run end-to-end on the demo dataset and then adapted as needed.
