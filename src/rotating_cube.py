from __future__ import annotations

from abc import ABC, abstractmethod
from argparse import ArgumentParser
from dataclasses import dataclass
from math import cos, sin, pi
from typing import TextIO

from numpy import matrix, array
import numpy as np


class Drawable(ABC):

    @abstractmethod
    def draw(self, file: TextIO):
        ...


class AnimationMaker:

    def __init__(self, output_name: str, delay: float) -> None:
        self._file = open(output_name, 'w+')
        self._delay = delay
        self._buffer: list[Drawable] = []

    def add(self, item: Drawable):
        self._buffer.append(item)

    def commit(self):
        for item in self._buffer:
            item.draw(file=self._file)
        self.delay()
        self.clear()
    
    def delay(self):
        self._file.write('delay\n')
        self._file.write(f'{self.delay}\n')

    def clear(self):
        self._file.write('clrscr\n')

    def end(self):
        self._file.write('end\n')
        self._file.close()



@dataclass
class Point(Drawable):
    x: float
    y: float
    z: float

    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other: Point) -> Point:
        return Point(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def as_array(self) -> array:
        return array([self.x, self.y, self.z])
    
    @staticmethod
    def from_array(a: array | matrix) -> Point:
        if isinstance(a, matrix):
            a = array(a)[0]
        return Point(a[0], a[1], a[2])
    
    def draw(self, file: TextIO):
        file.write('point\n')
        file.write(f'{self.x} {self.z}\n')


@dataclass
class Edge(Drawable):
    point_a: Point
    point_b: Point

    def draw(self, file: TextIO):
        file.write('line\n')
        file.write(f'{self.point_a.x} {self.point_a.y} {self.point_b.x} {self.point_b.y}\n')


@dataclass
class Polygon(Drawable):
    vertices: list[Point]

    def draw(self, file: TextIO):
        edges = [Edge(self.vertices[i], self.vertices[i + 1 % len(self.vertices)]) 
                 for i in range(self.vertices)]
        for edge in edges:
            edge.draw(file)


class Cube(Drawable):

    def __init__(self, length: float, center: Point = Point(0, 0, 0), transparent: bool = True) -> None:
        l = length
        self._l = l
        self._c = center
        # initialize vertices
        self._v = {
            1: center + Point(l/2, l/2, l/2),
            2: center + Point(l/2, l/2, -l/2),
            3: center + Point(l/2, -l/2, -l/2),
            4: center + Point(l/2, -l/2, l/2),
            5: center + Point(-l/2, l/2, l/2),
            6: center + Point(-l/2, l/2, -l/2),
            7: center + Point(-l/2, -l/2, -l/2),
            8: center + Point(-l/2, -l/2, l/2),
        }

    def get_edges(self) -> list[Edge]:
        return [
            Edge(self._v[1], self._v[2]),
            Edge(self._v[2], self._v[3]),
            Edge(self._v[3], self._v[4]),
            Edge(self._v[4], self._v[1]),
            Edge(self._v[5], self._v[6]),
            Edge(self._v[6], self._v[7]),
            Edge(self._v[7], self._v[8]),
            Edge(self._v[8], self._v[5]),
            Edge(self._v[1], self._v[5]),
            Edge(self._v[2], self._v[6]),
            Edge(self._v[3], self._v[7]),
            Edge(self._v[4], self._v[8]),
        ]
    
    def get_faces(self) -> list[Polygon]:
        return [
            Polygon(self._v[1], self._v[2], self._v[3], self._v[4]),
            Polygon(self._v[5], self._v[6], self._v[7], self._v[8]),
            Polygon(self._v[1], self._v[2], self._v[6], self._v[5]),
            Polygon(self._v[2], self._v[6], self._v[7], self._v[3]),
            Polygon(self._v[3], self._v[7], self._v[8], self._v[4]),
            Polygon(self._v[1], self._v[5], self._v[8], self._v[4]),
        ]
    
    def rotate(self, A: matrix):
        for index, vertex in self._v.items():
            self._v[index] = Point.from_array(A @ vertex.as_array())

    def draw(self, file: TextIO):
        for edge in self.get_edges():
            edge.draw(file=file)



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


def draw_rotating_cube_animation(name: str, axis: array, w: float, delay: float = 3e-2, n: int = 1000,
                                 show_axis: bool = False):
    am = AnimationMaker(name, delay)
    cube = Cube(length=1)
    axis_repr = Edge(Point.from_array(-axis), Point.from_array(axis))
    for _ in range(n):
        if show_axis:
            am.add(axis_repr)
        am.add(cube)
        am.commit()
        cube.rotate(A=rotation_matrix(theta=w*delay, u=axis))


def create_parser():
    parser = ArgumentParser()
    parser.add_argument('ux', help='x component of rotation axis')
    parser.add_argument('uy', help='y component of rotation axis')
    parser.add_argument('uz', help='z component of rotation axis')
    parser.add_argument('--period', '-p', help='period of rotation in seconds', default=10)
    parser.add_argument('--delay', '-d', help='delay between frames in seconds', default=3e-2)
    parser.add_argument('--out', '-o', help='output file name', default=None)
    parser.add_argument('--show-axis', help='show axis of rotation', action= 'store_true')
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    u = array([int(args.ux), int(args.uy), int(args.uz)])
    w = 2*pi / float(args.period)
    name = args.out if args.out is not None else f'rotating_cube_axis_{"_".join([str(i) for i in u])}.txt'
    draw_rotating_cube_animation(name=name, axis=u, w=w, delay=args.delay, show_axis=args.show_axis)


if __name__ == '__main__':
    main()
