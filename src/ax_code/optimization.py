"""
On next suggested trials:

    Every run suggests three new trials (trial 10, 11, and 12), and for the first two, I'm getting the message: 
    "The observations are identical to the last set of observations used to fit the model. Skipping model fitting." 

    This means that the model has determined that the data observed for these trials is very similar to the existing 
    data used to train the model. Therefore, there's little to gain from refitting the model with nearly identical data.
    For the third trial (trial 12), it doesn't display the message, indicating that the data for this trial might be 
    more informative or different enough to warrant retraining the model.

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










"""