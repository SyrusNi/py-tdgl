import argparse
import os
from numpy import ndarray
import numpy as np


def parse_args():
    parser = argparse.ArgumentParser(description="parameters for tdgl")

    #description
    parser.add_argument('--description', type=str, default='vortices', help='description of args')

    #layer parameters
    parser.add_argument('--length_units', type=str, default='um')
    parser.add_argument('--coherence_length', type=float, default=1/3)
    parser.add_argument('--london_lambda', type=float, default=2)
    parser.add_argument('--thickness', type=float, default=0.1)
    parser.add_argument('--gamma', type=float, default=1, help='inelastic electron-phonon scattering, gapless superconductors gamma = 0 or dirty gapped superconductors gamma > 0')

    #device geometry
    parser.add_argument('--width', type=float, default=6)
    parser.add_argument('--length', type=float, default=6)

    #make mesh
    parser.add_argument('--max_edge_length', type=float, default=0.16, help='should be smaller than coherence length')
    parser.add_argument('--smooth', type=int, default=100)

    #solve options
    parser.add_argument('--field_units', type=str, default="mT")
    parser.add_argument('--current_units', type=str, default="uA")
    parser.add_argument('--skip_time', type=float, default=0, help='time of thermalization')
    parser.add_argument('--solve_time', type=float, default=300)
    parser.add_argument('--save_every', type=float, default=100)
    
    #Externel Fields
    parser.add_argument('--setpoints', type=ndarray, default=np.array([[0, 300], [0.39, 0.39]]).T)
    parser.add_argument('--value', type=float, default=1.0)

    #save options
    parser.add_argument('--output_directory', type=str, default='solutions/0821')
    parser.add_argument('--output_file', type=str, default='showup_300', help='name of the simulation and record file')
    parser.add_argument('--make_animation', type=bool, default=False)

    args, _ = parser.parse_known_args()

    return args
