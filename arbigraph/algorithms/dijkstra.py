"""
Dijkstra's Single-Source Shortest Path Algorithm (Implemented from Scratch).

Important Mathematical Note for Currency Graphs:
    Raw currency log-weights w(u, v) = -ln(rate) ARE NEGATIVE whenever rate > 1.0
    (for example, USD -> BDT = 120.0 gives w = -4.7875 < 0).
    Plain Dijkstra FAILS on graphs with negative edge weights!

    Therefore, Dijkstra is invoked exclusively inside Phase 3 of Johnson's Algorithm
    AFTER Bellman-Ford vertex potentials h(v) have reweighted every edge to:
        w_hat(u, v) = w(u, v) + h(u) - h(v) >= 0.

Time Complexity:  O((V + E) log V) using our custom Binary MinHeap
Space Complexity: O(V)
"""

from __future__ import annotations
from dataclasses import dataclass
import math
from typing import List, Tuple

from .min_heap import MinHeap

EPS = 1e-12


@dataclass(frozen=True)
class ReweightedEdge:
    """Non-negative edge used in Phase 3 of Johnson's Algorithm."""
    u: int
    v: int
    original_weight: float
    reweighted_weight: float  # Guaranteed >= 0


def dijkstra_single_source(
    num_vertices: int,
    adj: List[List[ReweightedEdge]],
    source: int,
) -> Tuple[List[float], List[int]]:
    """
    Compute shortest non-negative reweighted paths from `source` to all vertices
    using our from-scratch `MinHeap`.

    Returns:
        (dist_hat, parent) where dist_hat[v] is the reweighted shortest distance
        and parent[v] stores the predecessor on the optimal conversion path.
    """
    dist_hat = [math.inf] * num_vertices
    parent = [-1] * num_vertices
    dist_hat[source] = 0.0

    pq: MinHeap[int] = MinHeap()
    pq.push(0.0, source)

    while not pq.is_empty():
        d_u, u = pq.pop()

        # Lazy deletion check: skip stale heap entries
        if d_u > dist_hat[u] + EPS:
            continue

        for edge in adj[u]:
            cand = d_u + edge.reweighted_weight
            if cand < dist_hat[edge.v] - EPS:
                dist_hat[edge.v] = cand
                parent[edge.v] = u
                pq.push(cand, edge.v)

    return dist_hat, parent
