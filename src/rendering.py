from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TextIO

from numpy import array


@dataclass
class DrawConfig:
    output_name: str
    focus: float | None
    transparent: bool = False
    output: TextIO | None = None

    @property
    def perspective(self):
        return self.focus is not None


class Drawable(ABC):

    @abstractmethod
    def draw(self, config: DrawConfig):
        ...


@dataclass
class AnimationConfig:
    fps: float
    duration: float
    draw_config: DrawConfig

    @property
    def delay(self):
        return self.fps ** (-1)


@dataclass
class RotationAnimationConfig(AnimationConfig):
    axis: array
    w: float  # angular velocity
    initial_angle: float
    show_axis: bool = False


class AnimationMaker:

    def __init__(self, config=AnimationConfig) -> None:
        if config.draw_config.output is None:
            config.draw_config.output = open(config.draw_config.output_name, 'w+')
            self._owns_output = True
        else:
            self._owns_output = False
        self._config = config
        self._output = config.draw_config.output
        self._buffer: list[Drawable] = []

    def add(self, item: Drawable):
        self._buffer.append(item)

    def commit(self):
        for item in self._buffer:
            item.draw(config=self._config.draw_config)

    def frame(self):
        self.commit()
        self.delay()
        self.clear()

    def delay(self, time: float | None = None):
        self._output.write('delay\n')
        self._output.write(f'{1 / self._config.fps if time is None else time}\n')

    def clear(self):
        self._output.write('clrscr\n')

    def end(self):
        self._output.write('end\n')
        if self._owns_output:
            self._output.close()
            self._config.draw_config.output = None
