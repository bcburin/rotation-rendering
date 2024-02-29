from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TextIO


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
