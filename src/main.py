from __future__ import annotations

from argparse import ArgumentParser
from math import pi

from numpy import array

from src.models import Cube, Edge, Point
from src.rendering import AnimationMaker, DrawConfig, RotationAnimationConfig
from src.utils import get_default_output_name


def create_parser():
    parser = ArgumentParser()
    parser.add_argument('ux', help='x component of rotation axis')
    parser.add_argument('uy', help='y component of rotation axis')
    parser.add_argument('uz', help='z component of rotation axis')
    parser.add_argument('--period', '-p', help='period of rotation in seconds', default=10)
    parser.add_argument('--out', '-o', help='output file name', default=None)
    parser.add_argument(
        '--focus', '-f', help='focal distance in the z axis if perspective is being used', default=None)
    parser.add_argument('--duration', '-d', help='duration of animation in seconds', default=20)
    parser.add_argument('--fps', help='number of frames per second', default=30)
    parser.add_argument('--cube-length', help='length of the side of the cube', default=1)
    parser.add_argument('--transparent', help='renders parts out of sight from focus', action='store_true')
    parser.add_argument('--perspective', help='enables perspective view from focus', action='store_true')
    parser.add_argument('--show-axis', help='show axis of rotation', action='store_true')
    parser.add_argument('--cube-center-x', '--cx', help='initial x coordinate of cube center', default=0)
    parser.add_argument('--cube-center-y', '--cy', help='initial y coordinate of cube center', default=0)
    parser.add_argument('--cube-center-z', '--cz', help='initial z coordinate of cube center', default=0)
    parser.add_argument(
        '--initial-angle', help='initial angle of rotation (in degrees)', default=0)
    parser.add_argument(
        '--single-frame', help='make a single frame animation of a rotated cube', action='store_true')
    return parser


def draw_single_frame_rotated_cube_animation(cube_length: float, cube_center: Point, config: RotationAnimationConfig):
    am = AnimationMaker(config=config)
    cube = Cube(length=cube_length, center=cube_center)
    cube.rotate(theta=config.initial_angle, axis=config.axis)
    am.add(cube)
    am.commit()
    am.delay(time=config.duration)
    am.end()


def draw_rotating_cube_animation(cube_length: float, cube_center: Point, config: RotationAnimationConfig):
    am = AnimationMaker(config=config)
    # build models
    axis_edge = Edge(Point.from_array(-config.axis), Point.from_array(config.axis))
    cube = Cube(length=cube_length, center=cube_center)
    if config.initial_angle != 0:
        cube.rotate(theta=config.initial_angle, axis=config.axis)
    # iterate frames
    for _ in range(int(config.duration * config.fps)):
        if config.show_axis:
            am.add(axis_edge)
        am.add(cube)
        am.frame()
        cube.rotate(theta=config.w * config.delay, axis=config.axis)
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
        focus=None if not args.perspective
        else float(args.focus) if args.focus is not None else float(args.cube_length)*2,
        transparent=args.transparent)
    # rotation animation configurations
    animation_config = RotationAnimationConfig(
        fps=float(args.fps), duration=float(args.duration),
        draw_config=draw_config, axis=u, w=w, show_axis=args.show_axis,
        initial_angle=pi * float(args.initial_angle) / 180
    )
    # create rotation animation
    kwargs = {
        'cube_length': args.cube_length,
        'cube_center': Point(float(args.cube_center_x), float(args.cube_center_y), float(args.cube_center_z)),
        'config': animation_config
    }
    if args.single_frame:
        draw_single_frame_rotated_cube_animation(**kwargs)
    else:
        draw_rotating_cube_animation(**kwargs)


if __name__ == '__main__':
    main()
