"""
def add(a, b):
    return a + b


def test_add():
    assert add(2, 3) == 5
    assert add('space', 'ship') == 'spaceship'
    # assert add(2, '3') == 5
"""
import numpy as np
import pandas as pd
from ax.service.ax_client import AxClient
from ax.service.utils.instantiation import ObjectiveProperties
from ax.modelbridge.registry import Models
from ax.modelbridge.generation_strategy import GenerationStrategy, GenerationStep
import pytest

unique_parameters = ["tungstate_concentration", "current_density", "deposition_time", "pH"] 

def experiment():
    # EXAMPLE, here use actual data
    X_train = np.array([[0.05, 10, 500, 5],
                   [0.05, 50, 300, 6],
                   [0.1, 10, 300, 7],
                   [0.1, 10, 600, 8],

                   [0.1, 50, 600, 7.5],
                   [0.1, 100, 600, 10],
                   [0.1, 50, 400, 6.5],
                   [0.1, 30, 600, 8.5],
                   [0.15, 10, 600, 9.5],
                   [0.15, 50, 300, 9.5],

                   # NEW OPTIMIZATION DATA    
                   ])

    # Convert to dataframe
    X_train = pd.DataFrame(X_train, columns=unique_parameters)

    unique_objectives = ["overpotential", "overpotential_slope"]

    # EXAMPLE, here use actual observations
    y_train = np.array([[-358,0.00015], 
                        [-319,0.000066], 
                        [-377,0.0001], 
                        [-319,-0.000518],
                        [-286,0.00008], 
                        [-312,0.000029], 
                        [-309,-0.000057], 
                        [-290,0.001656],
                        [-329,0.000131], 
                        [-305,-0.000064],

                        # NEW OPTIMIZATION DATA                    
                        ])

    # Convert to dataframe
    y_train = pd.DataFrame(y_train, columns=unique_objectives)

    parameters = [
        {
            "name": "tungstate_concentration",
            "type": "range",
            "bounds": [0.05, 0.2],
            "value_type": "float"  
        },
        {
            "name": "current_density",
            "type": "range",
            "bounds": [5, 125],
            "value_type": "int"  
        },
        {
            "name": "deposition_time",
            "type": "range",
            "bounds": [60, 600],
            "value_type": "int"  
        },
        {
            "name": "pH",
            "type": "range",
            "bounds": [5, 10],
            "value_type": "int"  
        }
    ]
    
    # Set up AxClient instance with desired configuration
    gs = GenerationStrategy(
        steps=[
            GenerationStep(
                model=Models.MOO,
                num_trials=-1,
                max_parallelism=3
            )
        ]
    )
    ax_client = AxClient(generation_strategy=gs)
    ax_client.create_experiment(
        name="NiW",
        parameters=parameters,
        objectives={
            "overpotential": ObjectiveProperties(minimize=False, threshold=-350),
            "overpotential_slope": ObjectiveProperties(minimize=False, threshold=-0.001)
        },
        overwrite_existing_experiment=False,
        is_test=False,
        choose_generation_strategy_kwargs={"max_parallelism_override": 3}
    )
    return ax_client

def test_experiment():
    ax_client = experiment()
    
    # Perform assertions on the experiment object
    assert ax_client.experiment.name == "NiW"

    # Check the number of parameters
    assert len(ax_client.experiment.parameters) == 4
    # Check the number of objectives
    assert len(ax_client.experiment.metrics) == 2

    # Check the names and types of parameters
    parameters = ax_client.experiment.parameters
    for parameter in parameters:
        assert parameter in ["tungstate_concentration", "current_density", "deposition_time", "pH"]
    
    # Check the names and properties of objectives
    objectives = ax_client.experiment.tracking_metrics
    for objective in objectives:
        assert objective in ["overpotential", "overpotential_slope"]
        assert not objective.lower_is_better  # Check that minimize is False
        if objective.name == "overpotential":
            assert objective.target == -350
        elif objective.name == "overpotential_slope":
            assert objective.target == -0.001
