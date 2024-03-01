from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TextIO

from numpy import array


@dataclass
class DrawConfig:
    output_name: str
    focus: float
    transparent: bool = False
    perspective: bool = False
    output: TextIO | None = None


class Drawable(ABC):

    @abstractmethod
    def draw(self, config: DrawConfig):
        ...


@dataclass
class AnimationConfig:
    delay: float
    n_iterations: int
    draw_config: DrawConfig


@dataclass
class RotationAnimationConfig(AnimationConfig):
    axis: array
    w: float  # angular velocity
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
        self.delay()
        self.clear()

    def delay(self):
        self._output.write('delay\n')
        self._output.write(f'{self.delay}\n')

    def clear(self):
        self._output.write('clrscr\n')

    def end(self):
        self._output.write('end\n')
        if self._owns_output:
            self._output.close()
            self._config.draw_config.output = None
