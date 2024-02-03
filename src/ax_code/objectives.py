"""
- On thresholds: 

        # Optional float representing the smallest objective value (respectively largest if minimize=True) that is considered valuable in the context of multi-objective optimization. 
        # In BoTorch and in the literature, this is also known as an element of the reference point vector that defines the hyper-volume of the Pareto front.

        # Optional, will be inferred if not set manually, they help us make use of domain knowledge.
        # Basically only the points within the thresholds will be considered as for the Pareto frontier and objective improvement.

        # Ax will ALWAYS try to find points that optimize objectives BEYOND the specified thresholds, using all available data.
        # Lower bound if maximizing --> it searches and considers optimum points ABOVE threshold
        
        # Set LOWER thresholds if Ax is unable to find any Pareto optimal points with your current data and thresholds. 
        # This gives it more feasible goals.
        # Set HIGHER thresholds if you are getting Pareto optimal results but want to push further. 
        # This sets tougher goals for optimization.

        ##############################################################################################
        
From Balandat:
        
        # The (threshold) reference point should be set to be slightly WORSE (10% is reasonable) than the worst value of each objective 
        # that a decision maker would tolerate. These can be chosen by asking the following question for each of your objectives: 
        
        # For objective A, if all other objectives had amazing values, what is the worst allowable/viable value for
        # objective A from an application standpoint? Phrased conversely, what value of objective A would make the material 
        # inviable in spite of great performance for the other objectives? 
        
        # Then give yourself something like a 10% tolerance on this outcome. For example, if you're MINIMIZING objective A, 
        # and the maximum allowable value is 1.0, then set the outcome constraint to something like yA<= 1.0/0.9=1.11.

        # RESPECTIVELY: If MAXIMIZING, and minimum allowable value is -350, then set the outcome constraint to:
        # yA>= -350 + 0.1*(-350) = -350 - 35 = -385


- On SEM:
        # Result of the evaluation should generally be a mapping of the format: {metric_name -> (mean, SEM)}. 
        # It can also return only the mean as a float, in which case Ax will treat SEM as unknown 
        # and use a model that can INFER it.

- On parallelism (Tradeoff between parallelism and total number of trials):

In Bayesian Optimization (any optimization, really), we have the choice between performing evaluations of 
our function in a sequential fashion (i.e. only generate a new candidate point to evaluate after the 
previous candidate has been evaluated), or in a parallel fashion (where we evaluate multiple candidates 
concurrently). The sequential approach will (in expectation) produce better optimization results, 
since at any point during the optimization the ML model that drives it uses strictly more information 
than the parallel approach. However, if function evaluations take a long time and end-to-end optimization
time is important, then the parallel approach becomes attractive. The difference between the performance 
of a sequential (aka 'fully adaptive') algorithm and that of a (partially) parallelized algorithm is referred 
to as the 'adaptivity gap'.

To balance end-to-end optimization time with finding the optimal solution in fewer trials, 
we opt for a ‘staggered’ approach by allowing a limited number of trials to be evaluated in parallel. 
By default, in simplified Ax APIs (e.g., in Service API) the allowed parallelism for the Bayesian phase 
of the optimization is 3. Service API tutorial has more information on how to handle and change allowed 
parallelism for that API."""