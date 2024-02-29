from __future__ import annotations

from dataclasses import dataclass
from typing import TextIO

from numpy import matrix, array

from src.rendering import Drawable, AnimationMaker
from src.utils import rotation_matrix


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
        cube.rotate(A=rotation_matrix(theta=w * delay, u=axis))
