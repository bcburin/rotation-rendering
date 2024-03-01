from __future__ import annotations

from argparse import ArgumentParser
from math import pi

from numpy import array

from src.models import Cube, Edge, Point
from src.rendering import AnimationMaker
from src.utils import rotation_matrix


def create_parser():
    parser = ArgumentParser()
    parser.add_argument('ux', help='x component of rotation axis')
    parser.add_argument('uy', help='y component of rotation axis')
    parser.add_argument('uz', help='z component of rotation axis')
    parser.add_argument('--period', '-p', help='period of rotation in seconds', default=10)
    parser.add_argument('--delay', '-d', help='delay between frames in seconds', default=3e-2)
    parser.add_argument('--out', '-o', help='output file name', default=None)
    parser.add_argument('--focus', '-f', help='focal distance in the z axis', default=None)
    parser.add_argument('--cube-length', help='length of the side of the cube', default=1)
    parser.add_argument('--transparent', help='renders parts out of sight from focus', action='store_true')
    parser.add_argument('--perspective', help='enables perspective view from focus', action='store_true')
    parser.add_argument('--show-axis', help='show axis of rotation', action='store_true')
    return parser


def draw_rotating_cube_animation(
        name: str, cube_length: float, axis: array, w: float, delay: float = 3e-2, n: int = 500,
        show_axis: bool = False, focus: float = None, transparent: bool = False, perspective: bool = False):
    am = AnimationMaker(name, delay, focus, transparent, perspective)
    cube = Cube(length=cube_length)
    axis_repr = Edge(Point.from_array(-axis), Point.from_array(axis))
    for _ in range(n):
        if show_axis:
            am.add(axis_repr)
        am.add(cube)
        am.commit()
        cube.rotate(A=rotation_matrix(theta=w * delay, u=axis))
    am.end()


def main():
    parser = create_parser()
    args = parser.parse_args()
    # axis vector
    u = (array([int(args.ux), int(args.uy), int(args.uz)])
         if float(args.ux).is_integer() and float(args.uy).is_integer() and float(args.uz).is_integer()
         else array([float(args.ux), float(args.uy), float(args.uz)]))
    # angular velocity
    w = 2*pi / float(args.period)
    if not args.perspective:
        args.focus = float(args.cube_length) * 1000
    elif args.focus is None:
        args.focus = float(args.cube_length) + 2
    name = (args.out
            if args.out is not None
            else f'{"perspective_" if args.perspective else ""}{"transparent" if args.transparent else "opaque"}_'
                 f'cube_axis_{"_".join([str(i) for i in u])}.txt')
    draw_rotating_cube_animation(
        name=name, cube_length=float(args.cube_length), axis=u, w=w, delay=args.delay,
        show_axis=args.show_axis, focus=float(args.focus), transparent=args.transparent, perspective=args.perspective)


if __name__ == '__main__':
    main()
