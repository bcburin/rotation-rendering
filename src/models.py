from __future__ import annotations

from dataclasses import dataclass
from typing import TextIO

import numpy as np
from numpy import matrix, array

from src.rendering import Drawable


@dataclass
class Point(Drawable):
    x: float
    y: float
    z: float

    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other: Point) -> Point:
        return Point(self.x - other.x, self.y - other.y, self.z - other.z)

    def __truediv__(self, other: float) -> Point:
        return Point(self.x/other, self.y/other, self.z/other)

    def __mul__(self, other: float):
        return Point(self.x*other, self.y*other, self.z*other)

    def length(self):
        return np.sqrt(sum(self.as_array()**2))

    def as_array(self) -> array:
        return array([self.x, self.y, self.z])
    
    @staticmethod
    def from_array(a: array | matrix) -> Point:
        if isinstance(a, matrix):
            a = array(a)[0]
        return Point(a[0].item(), a[1].item(), a[2].item())

    def add_perspective(self, focus: float) -> Point:
        return Point(focus * self.x / (focus - self.z), focus * self.y / (focus - self.z), 0)
    
    def draw(self, file: TextIO, focus: float | None = None, transparent: bool = False, perspective: bool = False):
        if self.z == focus:
            return
        file.write('point\n')
        if not perspective:
            file.write(f'{self.x} {self.y}\n')
        else:
            p = self.add_perspective(focus)
            file.write(f'{p.x} {p.y}')


@dataclass
class Edge(Drawable):
    point_a: Point
    point_b: Point

    def draw(self, file: TextIO, focus: float | None = None, transparent: bool = False, perspective: bool = False):
        file.write('line\n')
        if not perspective:
            file.write(f'{self.point_a.x} {self.point_a.y} {self.point_b.x} {self.point_b.y}\n')
        else:
            p_a = self.point_a.add_perspective(focus)
            p_b = self.point_b.add_perspective(focus)
            file.write(f'{p_a.x} {p_a.y} {p_b.x} {p_b.y}\n')


@dataclass
class Polygon(Drawable):
    vertices: list[Point]

    def draw(self, file: TextIO, focus: float | None = None, transparent: bool = False, perspective: bool = False):
        edges = [Edge(self.vertices[i], self.vertices[(i + 1) % len(self.vertices)])
                 for i in range(len(self.vertices))]
        for edge in edges:
            edge.draw(file, focus, transparent, perspective)

    def get_normal_vector(self, ref: Point | None = None):
        a, b, c = self.vertices[0], self.vertices[1], self.vertices[2]
        v1, v2 = a-b, c-b
        n = np.cross(v1.as_array(), v2.as_array())
        # normalize vector
        n = n / np.sqrt(np.sum(n**2))
        # the code below compares the normal found with the distance between a reference
        # point and one of the vertices, and tries to follow the same direction (dot product > 0)
        if ref is not None and np.dot(n, (b-ref).as_array()) < 0:
            n = -n
        return n

    def get_barycenter(self) -> Point:
        s = Point(0, 0, 0)
        for v in self.vertices:
            s = s + v
        return s / len(self.vertices)


class Cube(Drawable):

    def __init__(self, length: float, center: Point = Point(0, 0, 0)) -> None:
        self._l = length
        self._c = center
        self._init_vertices(center, length)

    def _init_vertices(self, center, l):
        self._v = {
            1: center + Point(l / 2, l / 2, l / 2),
            2: center + Point(l / 2, l / 2, -l / 2),
            3: center + Point(l / 2, -l / 2, -l / 2),
            4: center + Point(l / 2, -l / 2, l / 2),
            5: center + Point(-l / 2, l / 2, l / 2),
            6: center + Point(-l / 2, l / 2, -l / 2),
            7: center + Point(-l / 2, -l / 2, -l / 2),
            8: center + Point(-l / 2, -l / 2, l / 2),
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
            Polygon([self._v[1], self._v[2], self._v[3], self._v[4]]),
            Polygon([self._v[8], self._v[7], self._v[6], self._v[5]]),
            Polygon([self._v[5], self._v[6], self._v[2], self._v[1]]),
            Polygon([self._v[2], self._v[6], self._v[7], self._v[3]]),
            Polygon([self._v[3], self._v[7], self._v[8], self._v[4]]),
            Polygon([self._v[4], self._v[8], self._v[5], self._v[1]]),
        ]
    
    def rotate(self, A: matrix):
        for index, vertex in self._v.items():
            self._v[index] = Point.from_array(A @ vertex.as_array())

    def draw(self, file: TextIO, focus: float | None = None, transparent: bool = False, perspective: bool = False):
        if transparent:
            for edge in self.get_edges():
                edge.draw(file, focus, transparent, perspective)
        else:
            for face in self.get_faces():
                n = face.get_normal_vector(ref=self._c)
                a = face.get_barycenter()
                if np.dot((Point(0, 0, focus)-a).as_array(), n) > 0:
                    face.draw(file, focus, transparent, perspective)

