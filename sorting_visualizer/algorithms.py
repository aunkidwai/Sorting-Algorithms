"""Generator-based sorting algorithm implementations."""
from __future__ import annotations

from typing import Generator, List, Tuple

ArrayLike = List[int]
YieldValue = Tuple[ArrayLike, Tuple[int, ...]]


def _yield_state(arr: ArrayLike, *indices: int) -> YieldValue:
    return arr, tuple(indices)


def bubble_sort(arr: ArrayLike) -> Generator[YieldValue, None, None]:
    n = len(arr)
    for i in range(n):
        for j in range(0, n - 1 - i):
            yield _yield_state(arr, j, j + 1)
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                yield _yield_state(arr, j, j + 1)
    yield _yield_state(arr)


def insertion_sort(arr: ArrayLike) -> Generator[YieldValue, None, None]:
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            yield _yield_state(arr, j, j + 1)
            arr[j + 1] = arr[j]
            yield _yield_state(arr, j, j + 1)
            j -= 1
        arr[j + 1] = key
        yield _yield_state(arr, j + 1)
    yield _yield_state(arr)


def selection_sort(arr: ArrayLike) -> Generator[YieldValue, None, None]:
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            yield _yield_state(arr, min_idx, j)
            if arr[j] < arr[min_idx]:
                min_idx = j
                yield _yield_state(arr, min_idx)
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            yield _yield_state(arr, i, min_idx)
    yield _yield_state(arr)


def merge_sort(arr: ArrayLike) -> Generator[YieldValue, None, None]:
    yield from _merge_sort_recursive(arr, 0, len(arr) - 1)
    yield _yield_state(arr)


def _merge_sort_recursive(arr: ArrayLike, left: int, right: int) -> Generator[YieldValue, None, None]:
    if left >= right:
        return
    mid = (left + right) // 2
    yield from _merge_sort_recursive(arr, left, mid)
    yield from _merge_sort_recursive(arr, mid + 1, right)
    yield from _merge(arr, left, mid, right)


def _merge(arr: ArrayLike, left: int, mid: int, right: int) -> Generator[YieldValue, None, None]:
    left_copy = arr[left : mid + 1]
    right_copy = arr[mid + 1 : right + 1]
    i = j = 0
    k = left

    while i < len(left_copy) and j < len(right_copy):
        yield _yield_state(arr, k)
        if left_copy[i] <= right_copy[j]:
            arr[k] = left_copy[i]
            i += 1
        else:
            arr[k] = right_copy[j]
            j += 1
        k += 1
        yield _yield_state(arr, k - 1)

    while i < len(left_copy):
        arr[k] = left_copy[i]
        i += 1
        k += 1
        yield _yield_state(arr, k - 1)

    while j < len(right_copy):
        arr[k] = right_copy[j]
        j += 1
        k += 1
        yield _yield_state(arr, k - 1)


def quick_sort(arr: ArrayLike) -> Generator[YieldValue, None, None]:
    yield from _quick_sort_recursive(arr, 0, len(arr) - 1)
    yield _yield_state(arr)


def _quick_sort_recursive(arr: ArrayLike, low: int, high: int) -> Generator[YieldValue, None, None]:
    if low >= high:
        return
    pivot_idx = yield from _partition(arr, low, high)
    yield from _quick_sort_recursive(arr, low, pivot_idx - 1)
    yield from _quick_sort_recursive(arr, pivot_idx + 1, high)


def _partition(arr: ArrayLike, low: int, high: int) -> Generator[int, None, None]:
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        yield _yield_state(arr, j, high)
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
            yield _yield_state(arr, i, j)
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    yield _yield_state(arr, i + 1, high)
    return i + 1


def heap_sort(arr: ArrayLike) -> Generator[YieldValue, None, None]:
    n = len(arr)

    for i in range(n // 2 - 1, -1, -1):
        yield from _heapify(arr, n, i)

    for end in range(n - 1, 0, -1):
        arr[0], arr[end] = arr[end], arr[0]
        yield _yield_state(arr, 0, end)
        yield from _heapify(arr, end, 0)

    yield _yield_state(arr)


def _heapify(arr: ArrayLike, heap_size: int, root: int) -> Generator[YieldValue, None, None]:
    largest = root
    left = 2 * root + 1
    right = 2 * root + 2

    if left < heap_size:
        yield _yield_state(arr, root, left)
        if arr[left] > arr[largest]:
            largest = left

    if right < heap_size:
        yield _yield_state(arr, root, right)
        if arr[right] > arr[largest]:
            largest = right

    if largest != root:
        arr[root], arr[largest] = arr[largest], arr[root]
        yield _yield_state(arr, root, largest)
        yield from _heapify(arr, heap_size, largest)


def shell_sort(arr: ArrayLike) -> Generator[YieldValue, None, None]:
    n = len(arr)
    gap = n // 2

    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                yield _yield_state(arr, j, j - gap)
                arr[j] = arr[j - gap]
                yield _yield_state(arr, j, j - gap)
                j -= gap
            arr[j] = temp
            yield _yield_state(arr, j)
        gap //= 2

    yield _yield_state(arr)


def counting_sort(arr: ArrayLike) -> Generator[YieldValue, None, None]:
    if not arr:
        yield _yield_state(arr)
        return

    min_val = min(arr)
    max_val = max(arr)
    range_size = max_val - min_val + 1
    count = [0] * range_size

    for value in arr:
        count[value - min_val] += 1
        yield _yield_state(arr)

    for i in range(1, range_size):
        count[i] += count[i - 1]

    output = [0] * len(arr)
    for value in reversed(arr):
        count[value - min_val] -= 1
        new_index = count[value - min_val]
        output[new_index] = value
        yield _yield_state(arr, new_index)

    for i, value in enumerate(output):
        arr[i] = value
        yield _yield_state(arr, i)

    yield _yield_state(arr)


def radix_sort(arr: ArrayLike) -> Generator[YieldValue, None, None]:
    if not arr:
        yield _yield_state(arr)
        return

    if min(arr) < 0:
        raise ValueError("Radix sort requires non-negative integers")

    max_val = max(arr)
    exp = 1
    while max_val // exp > 0:
        yield from _counting_sort_by_digit(arr, exp)
        exp *= 10

    yield _yield_state(arr)


def _counting_sort_by_digit(arr: ArrayLike, exp: int) -> Generator[YieldValue, None, None]:
    n = len(arr)
    output = [0] * n
    count = [0] * 10

    for value in arr:
        index = (value // exp) % 10
        count[index] += 1
        yield _yield_state(arr)

    for i in range(1, 10):
        count[i] += count[i - 1]

    for i in range(n - 1, -1, -1):
        index = (arr[i] // exp) % 10
        count[index] -= 1
        new_index = count[index]
        output[new_index] = arr[i]
        yield _yield_state(arr, i)

    for i in range(n):
        arr[i] = output[i]
        yield _yield_state(arr, i)

ALGORITHMS = {
    "Bubble Sort": bubble_sort,
    "Insertion Sort": insertion_sort,
    "Selection Sort": selection_sort,
    "Merge Sort": merge_sort,
    "Quick Sort": quick_sort,
    "Heap Sort": heap_sort,
    "Shell Sort": shell_sort,
    "Counting Sort": counting_sort,
    "Radix Sort": radix_sort,
}

