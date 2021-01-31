from argparse import ArgumentParser
from time import time
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go 

from corrector.Lattice import Lattice, nx_template, win_or_lose

def run(A, shear, threshold, NX, H, V):
    A.apply_error(threshold)
    BA = A.correct(NX)
    result = win_or_lose(BA, H, V)
    return result

def repeat(A, shear, threshold, reps, NX, H, V):
    results = []
    for rep in range(reps):
        result = run(A, shear, threshold, NX, H, V)
        results.append(result)
    return results.count(False)/reps

def process():
    parser = ArgumentParser(description="Plot a graph showing probability of successful correction for different lattice dimensions and error thresholds.")
    """parser.add_argument('d_range', type=list,
                        help="Input range of dimensions of qubit lattice you wish to plot.")"""
    """parser.add_argument('shear', type=int,
                        help="Input shear of qubit lattice.")"""
    """parser.add_argument('t_range', type=list,
                        help="Input thresholds (probability of error per qubit) you wish to plot. Format: [start, end, step]")"""
    parser.add_argument('reps', type=int,
                        help="Number of repetitions for set d, shear and threshold parameters.")
    args = parser.parse_args()
    
    t0=time()
    
    """DEFAULT PARAMETERS for d_range, t_range and shear"""
    d_range=[6, 8, 12]
    t_range=list(np.arange(0.02, 0.14, 0.01))
    shear=0
    
    fig = go.Figure()
    
    """Here we are going to set up all the things that only need to be done *once* for each (d, shear, threshold)"""
    for d in d_range:
        y = []
        A = Lattice(d, shear)
        NX = nx_template(d, shear)
        H, V = A.logical_operators()
        for thresh in t_range:
            p_success = repeat(A, shear, thresh, args.reps, NX, H, V)
            y.append(p_success)
        fig.add_trace(go.Scatter(x=t_range, y=y, mode='lines+markers', name=d))
        
    t1=time()

    fig.update_layout(autosize=False,
    width=500,
    height=500,
    xaxis_title='probability of error per qubit',
    yaxis_title='probability of decoder failure')

    fig.write_image("graph_plotly.png")
    
    print("time taken = ", t1-t0)

if __name__ == "__main__":
    process()