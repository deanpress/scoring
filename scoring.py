import random
import math
import numpy as np
from scipy.optimize import minimize

# Cost function
#
# The expected input is:
#
# 1. A proposed full list of log-probabilities for all items
# 2. A list of (a, b, c) triples from jurors, where a and b are indices, and
#    c is the log of the juror's opinion of how much more value item b provided
#    than item a. If item a is more valuable, then c should be negative.

def cost_function(logits, samples):
    return sum((logits[b] - logits[a] - c) ** 2 for a, b, c in samples)

# Optimization to find best vector of weights on the input logits. For example,
# if the input logits contains three lists and the output is [0.5, 0.5, 0], then
# this means that the optimum is to take a 50/50 average of the first two lists.
# 
# Inputs are (i) the logits themselves, and (ii) the juror samples, in the same
# format as in cost_function

def find_optimal_weights(logits, samples):

    def split_cost(weights):
        combined_logits = [
            sum(w * L[i] for w, L in zip(weights, logits))
            for i in range(len(logits[0]))
        ]
        return cost_function(combined_logits, samples)

    # Initial guess: equal weights
    initial_weights = [1 / len(logits)] * len(logits)

    # Constraint: weights must sum to 1
    constraints = ({'type': 'eq', 'fun': lambda w: sum(w) - 1})

    # Bounds: weights must be between 0 and 1
    bounds = [(0, 1)] * len(logits)

    # Minimize the split cost
    result = minimize(
        split_cost,
        initial_weights,
        bounds=bounds,
        constraints=constraints
    )
    return result.x
