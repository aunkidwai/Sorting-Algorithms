"""Entry point for the sorting visualizer application."""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from .algorithms import ALGORITHMS
from .visualizer import SortingVisualizer


class ControlPanel(tk.Frame):
    def __init__(self, master: tk.Misc, visualizer: SortingVisualizer):
        super().__init__(master)
        self.visualizer = visualizer
        self.pack(fill=tk.X, padx=8, pady=4)

        # Algorithm dropdown
        self.algorithm_var = tk.StringVar(value=visualizer.algorithm_name)
        algo_menu = ttk.Combobox(self, textvariable=self.algorithm_var, values=list(ALGORITHMS.keys()), state="readonly")
        algo_menu.pack(side=tk.LEFT, padx=4)
        algo_menu.bind("<<ComboboxSelected>>", self._change_algorithm)

        # Array size slider
        self.size_var = tk.IntVar(value=50)
        size_scale = tk.Scale(
            self,
            from_=10,
            to=150,
            orient=tk.HORIZONTAL,
            label="Size",
            variable=self.size_var,
            command=lambda _=None: self.visualizer.generate_array(self.size_var.get()),
        )
        size_scale.pack(side=tk.LEFT, padx=8)

        # Speed slider
        self.speed_var = tk.IntVar(value=self.visualizer.speed_ms)
        speed_scale = tk.Scale(
            self,
            from_=5,
            to=200,
            orient=tk.HORIZONTAL,
            label="Speed (ms)",
            variable=self.speed_var,
            command=lambda _=None: setattr(self.visualizer, "speed_ms", self.speed_var.get()),
        )
        speed_scale.pack(side=tk.LEFT, padx=8)

        tk.Button(self, text="Generate", command=lambda: self.visualizer.generate_array(self.size_var.get())).pack(
            side=tk.LEFT, padx=4
        )
        tk.Button(self, text="Start", command=self.visualizer.start_sort).pack(side=tk.LEFT, padx=4)

    def _change_algorithm(self, event: tk.Event | None = None) -> None:
        name = self.algorithm_var.get()
        self.visualizer.set_algorithm(name)


def main() -> None:
    root = tk.Tk()
    root.title("Sorting Algorithm Visualizer")
    visualizer = SortingVisualizer(root)
    ControlPanel(root, visualizer)
    visualizer.generate_array(50)
    root.mainloop()


if __name__ == "__main__":
    main()
