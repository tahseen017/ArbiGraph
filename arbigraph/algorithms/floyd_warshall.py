"""
Lab 8: Floyd-Warshall Dynamic Programming All-Pairs Shortest Path Algorithm.

Role in ArbiGraph:
    1. Cross-verifies Johnson's Algorithm all-pairs log-distances to 1e-9 precision.
    2. Detects negative cycles via diagonal check `dist[i][i] < -EPS`.
    3. Benchmarks empirical runtime scaling:
       - Floyd-Warshall: O(V^3) always (triple nested DP loop)
       - Johnson's:      O(V^2 log V + V * E), dramatically faster on sparse FX/Crypto graphs!

Time Complexity:  O(V^3)
Space Complexity: O(V^2)
"""

from __future__ import annotations
from dataclasses import dataclass
import math
import time
from typing import List

from .graph import CurrencyGraph

EPS = 1e-9


@dataclass
class FloydWarshallResult:
    has_arbitrage: bool
    log_dist_matrix: List[List[float]]
    best_rate_matrix: List[List[float]]
    next_hop: List[List[int]]
    execution_time_ms: float


def run_floyd_warshall(graph: CurrencyGraph) -> FloydWarshallResult:
    """Execute standard O(V^3) Floyd-Warshall DP on the currency graph."""
    t0 = time.perf_counter()
    n = graph.num_vertices
    dist = graph.build_adjacency_matrix()
    next_hop = [[-1] * n for _ in range(n)]

    for i in range(n):
        next_hop[i][i] = i
    for edge in graph.edges:
        next_hop[edge.u][edge.v] = edge.v

    for k in range(n):
        dist_k = dist[k]
        for i in range(n):
            dik = dist[i][k]
            if not math.isfinite(dik):
                continue
            dist_i = dist[i]
            next_i = next_hop[i]
            next_ik = next_i[k]
            for j in range(n):
                cand = dik + dist_k[j]
                if cand < dist_i[j] - EPS:
                    dist_i[j] = cand
                    next_i[j] = next_ik

    has_arbitrage = any(dist[i][i] < -EPS for i in range(n))
    best_rates = [[0.0] * n for _ in range(n)]
    if not has_arbitrage:
        for i in range(n):
            for j in range(n):
                if math.isfinite(dist[i][j]):
                    best_rates[i][j] = 1.0 if i == j else math.exp(-dist[i][j])

    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    return FloydWarshallResult(
        has_arbitrage=has_arbitrage,
        log_dist_matrix=dist,
        best_rate_matrix=best_rates,
        next_hop=next_hop,
        execution_time_ms=elapsed_ms,
    )
