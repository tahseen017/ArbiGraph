"""
Empirical Complexity Benchmark Suite.

Compares empirical execution times of:
    1. Johnson's Algorithm   O(V^2 log V + V * E)
    2. Floyd-Warshall        O(V^3)
    3. Bellman-Ford          O(V * E) with Early-Exit vs Worst-Case

on sparse hub-and-spoke FX/Crypto graphs where E ~ 5 * V (realistic market topology
since minor currencies quote against major hubs like USD, EUR, USDT, BTC rather than
every exotic currency quoting against every other exotic currency).
"""

from __future__ import annotations
from dataclasses import dataclass
import math
import random
from typing import List

from .bellman_ford import detect_arbitrage_bellman_ford
from .floyd_warshall import run_floyd_warshall
from .graph import CurrencyGraph
from .johnsons import run_johnsons_algorithm


@dataclass
class ScalingPoint:
    vertices: int
    edges: int
    bellman_ford_ms: float
    johnsons_ms: float
    floyd_warshall_ms: float
    speedup_factor: float
    max_matrix_diff: float


def _generate_sparse_calm_fx_graph(num_vertices: int, seed: int = 42) -> CurrencyGraph:
    """
    Generate an arbitrage-free sparse currency graph with `num_vertices` currencies.
    Assigns each currency i a true USD value P_i and adds bid-ask spread < 1.0 so
    no negative cycles exist: R_{i->j} = (P_i / P_j) * (1 - spread).
    """
    rng = random.Random(seed + num_vertices)
    g = CurrencyGraph(fee_pct=0.05)

    names = [f"C{i:02d}" for i in range(num_vertices)]
    intrinsic_val = [math.exp(rng.uniform(-4.5, 4.5)) for _ in range(num_vertices)]

    # Hub currencies (first 3) connect to all; regional currencies connect to 2 random peers
    hubs = min(3, num_vertices)
    for i in range(num_vertices):
        g.add_currency(names[i])

    for i in range(num_vertices):
        targets = set(range(hubs))
        for _ in range(2):
            targets.add(rng.randrange(num_vertices))
        targets.discard(i)

        for j in targets:
            spread_ij = rng.uniform(0.001, 0.008)
            spread_ji = rng.uniform(0.001, 0.008)
            rate_ij = (intrinsic_val[i] / intrinsic_val[j]) * (1.0 - spread_ij)
            rate_ji = (intrinsic_val[j] / intrinsic_val[i]) * (1.0 - spread_ji)
            g.add_exchange_rate(names[i], names[j], rate_ij, venue="Bench")
            g.add_exchange_rate(names[j], names[i], rate_ji, venue="Bench")

    return g


def run_scaling_benchmark(sizes: List[int] | None = None) -> List[ScalingPoint]:
    """Run scaling comparison across increasing vertex counts V (up to 160 world currencies)."""
    if sizes is None:
        sizes = [15, 35, 70, 110, 160]

    results: List[ScalingPoint] = []
    for v_count in sizes:
        g = _generate_sparse_calm_fx_graph(v_count)

        bf_res = detect_arbitrage_bellman_ford(g, discover_secondary_cycles=False)
        j_res = run_johnsons_algorithm(g)
        fw_res = run_floyd_warshall(g)

        # Verify Johnson's and Floyd-Warshall compute identical shortest log-distances
        max_diff = 0.0
        if not j_res.has_arbitrage and not fw_res.has_arbitrage:
            for u in range(v_count):
                for v in range(v_count):
                    dj = j_res.log_dist_matrix[u][v]
                    df = fw_res.log_dist_matrix[u][v]
                    if math.isfinite(dj) and math.isfinite(df):
                        max_diff = max(max_diff, abs(dj - df))

        speedup = (
            fw_res.execution_time_ms / j_res.execution_time_ms
            if j_res.execution_time_ms > 1e-6
            else 1.0
        )

        results.append(
            ScalingPoint(
                vertices=v_count,
                edges=g.num_edges,
                bellman_ford_ms=round(bf_res.execution_time_ms, 3),
                johnsons_ms=round(j_res.execution_time_ms, 3),
                floyd_warshall_ms=round(fw_res.execution_time_ms, 3),
                speedup_factor=round(speedup, 2),
                max_matrix_diff=round(max_diff, 12),
            )
        )

    return results
