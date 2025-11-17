# Sorting Algorithm Visualizer

This project provides a small `tkinter` application that visualizes common sorting algorithms. Each algorithm is implemented as a Python generator that yields after every interesting operation, allowing the UI to animate comparisons and swaps in real time.

## Features

- Algorithms: Bubble, Selection, Insertion, Merge, Quick, Heap, Shell, Counting, and Radix sort
- Adjustable array size and animation speed
- Random array generation with unique values

## Project layout

```
sorting_visualizer/
├── algorithms.py   # Generator-based sorting algorithms
├── visualizer.py   # Drawing engine built with tkinter
└── main.py         # UI and application entry point
```

## Usage

Create and activate a Python 3.11+ environment, install dependencies (only the standard library is required), and run:

```
python -m sorting_visualizer.main
```

Use the controls at the top of the window to choose an algorithm, adjust the array size and animation speed, generate new data, and start the visualization. Counting and radix sort both expect non-negative integers, which matches the random arrays provided by the UI.
