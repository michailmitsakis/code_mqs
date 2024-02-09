"""
"The observations are identical to the last set of observations "
"used to fit the model. Skipping model fitting."

MORE INFO ON THIS 'ERROR' HERE - https://github.com/facebook/Ax/issues/1930:

"It's hard to say without a better understanding of exactly what code you're running, but the error is coming
from here --> https://github.com/facebook/Ax/blob/cc89030ddefa0f27369148f61d90cb62f5ce56f8/ax/modelbridge/torch.py#L643)

Ax/ax/modelbridge/torch.py 
--> line 643 in def(fit)

if self.model is not None and observations == self._last_observations:
    logger.info(
        "The observations are identical to the last set of observations "
        "used to fit the model. Skipping model fitting."

It can happen if no new observations have been added (and won't happen if new observations have
been added but they are identical to past observations). Is it possible that all of your trials in a batch
have been marked failed, which would result in no new data is being passed to _fit? That would be consistent
with this message being less likely with high parallelism. 
(Note also that this is an info log and optimizationcan proceed.)"

More on model instantiation:

ax_client.fit_model()
print('model:', ax_client.generation_strategy.model)

# This should already be called at every get_next_trial() call.

# From the documentation:
# Model update is normally tied to the GenerationStrategy.gen() call,
# which is called from get_next_trial(). In order to ensure that predictions
# can be performed without the need to call get_next_trial(), we update the
# model with all attached data. Note that this method keeps track of previously
# seen trials and will update the model if there is newly attached data.

##################################

Generation strategy comments:

        # Quasi-random Sobol sequence along with my initial data
        # GenerationStep(
            # model=Models.SOBOL, 
            # num_trials=5,  # How many trials to produce during generation step
            # min_trials_observed=3,  # How many trials to be completed before next model
            # max_parallelism=5  # Max parallelism for this step
        # ),
        ################
        # Skips SOBOL sampling step (which is the default first step) and uses the initial data provided
        # Bayesian optimization step (requires data obtained from previous phase and learns
        # from all data available at the time of each new candidate generation call)

On next suggested trials:

    Every run suggests three new trials (trial 10, 11, and 12), and for the first two, I'm getting the message: 
    "The observations are identical to the last set of observations used to fit the model. Skipping model fitting." 

    This means that the model has determined that the data observed for these trials is very similar to the 
    existing data used to train the model. Therefore, there's little to gain from refitting the model with nearly 
    identical data. For the third trial (trial 12), it doesn't display the message, indicating that the data for
    this trial might be more informative or different enough to warrant retraining the model.

    Basically the first 2 recommendations are quite similar to each other, when looking at the proposed parameters, 
    so the model doesn't need to be retrained. The third one is different enough to warrant retraining the model.

On Pareto optimal parameters:

    **ax_client.get_pareto_optimal_parameters():** 
    Identifies the best parameterizations tried in the experiment so far, using model predictions if 
    use_model_predictions is true and using observed values from the experiment otherwise. 
    By default, uses model predictions to account for observation noise.

    use_model_predictions: Whether to extract the Pareto frontier using model predictions or directly observed values.
    If True, the metric means and covariances in this method's output will also be based on model predictions and 
    may differ from the observed values.

    **By lowering thresholds, we can actually find Pareto optimal solutions.**

    This confirms that the previous issue was the lack of coverage of the objective space, preventing identification 
    of Pareto optimal points with the default higher thresholds. Now with lower thresholds, Ax can find trials that 
    do optimize each objective past the minimum bar I set. And by finding multiple such trials,
    it can determine the full Pareto front.

    Dictionary outputs:

    The first dictionary represents the parameter values for the trial.
    (e.g., 'tungstate_concentration': 0.1, 'current_density': 50, 'deposition_time': 600, 'temperature': 60).

    The second dictionary contains the mean values of the objectives for this parameterization. 
    (e.g., 'overpotential': -288.65735513081376, 'overpotential_slope': 5.1357668682255796e-05') 

    The third dictionary contains the **covariance matrix between the objectives**. 
    The covariance matrix reflects the relationship between the two objectives. 
    It tells us **how the variation in one objective might relate to the variation in another**. 

On covariance:

    In this example, the values seem to be zero or very small, suggesting little correlation between the 
    objectives, i.e.  changes in one objective (e.g., overpotential) are not strongly correlated with changes 
    in the other objective (e.g., overpotential slope). In other words, optimizing for one objective might not 
    have a significant impact on the other objective.

    According to this, they are thus decoupled and independent of each other, suggesting they do not actually possess trade-offs. **BUT according to domain knowledge we know that is almost always NOT true.**

Explanation of discrepancy between covariance matrix and domain knowledge considerations:

    **Sample Size:** The covariance matrix's accuracy heavily depends on the amount of data available. 
    If you have a small sample size, the covariance values might not accurately 
    capture the true relationships between objectives.

    **Nonlinear Relationships:** If the relationship between your objectives is nonlinear, covariance might 
    not accurately capture it. A high covariance doesn't necessarily indicate a linear relationship, and a 
    low covariance doesn't necessarily indicate independence in nonlinear scenarios.

    **Measurement Noise:** Noise in the measurements of your objectives can obscure the true underlying 
    relationships, leading to misleading covariance values.

On variance:
    
    The **diagonal** elements of the covariance matrix provide information about the **variance** of each 
    individual objective. In the context of multi-objective optimization, these variances can offer insights 
    into the inherent variability of each objective when the other objectives are held constant.

    **If the diagonal elements of the covariance matrix for one objective are much larger than those of another
    objective, it indicates that the variance (spread) of that objective's values is higher. This might suggest
    that the corresponding objective is more sensitive to changes in the experimental parameters or that there
    is more variability in the objective values in general.**

    Comparing the diagonal elements of the covariance matrix between two objectives can help us understand the 
    relative variability or sensitivity of each objective. If the diagonal element of the covariance matrix for 
    the overpotential objective is much larger than that of the overpotential slope objective, it suggests that 
    the overpotential objective is more variable or sensitive to changes in the experimental parameters compared 
    to the overpotential slope objective.

    In summary, the diagonal elements of the covariance matrix provide insights into the individual variability 
    and sensitivity of each objective, and comparing these elements between objectives can help us understand 
    their relative behaviors in response to parameter changes.

On Pareto front:

    The posterior pareto front is not necessarily the same as the collection of observed optimal pareto points
    found by the optimizer during the trials. The optimizer is trying to find the (single or few) best points
    on the pareto front, but the pareto front itself is a set of points, not a single or a few points.

Alternatively:

    Get Pareto frontier ignoring all modelling and just using the data =
    equivalent to getting Pareto optimal parameters from model predictions from above, no need.

    from ax.plot.pareto_utils import get_observed_pareto_frontiers

    objectives = ax_client.experiment.optimization_config.objective.objectives
    frontier = get_observed_pareto_frontiers(
        experiment=ax_client.experiment,
        data=ax_client.experiment.fetch_data()
    )
    print(frontier)

Noise in the Pareto front:

    There are a few potential contributors to the large error bars:

    - Measurement noise in the physical experiment: This noise directly propagates into uncertainty in the
    Pareto front estimation. Noisy observations lead to broader confidence intervals
    for the predicted Pareto frontier.

    - Model uncertainty: The Bayesian models used, like Gaussian processes, have their own uncertainty in
    predicting outcomes between observed points. This also contributes to broader confidence intervals on
    the estimated Pareto front.

    - Data sparsity: With limited observed data points, there is greater model prediction uncertainty across
    the objective space. More observed trials reduce uncertainty.

    - Optimization algorithm: Some algorithms like NEHVI are designed to quantify uncertainty in the Pareto front.
    But even with noiseless data, there would still be model uncertainty.

    The noise is likely a combination of physical measurement errors and model uncertainty. 
    More observed trials and using methods like NEHVI to quantify uncertainty helps, but some noise is
    intrinsic when estimating the full Pareto front.


On the hypervolume and the difference with get_trace:
    
    - If I want a more accurate representation of the Pareto front, I should use use_model_predictions=FALSE when calculating the hypervolume i..e what 'get_trace' does. The use of model predictions (use_model_predictions=True) can be faster but might not reflect the true Pareto front accurately, especially if the model's predictions deviate significantly from the actual data.
    - For example here the hypervolume value DOESN'T CHANGE AT ALL, according to the model predictions, which is clearly not true. Again, there is probbaly a noise related or model fitting issue here.

On hypervolume improvement:

    When running trial_indices=[10] and [11], the improved upon hypervolume is apparently ZERO, but then is shows a positive value for [12]. This kind of tracks with the message output when being suggested 3 new trials for every batch, for the first 2 out of the 3: 
    "ax.modelbridge.torch: The observations are identical to the last set of observations used to fit the model. Skipping model fitting." 
    This message is missing from the third trial, which is why it is the first one to actually improve upon the hypervolume, after the initial 10 trials. However, this only occurs for use_model_predictions=False and not True, which is weird. 
    
    In any case, **if I see a value of 0, it means that the current trial doesn't contribute to improving the hypervolume compared to the PREVIOUS state**.

    During some sets of iterations, it seems that the optimization process did not find better solutions, as the hypervolume stays the same.

"""