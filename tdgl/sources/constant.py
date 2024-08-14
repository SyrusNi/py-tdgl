import numpy as np
from numpy import ndarray
import matplotlib.pyplot as plt

from ..em import uniform_Bz_vector_potential, ureg
from ..parameter import Parameter


def constant_field_vector_potential(
    x,
    y,
    z,
    *,
    Bz: float,
    field_units: str = "mT",
    length_units: str = "um",
):
    if z.ndim == 0:
        z = z * np.ones_like(x)
    positions = np.array([x.squeeze(), y.squeeze(), z.squeeze()]).T
    positions = (positions * ureg(length_units)).to("m").magnitude
    Bz = Bz * ureg(field_units)
    A = uniform_Bz_vector_potential(positions, Bz)
    return A.to(f"{field_units} * {length_units}").magnitude


def ConstantField(
    value: float = 0, field_units: str = "mT", length_units: str = "um"
) -> Parameter:
    """Returns a Parameter that computes a constant as a function of ``x, y, z``.
    Args:
        value: The constant value of the field.
    Returns:
        A Parameter that returns ``value`` at all ``x, y, z``.
    """
    return Parameter(
        constant_field_vector_potential,
        Bz=float(value),
        field_units=field_units,
        length_units=length_units,
    )

def varying_field_vector_potential(x, y, z, *, t, time_factor, Bz: float, field_units: str = "mT", length_units: str = "um"):
    if z.ndim == 0 or 1:
        z = z * np.ones_like(x)
    positions = np.array([x.squeeze(), y.squeeze(), z.squeeze()]).T
    positions = (positions * ureg(length_units)).to("m").magnitude
    Bz = Bz * time_factor(t=t)
    Bz = Bz * ureg(field_units)
    A = uniform_Bz_vector_potential(positions, Bz)
    return A.to(f"{field_units} * {length_units}").magnitude

def VaryingField(value: float = 0, time_factor=lambda t: 1.0, field_units: str = "mT", length_units: str = "um"):
    '''
    Returns a Parameter that computes a constant as a function of ``x, y, z``.
    Args:
        value: The unit value V of the field, usually set to 1.0 for convenience.
        time_factor: A function f(t: float) -> float that controls the time dependency of the field. The true value of the field is V * f(t).
        field_units: Units of the field
    Returns:
        A Parameter that returns ``value`` at all ``x, y, z``.
    '''
    return Parameter(
        varying_field_vector_potential,
        Bz=float(value),
        time_factor=time_factor,
        field_units=field_units,
        length_units=length_units,
        time_dependent=True
    )

class Setpoints:
    def __init__(self, setpoints: ndarray, plot_function = False, **kwargs):
        '''
        Define and plot a Piecewise Function.
        Args:
            setpoints: Ndarrays with shape N*2 like ((t1, B1),...,(tN, BN)), serving as the nodes for the piecewise function you want.
        Returns:
            A Piecewise Function
        '''
        self.setpoints = setpoints
        self.kwargs = kwargs
        if plot_function:
            self.plot_time_factor()
    
    def get_func(self):
        return self.time_factor
    
    def time_factor(self, t: float) -> float:
        setpoints = self.setpoints
        if t < setpoints[0, 0]:
            return setpoints[0, 1]
        elif t >= setpoints[-1, 0]:
            return setpoints[-1, 1]
        else:
            for i in range(len(setpoints)):
                ti, Bi = setpoints[i]
                tf, Bf = setpoints[i+1]
                Bi, Bf = float(Bi), float(Bf)
                if ti <= t < tf:
                    return Bi + (Bf-Bi)*(t-ti)/(tf-ti)
                
    def plot_time_factor(self):
        ti = self.setpoints[0, 0]
        tf = self.setpoints[-1, 0]
        T = np.linspace(ti, tf, max(100, 5*len(self.setpoints)))
        B = np.zeros_like(T)
        for i in range(len(T)):
            t = T[i]
            B[i] = self.time_factor(t)
        plt.plot(T, B)
        plt.ylabel('time_factor')
        plt.xlabel('Time/s')
        plt.show()