import tdgl
from tdgl.geometry import box, circle
from tdgl.visualization.animate import create_animation
import numpy as np
import h5py
import os
import matplotlib.pyplot as plt
from IPython.display import HTML, display
from parser import parse_args

def make_video_from_solution(
    solution,
    quantities=("order_parameter"),
    fps=20,
    figsize=(5, 4),
):
    """Generates an HTML5 video from a tdgl.Solution."""
    with tdgl.non_gui_backend():
        with h5py.File(solution.path, "r") as h5file:
            anim = create_animation(
                h5file,
                quantities=quantities,
                fps=fps,
                figure_kwargs=dict(figsize=figsize),
            )
            video = anim.to_html5_video()
        return HTML(video)
    
def make_layer(args):
    length_units = args.length_units

    # Material parameters
    layer = tdgl.Layer(coherence_length=args.coherence_length, 
                       london_lambda=args.london_lambda, 
                       thickness=args.thickness, 
                       gamma=args.gamma)

    # Outer geometry of the film
    film = (
        tdgl.Polygon("film", points=box(args.width, args.length))
        .resample(401)
        .buffer(0)
    )

    device = tdgl.Device(
        "weak_link",
        layer=layer,
        film=film,
        length_units=length_units,
    )

    fig, ax = device.draw()
    plt.show()

    device.make_mesh(max_edge_length=args.max_edge_length, smooth=args.smooth)
    fig, ax = device.plot(mesh=True, legend=False)
    _ = ax.set_ylim(-5, 5)
    device.mesh_stats()
    plt.show()

    return device

def solve_tdgl(device, args):

    options = tdgl.SolverOptions(
    # Allow some time to equilibrate before saving data.
    solve_time=args.solve_time,
    output_file=os.path.join(args.output_directory, args.output_file + '.h5'),
    field_units = args.field_units,
    current_units= args.current_units,
    save_every=args.save_every,
    )

    # varying uniform field according to time_factor
    from tdgl.sources import VaryingField, Setpoints

    setpoints = args.setpoints

    func = Setpoints(setpoints, plot_function=True)
    my_scaling = func.get_func()

    applied_vector_potential = (
        VaryingField(args.value, time_factor=my_scaling, field_units=options.field_units, length_units=device.length_units)
    )

    solution = tdgl.solve(
    device,
    options,
    applied_vector_potential=applied_vector_potential,
    )

    return solution

def save_args(args):
    argsDict = args.__dict__
    filename = os.path.join(args.output_directory, args.output_file + '.txt')
    if not os.path.exists(args.output_directory):
        os.makedirs(args.output_directory)
    with open(filename, 'w') as f:
        f.writelines('------------------ start ------------------' + '\n')
        for key, value in argsDict.items():
            f.writelines('{key}: {value} \n'.format(key=key, value=value))
        f.writelines('------------------- end -------------------')
    

def main():
    args = parse_args()
    if os.path.exists(os.path.join(args.output_directory, args.output_file + '.txt')):
        raise ValueError('Log file already exists. Please change the output_directory or the output_file.')
    device = make_layer(args)
    solution = solve_tdgl(device, args)
    save_args(args)

    if args.make_animation:
        video = make_video_from_solution(
        solution,
        quantities=["order_parameter", "phase", "scalar_potential"],
        figsize=(6.5, 4),
        )
        display(video)

if __name__ == '__main__':
    main()