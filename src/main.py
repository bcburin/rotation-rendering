from __future__ import annotations

from argparse import ArgumentParser
from math import pi

from numpy import array

from src.models import draw_rotating_cube_animation


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
