"""
Custom Binary Min-Heap Priority Queue (Implemented from Scratch).

Used by Dijkstra's Algorithm inside Phase 3 of Johnson's Algorithm so that
zero external priority-queue libraries (like `heapq`) are needed.

Time Complexity:
    - push(): O(log N)
    - pop():  O(log N)
    - peek(): O(1)
Space Complexity: O(N)
"""

from __future__ import annotations
from typing import Generic, List, Tuple, TypeVar

T = TypeVar("T")


class MinHeap(Generic[T]):
    """A classic 0-indexed binary min-heap storing (priority, payload) pairs."""

    def __init__(self) -> None:
        self._data: List[Tuple[float, T]] = []

    def __len__(self) -> int:
        return len(self._data)

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def push(self, priority: float, item: T) -> None:
        """Insert a new (priority, item) pair in O(log N) time."""
        self._data.append((priority, item))
        self._sift_up(len(self._data) - 1)

    def pop(self) -> Tuple[float, T]:
        """Remove and return the minimum-priority pair in O(log N) time."""
        if not self._data:
            raise IndexError("pop from an empty MinHeap")

        top = self._data[0]
        last = self._data.pop()
        if self._data:
            self._data[0] = last
            self._sift_down(0)
        return top

    def _sift_up(self, idx: int) -> None:
        while idx > 0:
            parent = (idx - 1) // 2
            if self._data[idx][0] < self._data[parent][0]:
                self._data[idx], self._data[parent] = self._data[parent], self._data[idx]
                idx = parent
            else:
                break

    def _sift_down(self, idx: int) -> None:
        n = len(self._data)
        while True:
            smallest = idx
            left = 2 * idx + 1
            right = 2 * idx + 2

            if left < n and self._data[left][0] < self._data[smallest][0]:
                smallest = left
            if right < n and self._data[right][0] < self._data[smallest][0]:
                smallest = right

            if smallest != idx:
                self._data[idx], self._data[smallest] = self._data[smallest], self._data[idx]
                idx = smallest
            else:
                break
