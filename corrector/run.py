from argparse import ArgumentParser
from time import time
import numpy as np
import matplotlib.pyplot as plt

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
    d_range=[3, 4, 5, 6]
    t_range=list(np.arange(0.045, 0.125, 0.005))
    shear=0
    
    """Here we are going to set up all the things that only need to be done *once* for each (d, shear, threshold)"""
    for d in d_range:
        y = []
        A = Lattice(d, shear)
        NX = nx_template(d, shear)
        H, V = A.logical_operators()
        for thresh in t_range:
            p_fail = repeat(A, shear, thresh, args.reps, NX, H, V)
            y.append(p_fail)
        plt.plot(t_range, y, label = d, linewidth=2)
    t1=time()
    plt.legend(title="distance", loc=1, fontsize='small', fancybox=True)
    plt.ylabel('probability of decoder failure')
    plt.xlabel('probability of error per qubit')
    plt.savefig("graph.png")
    print("time taken = ", t1-t0)

if __name__ == "__main__":
    process()