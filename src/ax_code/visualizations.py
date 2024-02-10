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

"""
   
# Define function for automatic data conversion from the Ax dataframe to a list, for visualization purposes.

def data_convert(data_df):
    # Drop the 'sem' column containing NaNs
    data_df = data_df.drop(columns=['sem'])

    # Convert the DataFrame to a list of lists
    data_list = []

    for trial in data_df['trial_index'].unique():
        trial_data = data_df[data_df['trial_index'] == trial]
        
        # Extract data for 'overpotential' and 'overpotential_slope'
        overpotential_data = trial_data.loc[trial_data['metric_name'] == 'overpotential', 'mean'].tolist()[0]
        slope_data = trial_data.loc[trial_data['metric_name'] == 'overpotential_slope', 'mean'].tolist()[0]
        
        # Combine the data into a list of tuples
        trial_data_list = [overpotential_data, slope_data]
        
        # Extend the main list
        data_list.append(trial_data_list)

    # Now data_list has the format I want
    return data_list

######################

# Define function(s) for my own visualizations 

import matplotlib.pyplot as plt

def plot_pareto(data, visualization_type='batch'):
    if visualization_type == 'batch':
        plot_by_batch(data)
    elif visualization_type == 'trial':
        plot_by_trial(data)
    else:
        raise ValueError(f"Invalid visualization_type: {visualization_type}")

def plot_by_batch(data):

    """This split has to be manually adjusted based on the size and number of batches!"""
    batch_1 = data[:10]
    batch_2 = data[10:13]
    batch_3 = data[13:]

    plt.figure(figsize=(10, 6))
    plt.scatter(*zip(*batch_1), label='Batch 1', marker='o', color='b')
    plt.scatter(*zip(*batch_2), label='Batch 2', marker='s', color='g')
    plt.scatter(*zip(*batch_3), label='Batch 3', marker='^', color='r')

    plt.xlabel('Overpotential')
    plt.ylabel('Overpotential Slope')
    plt.title('Observed Pareto Front')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_by_trial(data):
    trials = list(range(len(data)))
    colormap = plt.cm.get_cmap('coolwarm', len(trials))

    plt.figure(figsize=(10, 6))
    for i, (overpotential, slope) in enumerate(data):
        color = colormap(i)
        plt.scatter(overpotential, slope, label=f'Trial {i}', color=color, marker='o', s=50)

    plt.xlabel('Overpotential')
    plt.ylabel('Overpotential Slope')
    plt.title('Observed Pareto Front (Color-coded by Trial)')
    plt.legend()
    plt.grid(True)
    plt.show()

######################

import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

def plot_pareto_objective(data, visualization_type='value'):
    if visualization_type == 'value':
        plot_by_value(data)
    elif visualization_type == 'slope':
        plot_by_slope(data)
    else:
        raise ValueError(f"Invalid visualization_type: {visualization_type}")

def plot_by_value(data):
    trials = list(range(len(data)))
    overpotential, slope = zip(*data)

    cmap = plt.get_cmap('viridis')
    
    """
    Normalizing values v_min and v_max of the color map - 
    might have to be set manually depending on the objectives
    """

    norm = Normalize(vmin=min(overpotential + slope), vmax=max(overpotential + slope))

    plt.figure(figsize=(10, 6))
    sc = plt.scatter(overpotential, slope, c=overpotential, cmap=cmap, norm=norm, marker='o', s=50)

    cbar = plt.colorbar(sc, format='%.1f')
    cbar.set_label('Color Scale (Overpotential)')

    plt.xlabel('Overpotential')
    plt.ylabel('Overpotential Slope')
    plt.title('Observed Pareto Front (Color-coded by Value)')

    plt.grid(True)
    plt.show()

def plot_by_slope(data):
    trials = list(range(len(data)))
    overpotential, slope = zip(*data)

    cmap = plt.get_cmap('viridis')
    
    """
    Normalizing values v_min and v_max of the color map - 
    might have to be set manually depending on the objectives
    """
    norm = Normalize(vmin=-0.05, vmax=+0.1)

    plt.figure(figsize=(10, 6))
    sc = plt.scatter(overpotential, slope, c=slope, cmap=cmap, norm=norm, marker='o', s=50)

    cbar = plt.colorbar(sc, format='%.4f')
    cbar.set_label('Color Scale (Overpotential Slope)')

    plt.xlabel('Overpotential')
    plt.ylabel('Overpotential Slope')
    plt.title('Observed Pareto Front (Color-coded by Overpotential Slope)')

    plt.grid(True)
    plt.show()