# On acquisition functions:

# Will use Models.MOO, which uses qNEHVI by default.

# New function based on Monte Carlo Acquisition Function:
# qNEHVI better than SOBOL and PAREGO for MOO - exploring tradeoff space, 
# while  GPEI is only single-objective (see Tutorials + -->)

"""These are different use cases - qNEHVI will explore the Pareto frontier and try to find optimal tradeoffs between your 
objectives. GPEI on the other hand optimizes a single objective (possibly subject to a constraint on the other objective 
if you specify that). If you know exactly what kind of constraint you can tolerate or how to weight your two objectives, 
GPEI will be more sample efficient, but if you try to explore the set of optimal tradeoffs you should use qNEHVI."""

# For batch optimization (or in noisy settings), we strongly recommend using qNEHVI rather than qEHVI 
# because it is # far more efficient than qEHVI and mathematically equivalent in the noiseless setting.

#################################################################################################

""" 
NOTE:
Model can be specified either from the model registry (ax.modelbridge.registry.Models 
or using a callable model constructor [function]. 

ONLY MODELS FROM THE REGISTRY CAN BE SAVED, and thus optimization can only be resumed if 
interrupted when using models from the registry.
"""

# ALTERNATIVE option, but not for our use case (saving model and resume optimization):
# from ax.modelbridge.factory import get_MOO_NEHVI
# So I will use the registry as I want to save the model and resume optimization at a later time.

# Similarly, set custom acquisition function, varying defaults
# - https://ax.dev/tutorials/modular_botax.html
# model = ax.modelbridge.registry.Models.BOTORCH_MODULAR,
# e.g. after max_parallelism:

"""            model_kwargs={        
                "surrogate_specs":
                {
                    "surrogate": ax.models.torch.botorch_modular.model.SurrogateSpec( 
                        botorch_model_class=botorch.models.gp_regression.SingleTaskGP, 
                        # SingleTaskGP: a single-task exact GP that infers a homoskedastic noise level (no noise observations).
                        covar_module_class=gpytorch.kernels.MaternKernel 
                        # covar_module_class=gpytorch.kernels.RBFKernel

                        # gp_kernel – kernel name. Currently only two kernels are supported: “matern” for Matern Kernel and “rbf” for RBFKernel. 
                        # Defaults to “matern”.

                        # The class of Matern kernels is a generalization of the RBF . It has an additional parameter which controls the smoothness of the resulting function. 
                        # The smaller , the less smooth the approximated function is. As ν → ∞ , the kernel becomes equivalent to the RBF kernel.
                        # from: https://scikit-learn.org/stable/modules/generated/sklearn.gaussian_process.kernels.Matern.html
                        
                                                                                    )
                },
                "botorch_acqf_class": botorch.acquisition.monte_carlo.qNoisyExpectedImprovement # qNEHVI
"""
# UCB is another option, but again needs BOTORCH_MODULAR which can't be saved