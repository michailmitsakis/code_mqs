def attach_training_data(ax_client, X_train, y_train, unique_objectives):

    """
    Doing this manually while also specifying parameter data types, to avoid odd errors 
    (e.g. initial data is one type, while in the dataframe it is another + need to use 'iloc' function to 
    iterate through the dataframes).
    """

    trial_index = 0
    n_train = X_train.shape[0]

    for i in range(n_train):
        trial_parameters = {
            param: int(value) if param in ["current_density", "deposition_time", "pH"] else float(value)
            for param, value in X_train.iloc[i, :].items()
        }
        
        trial_raw_data = {obj: float(value) for obj, value in zip(unique_objectives, y_train.iloc[i])}
        
        ax_client.attach_trial(trial_parameters)
        ax_client.complete_trial(trial_index=trial_index, raw_data=trial_raw_data)
        
        trial_index += 1