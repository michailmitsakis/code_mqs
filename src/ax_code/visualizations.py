# NOTE:
# CAN'T plot optimization trace as it needs a single objective
# Also need to plot Model performance/Objective improvement vs # of iterations

# https://ax.dev/tutorials/visualizations.html

""" 
Cross validation plot

    CV plots are useful to check how well the model predictions calibrate against the actual measurements. 
    **If all points are close to the dashed line, then the model is a good predictor of the real data.**

    Basically, CV plots show objective plateau, should take >=30-sth trials to optimize 
    (this is for GPEI but might be similar).

    The best way to get prediction accuracy of a botorch model is via cross validation.

    With folds specified as -1 (the default) we perform leave-one-out cross validation, 
    where we predict once for each observation, using all other observations as a training set and using 
    the selected observation as a single-item test set. 

    If we want to understand how the model fit improves over time you may do this after every trial, or use **cross_validate_by_trial(model: ModelBridge, trial: int)** to get the cross validation for all trials up to the trial index specified.

    - This seems to only show a single point though? 

    from ax.modelbridge.cross_validation import cross_validate_by_trial
    model = ax_client.generation_strategy.model
    cv_results_by_trial = cross_validate_by_trial(model, trial = 15)
    render(interact_cross_validation(cv_results_by_trial))


Contour plot

    Shows the response surface.
    The other parameters are fixed in the MIDDLE of their respective ranges.

    - Contour Lines: 
    The contour lines on the plot represent constant values of the response variable 
    (the objective or outcome you're interested in). Each contour line corresponds to a 
    specific value of the response variable.

    - Contour Line Patterns: 
    The contour lines may be closer together or farther apart. When contour lines are close together,
    it indicates that a small change in the input parameters leads to a significant change in the response
    variable. When contour lines are widely spaced, it suggests that changes in the input parameters have a relatively small impact on the response variable.

    - Optimal Regions: In optimization, you're often interested in finding regions on the contour plot where
    the response variable is either maximized or minimized. These regions correspond to the areas where the
    contour lines are closest to the desired optimum value.

    - Sensitivity Analysis: Contour plots can also be used for sensitivity analysis. You can observe how
    changes in the input parameters affect the response variable by examining how the contour lines shift
    or change shape when parameters are adjusted.

Trade-off plot

    Plots the tradeoff between an objective and all other metrics in a model. 
    Here we only have two, so basically the Pareto front.

    = Pareto frontier for 2 objectives, or how one changes when the other does

Slice plot

    Slice plots show the metric outcome as a function of one parameter while fixing the others. They serve a similar function as contour plots.

    slice_values: A dictionary {name: val} for the fixed values of the other parameters. If not provided,
    then the status quo values will be used if there is a status quo, otherwise the mean of numeric parameters
    or the mode of choice parameters. Ignored if fixed_features is specified.

Tile plot

    Tile plots are useful for viewing the effect of each arm. --> confusing?

    e.g. render(interact_fitted(model, rel=False))


###############################################################################
    
Define function(s) for my own visualizations now:

"""

