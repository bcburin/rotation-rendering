from __future__ import annotations

from argparse import ArgumentParser
from math import pi

from numpy import array

from src.models import Cube, Edge, Point
from src.rendering import AnimationMaker, DrawConfig, RotationAnimationConfig
from src.utils import rotation_matrix, get_default_output_name


def create_parser():
    parser = ArgumentParser()
    parser.add_argument('ux', help='x component of rotation axis')
    parser.add_argument('uy', help='y component of rotation axis')
    parser.add_argument('uz', help='z component of rotation axis')
    parser.add_argument('--period', '-p', help='period of rotation in seconds', default=10)
    parser.add_argument('--delay', '-d', help='delay between frames in seconds', default=3e-2)
    parser.add_argument('--out', '-o', help='output file name', default=None)
    parser.add_argument('--focus', '-f', help='focal distance in the z axis', default=None)
    parser.add_argument('--duration', help='duration of animation in seconds', default=20)
    parser.add_argument('--cube-length', help='length of the side of the cube', default=1)
    parser.add_argument('--transparent', help='renders parts out of sight from focus', action='store_true')
    parser.add_argument('--perspective', help='enables perspective view from focus', action='store_true')
    parser.add_argument('--show-axis', help='show axis of rotation', action='store_true')
    return parser


def draw_rotating_cube_animation(cube_length: float, config: RotationAnimationConfig):
    am = AnimationMaker(config=config)
    # build models
    axis_edge = Edge(Point.from_array(-config.axis), Point.from_array(config.axis))
    cube = Cube(length=cube_length)
    # iterate frames
    for _ in range(config.n_iterations):
        if config.show_axis:
            am.add(axis_edge)
        am.add(cube)
        am.commit()
        cube.rotate(rotation_matrix(theta=config.w * config.delay, u=config.axis))
    am.end()


def main():
    # parse arguments
    parser = create_parser()
    args = parser.parse_args()
    # axis vector and angular velocity
    u = array([float(args.ux), float(args.uy), float(args.uz)])
    w = 2*pi / float(args.period)
    # draw configurations
    draw_config = DrawConfig(
        output_name=args.out or get_default_output_name(args, u),
        focus=float(args.cube_length) * 1000 if not args.perspective
        else float(args.focus) or float(args.cube_length) + 2,
        transparent=args.transparent, perspective=args.perspective)
    # rotation animation configurations
    animation_config = RotationAnimationConfig(
        delay=float(args.delay),
        n_iterations=int(float(args.duration) / float(args.delay)),
        draw_config=draw_config, axis=u, w=w, show_axis=args.show_axis
    )
    # create rotation animation
    draw_rotating_cube_animation(cube_length=args.cube_length, config=animation_config)


if __name__ == '__main__':
    main()
