from __future__ import annotations

from math import cos, sin

import numpy as np
from numpy import array, matrix


def rotation_matrix(theta: float, u: array) -> matrix:
    u = u / np.sqrt(np.sum(u**2))
    return matrix([
        [
            cos(theta) + (u[0]**2)*(1-cos(theta)),
            u[0]*u[1]*(1-cos(theta)) - u[2]*sin(theta),
            u[0]*u[2]*(1-cos(theta)) + u[1]*sin(theta)
        ],
        [
            u[1]*u[0]*(1-cos(theta)) + u[2]*sin(theta),
            cos(theta) + (u[1]**2)*(1-cos(theta)),
            u[1]*u[2]*(1-cos(theta)) - u[0]*sin(theta)
        ],
        [
            u[2]*u[0]*(1-cos(theta)) - u[1]*sin(theta),
            u[2]*u[1]*(1-cos(theta)) + u[0]*sin(theta),
            cos(theta) + (u[2]**2)*(1-cos(theta))
        ]
    ])


def get_default_output_name(args, u: array):
    name = ""
    name += "perspective_" if args.perspective else ""
    name += "transparent" if args.transparent else "opaque"
    name += "_cube_axis_"
    name += "_".join([str(int(i)) if i.is_integer() else str(i) for i in u])
    name += ".txt"
    return name
