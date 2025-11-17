"""Tkinter-based drawing logic for sorting visualization."""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Callable, Generator, Iterable, List, Sequence, Tuple

from .algorithms import ALGORITHMS, ArrayLike, YieldValue


@dataclass
class SortingVisualizer:
    root: "tk.Tk"
    width: int = 960
    height: int = 480
    background: str = "white"
    bar_color: str = "#8c8c8c"
    highlight_color: str = "#e63946"
    sorted_color: str = "#2a9d8f"
    array: ArrayLike = field(default_factory=list)
    speed_ms: int = 25

    def __post_init__(self) -> None:
        import tkinter as tk

        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg=self.background)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        self.algorithm_name = "Bubble Sort"
        self.algorithm = ALGORITHMS[self.algorithm_name]
        self.generator: Generator[YieldValue, None, None] | None = None

    # Array management -------------------------------------------------
    def generate_array(self, size: int, min_val: int = 10, max_val: int = 400) -> None:
        if size <= 0:
            self.array = []
        else:
            self.array = random.sample(range(min_val, max_val), size)
        self.stop_animation()
        self.draw_array()

    # Drawing ----------------------------------------------------------
    def draw_array(self, highlight_indices: Sequence[int] | None = None, sorted_indices: Sequence[int] | None = None) -> None:
        highlight_set = set(highlight_indices or [])
        sorted_set = set(sorted_indices or [])

        self.canvas.delete("all")
        if not self.array:
            return

        c_width = int(self.canvas["width"])
        c_height = int(self.canvas["height"])
        bar_width = c_width / len(self.array)
        max_val = max(self.array)

        for i, value in enumerate(self.array):
            x0 = i * bar_width
            x1 = (i + 1) * bar_width
            height = (value / max_val) * (c_height - 20)
            y0 = c_height - height
            y1 = c_height

            color = self.bar_color
            if i in highlight_set:
                color = self.highlight_color
            elif i in sorted_set:
                color = self.sorted_color

            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")

    # Animation --------------------------------------------------------
    def start_sort(self) -> None:
        if not self.array:
            return
        self.stop_animation()
        self.generator = self.algorithm(self.array)
        self._animate()

    def stop_animation(self) -> None:
        self.generator = None

    def _animate(self) -> None:
        if self.generator is None:
            return
        try:
            _, indices = next(self.generator)
            self.draw_array(highlight_indices=indices)
            self.root.after(self.speed_ms, self._animate)
        except StopIteration:
            self.generator = None
            self.draw_array(sorted_indices=range(len(self.array)))

    # Algorithm selection ---------------------------------------------
    def set_algorithm(self, name: str) -> None:
        if name not in ALGORITHMS:
            raise ValueError(f"Unknown algorithm: {name}")
        self.algorithm_name = name
        self.algorithm = ALGORITHMS[name]
        self.stop_animation()


__all__ = ["SortingVisualizer", "ALGORITHMS"]
