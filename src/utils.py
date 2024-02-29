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
