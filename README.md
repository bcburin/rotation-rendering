# Rendering of Cube Rotations

This repository contains the source code for a project developed for the Computer Graphics course at IME (2024). It generates a `.txt` file containing graphic descriptions of cube rotation animations based on user-provided configurations, utilizing analytical Euclidean geometry.

The output `.txt` file contains simple instructions to plot points and lines, add delays and clear the screen. They are used by a proprietary graphic interpreter software implement in C using OpenGL, whose code we cannot publish.

## Installation


_If you already have numpy installed globally, you can skip this section._

To run the project, follow these steps:

1. Create and activate a virtual environment. You can refer to the [official python documentation](https://docs.python.org/3/library/venv.html) for instructions tailored to your operating system.
2. Once the virtual environment is activated, install the dependencies by running the following command in your terminal:

```commandline
pip install -r requirements.txt
```

Alternatively, if you don't mind having the dependencies installed globally, you can skip 1 and simply run the command in 2.

## Running the project

The simplest way to run the project is by executing the following command from the project's root folder in your command line:

```bash
python -m src.main {ux} {uy} {uz}
```

Replace {ux}, {uy}, and {uz} with the x, y, and z components of the rotation axis respectively. This command generates an animation of a unit cube rotating with default configurations centered at the origin.

You can view the CLI documentation for more options by running:


```bash
python -m src.main -h
```

This command provides information about various options available for customizing the animation, such as rotation period, output file name, duration, frames per second, cube length, perspective view, and more.

### Examples

```bash
python -m src.main 1 0 0
```

This command generates an animation of a cube rotating around the x-axis.

A more elaborate example is shown below. It creates an animation around the axis (1, 2, 1) with an inital angle of 60 degrees, with perspective projection considering the focus (0, 0, 5). The cube rotates with a period of 5 seconds.
The animation has a total duration of 30 seconds and runs at 20 FPS.

```bash
python -m src.main 1 2 1 --initial-angle 60 --perspective --focus 5 --period 5 --d 30 --fps 20
```

### CLI

Running `python -m src.main -h` whill show you the documentation of the project's CLI:

```
usage: main.py [-h] [--period PERIOD] [--out OUT] [--focus FOCUS] [--duration DURATION] [--fps FPS] [--cube-length CUBE_LENGTH] [--transparent]
               [--perspective] [--show-axis] [--cube-center-x CUBE_CENTER_X] [--cube-center-y CUBE_CENTER_Y] [--cube-center-z CUBE_CENTER_Z]
               [--initial-angle INITIAL_ANGLE] [--single-frame]
               ux uy uz

positional arguments:
  ux                    x component of rotation axis
  uy                    y component of rotation axis
  uz                    z component of rotation axis

options:
  -h, --help            show this help message and exit
  --period PERIOD, -p PERIOD
                        period of rotation in seconds
  --out OUT, -o OUT     output file name
  --focus FOCUS, -f FOCUS
                        focal distance in the z axis if perspective is being used
  --duration DURATION, -d DURATION
                        duration of animation in seconds
  --fps FPS             number of frames per second
  --cube-length CUBE_LENGTH
                        length of the side of the cube
  --transparent         renders parts out of sight from focus
  --perspective         enables perspective view from focus
  --show-axis           show axis of rotation
  --cube-center-x CUBE_CENTER_X, --cx CUBE_CENTER_X
                        initial x coordinate of cube center
  --cube-center-y CUBE_CENTER_Y, --cy CUBE_CENTER_Y
                        initial y coordinate of cube center
  --cube-center-z CUBE_CENTER_Z, --cz CUBE_CENTER_Z
                        initial z coordinate of cube center
  --initial-angle INITIAL_ANGLE
                        initial angle of rotation (in degrees)
  --single-frame        make a single frame animation of a rotated cube
`` 
