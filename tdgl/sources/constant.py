import numpy as np

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
    if z.ndim == 0:
        z = z * np.ones_like(x)
    positions = np.array([x.squeeze(), y.squeeze(), z.squeeze()]).T
    positions = (positions * ureg(length_units)).to("m").magnitude
    Bz = Bz * time_factor(t=t)
    Bz = Bz * ureg(field_units)
    A = uniform_Bz_vector_potential(positions, Bz)
    return A.to(f"{field_units} * {length_units}").magnitude

def VaryingField(value: float = 0, time_factor=lambda t: 1.0, field_units: str = "mT", length_units: str = "um"):
    return Parameter(
        varying_field_vector_potential,
        Bz=float(value),
        time_factor=time_factor,
        field_units=field_units,
        length_units=length_units,
        time_dependent=True
    )