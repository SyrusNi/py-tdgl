import argparse
import os


def parse_args():
    parser = argparse.ArgumentParser(description="parameters for tdgl")

    #layer parameters
    parser.add_argument('--length_units', type=str, default='um')
    parser.add_argument('--coherence_length', type=float, default=0.5)
    parser.add_argument('--london_lambda', type=float, default=2)
    parser.add_argument('--thickness', type=float, default=0.1)
    parser.add_argument('--gamma', type=float, default=1)

    #device geometry
    parser.add_argument('--width', type=float, default=5)
    parser.add_argument('--length', type=float, default=17.5)

    #make mesh
    parser.add_argument('--max_edge_length', type=float, default=0.25)
    parser.add_argument('--smooth', type=int, default=100)

    #solve options
    parser.add_argument('--output_file', type=str, default=os.path.join('solutions', "zero-field.h5"))
    parser.add_argument('--field_units', type=str, default="mT")
    parser.add_argument('--current_units', type=str, default="uA")
    parser.add_argument('--skip_time', type=float, default=100)
    parser.add_argument('--solve_time', type=float, default=150)
    parser.add_argument('--save_every', type=float, default=100)

    args, _ = parser.parse_known_args()

    return args
