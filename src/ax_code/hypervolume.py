import matplotlib.pyplot as plt

def get_hypervolume(ax_client, trial_indices, use_model_predictions):
    """
    Can do this for every trial - by default calculates hypervolume UP TO and INCLUDING the current trial
    Observe difference betweeen use_model_predictions=True/False
    """
    model_true = ax_client.get_hypervolume(trial_indices=trial_indices, use_model_predictions=use_model_predictions)
    return model_true

def plot_hypervolume_trace(ax_client):
    """
    Equivalent to calling _get_hypervolume repeatedly, with an increasing sequence of trial_indices 
    and with use_model_predictions = FALSE, though this does it more efficiently.
    """
    hypervolume_trace = ax_client.get_trace()

    plt.plot(range(1, len(hypervolume_trace) + 1), hypervolume_trace, label='Hypervolume', marker='o', linestyle='-', color='b')
    plt.xlabel('Iteration')
    plt.ylabel('Hypervolume')
    plt.title('Hypervolume over Iterations')
    plt.grid(True)
    plt.legend()
    plt.show()
