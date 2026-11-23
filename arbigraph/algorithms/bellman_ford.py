"""
Bellman-Ford Negative-Weight Cycle Detection & Arbitrage Reconstruction.

Core Algorithm:
    1. Multi-Source Initialization (Super-Source Equivalence):
       Initialize dist[v] = 0.0 for all v in V. Mathematically equivalent to adding a
       virtual vertex q with 0-weight directed edges (q -> v) to every currency so
       negative cycles in ANY connected component are guaranteed to be detected.
    2. Relaxation Passes (1 .. V - 1) with Early-Exit Optimization:
       Relax every edge (u, v, w). If no edge improves in an entire pass, terminate
       immediately in O(k * E) where k << V when the market is arbitrage-free.
    3. V-th Pass Negative Cycle Detection:
       Any edge still satisfying dist[u] + w < dist[v] - EPS proves a negative cycle.
    4. Exact Cycle Reconstruction (Walk Back V Steps):
       Because v may only be *reachable from* a negative cycle rather than *inside* it,
       stepping `curr = parent[curr]` V times guarantees landing strictly inside the
       cycle, after which parent pointers are traced until the loop closes and reversed.

Time Complexity:  O(V * E) worst-case; O(k * E) with Early Exit on calm markets
Space Complexity: O(V)
"""

from __future__ import annotations
from dataclasses import dataclass, field
import math
import time
from typing import Dict, List, Optional, Set, Tuple

from .graph import CurrencyGraph, Edge

EPS = 1e-9  # Floating-point tolerance to prevent false-positive "ghost" cycles


@dataclass
class TradeStep:
    """Single leg of a multi-hop currency conversion or arbitrage loop."""
    step_num: int
    from_currency: str
    to_currency: str
    raw_rate: float
    effective_rate: float
    weight: float
    amount_in: float
    amount_out: float
    venue: str
    max_volume_usd: float


@dataclass
class ArbitrageCycle:
    """Represents a verified negative-weight cycle (risk-free arbitrage loop)."""
    path: List[str]                 # e.g., ["USD", "EUR", "GBP", "USD"]
    total_log_weight: float         # Sum of -ln(effective_rate) < 0
    CycleMultiplier: float          # Product of effective_rates > 1.0
    profit_pct: float               # (multiplier - 1.0) * 100
    bottleneck_volume_usd: float    # Min liquidity cap across cycle edges
    steps: List[TradeStep]          # Simulated trade execution for starting_capital
    starting_capital: float
    ending_capital: float
    net_profit: float


@dataclass
class PassTrace:
    """Telemetry from a single Bellman-Ford relaxation pass (for UI display)."""
    pass_number: int
    relaxations_count: int
    sample_updates: List[str]


@dataclass
class BellmanFordResult:
    """Complete output of Bellman-Ford arbitrage detection."""
    has_arbitrage: bool
    cycles: List[ArbitrageCycle]
    passes_executed: int
    max_possible_passes: int
    early_stopped: bool
    total_relaxations: int
    execution_time_ms: float
    distances: Dict[str, float]
    pass_traces: List[PassTrace] = field(default_factory=list)


def _canonical_cycle_key(cycle_vertices: List[int], currencies: List[str]) -> Tuple[str, ...]:
    """
    Normalize a closed loop [v0, v1, ..., vk, v0] so rotations of the same directed cycle
    (e.g. USD->EUR->GBP->USD and EUR->GBP->USD->EUR) map to the exact same canonical tuple.
    """
    ring = [currencies[v] for v in cycle_vertices[:-1]]
    if not ring:
        return ()
    min_sym = min(ring)
    min_idx = ring.index(min_sym)
    rotated = ring[min_idx:] + ring[:min_idx]
    return tuple(rotated)


def _build_arbitrage_cycle(
    graph: CurrencyGraph,
    cycle_indices: List[int],
    starting_capital: float = 1000.0,
    preferred_start: Optional[str] = None,
) -> Optional[ArbitrageCycle]:
    """
    Validate a candidate cycle [v0, v1, ..., vk, v0] against actual graph edges,
    rotate to `preferred_start` if part of the cycle, and compute exact profit ledger.
    """
    ring = cycle_indices[:-1]
    if len(ring) < 2:
        return None

    # Rotate so preferred_start (e.g. USD) is first if present; otherwise keep cleanest ticker first
    symbols_ring = [graph.currencies[idx] for idx in ring]
    if preferred_start and preferred_start.upper() in symbols_ring:
        rot = symbols_ring.index(preferred_start.upper())
    elif "USD" in symbols_ring:
        rot = symbols_ring.index("USD")
    else:
        min_sym = min(symbols_ring)
        rot = symbols_ring.index(min_sym)

    ordered_ring = ring[rot:] + ring[:rot]
    ordered_closed = ordered_ring + [ordered_ring[0]]

    total_weight = 0.0
    multiplier = 1.0
    bottleneck_vol = math.inf
    current_amt = starting_capital
    steps: List[TradeStep] = []

    for i in range(len(ordered_ring)):
        u = ordered_closed[i]
        v = ordered_closed[i + 1]
        edge: Optional[Edge] = graph.get_edge(u, v)
        if edge is None:
            return None

        next_amt = current_amt * edge.effective_rate
        total_weight += edge.weight
        multiplier *= edge.effective_rate
        bottleneck_vol = min(bottleneck_vol, edge.max_volume_usd)

        steps.append(
            TradeStep(
                step_num=i + 1,
                from_currency=edge.source,
                to_currency=edge.target,
                raw_rate=edge.raw_rate,
                effective_rate=edge.effective_rate,
                weight=edge.weight,
                amount_in=current_amt,
                amount_out=next_amt,
                venue=edge.venue,
                max_volume_usd=edge.max_volume_usd,
            )
        )
        current_amt = next_amt

    # Strict numeric check against floating-point rounding ghosts
    if total_weight >= -EPS or multiplier <= 1.0 + 1e-6:
        return None

    profit_pct = (multiplier - 1.0) * 100.0
    return ArbitrageCycle(
        path=[graph.currencies[idx] for idx in ordered_closed],
        total_log_weight=total_weight,
        CycleMultiplier=multiplier,
        profit_pct=profit_pct,
        bottleneck_volume_usd=bottleneck_vol if math.isfinite(bottleneck_vol) else 10000.0,
        steps=steps,
        starting_capital=starting_capital,
        ending_capital=current_amt,
        net_profit=current_amt - starting_capital,
    )


def _extract_cycle_from_vertex(
    start_vertex: int,
    parent: List[int],
    num_vertices: int,
) -> Optional[List[int]]:
    """
    Walk back V steps from `start_vertex` to guarantee entry into the negative cycle,
    then trace parent pointers until a vertex repeats and reverse to forward trade order.
    """
    curr = start_vertex
    for _ in range(num_vertices):
        curr = parent[curr]
        if curr == -1:
            return None

    # Trace cycle starting at `curr`
    visited_pos: Dict[int, int] = {}
    trace: List[int] = []
    node = curr
    while node != -1 and node not in visited_pos:
        visited_pos[node] = len(trace)
        trace.append(node)
        node = parent[node]

    if node == -1:
        return None

    cycle_start = visited_pos[node]
    backward_loop = trace[cycle_start:] + [node]
    # Reverse because `parent[v] = u` points against edge direction (u -> v)
    forward_loop = list(reversed(backward_loop))
    return forward_loop


def _run_bf_subgraph(
    graph: CurrencyGraph,
    excluded_edges: Optional[Set[Tuple[int, int]]] = None,
    record_trace: bool = False,
) -> Tuple[List[float], List[int], List[int], int, bool, int, List[PassTrace]]:
    """
    Core Bellman-Ford pass engine over `graph` (optionally excluding specific edges
    to uncover secondary arbitrage loops sharing hub currencies like USD).
    """
    n = graph.num_vertices
    dist = [0.0] * n
    parent = [-1] * n
    passes_executed = 0
    early_stopped = False
    total_relaxations = 0
    traces: List[PassTrace] = []

    active_edges = (
        graph.edges
        if not excluded_edges
        else [e for e in graph.edges if (e.u, e.v) not in excluded_edges]
    )
    max_iters = n

    # V - 1 Relaxation Passes
    for p in range(1, max(1, max_iters)):
        passes_executed = p
        relax_in_pass = 0
        samples: List[str] = []

        for edge in active_edges:
            if dist[edge.u] + edge.weight < dist[edge.v] - EPS:
                dist[edge.v] = dist[edge.u] + edge.weight
                parent[edge.v] = edge.u
                relax_in_pass += 1
                total_relaxations += 1
                if record_trace and len(samples) < 4:
                    samples.append(
                        f"{edge.source}->{edge.target} (d[{edge.target}]={dist[edge.v]:.5f})"
                    )

        if record_trace:
            traces.append(
                PassTrace(
                    pass_number=p,
                    relaxations_count=relax_in_pass,
                    sample_updates=samples,
                )
            )

        # Optimization: Early exit if zero relaxations occurred
        if relax_in_pass == 0:
            early_stopped = True
            break

    # V-th Pass: Check all edges for remaining negative-weight relaxations
    relaxed_on_nth: List[int] = []
    if not early_stopped and max_iters > 0:
        passes_executed = max_iters
        nth_samples: List[str] = []
        for edge in active_edges:
            if dist[edge.u] + edge.weight < dist[edge.v] - EPS:
                dist[edge.v] = dist[edge.u] + edge.weight
                parent[edge.v] = edge.u
                relaxed_on_nth.append(edge.v)
                total_relaxations += 1
                if record_trace and len(nth_samples) < 4:
                    nth_samples.append(
                        f"CYCLE WITNESS: {edge.source}->{edge.target}"
                    )
        if record_trace:
            traces.append(
                PassTrace(
                    pass_number=max_iters,
                    relaxations_count=len(relaxed_on_nth),
                    sample_updates=nth_samples,
                )
            )

    return dist, parent, relaxed_on_nth, passes_executed, early_stopped, total_relaxations, traces


def detect_arbitrage_bellman_ford(
    graph: CurrencyGraph,
    starting_capital: float = 1000.0,
    preferred_start: Optional[str] = "USD",
    discover_secondary_cycles: bool = True,
) -> BellmanFordResult:
    """
    Run Bellman-Ford negative cycle detection on `graph`.

    Returns:
        BellmanFordResult containing all verified arbitrage cycles, relaxation pass telemetry,
        early-exit status, and execution timing in milliseconds.
    """
    t0 = time.perf_counter()
    n = graph.num_vertices
    if n == 0:
        return BellmanFordResult(
            has_arbitrage=False,
            cycles=[],
            passes_executed=0,
            max_possible_passes=0,
            early_stopped=True,
            total_relaxations=0,
            execution_time_ms=0.0,
            distances={},
            pass_traces=[],
        )

    (
        dist,
        parent,
        witnesses,
        passes_executed,
        early_stopped,
        total_relaxations,
        traces,
    ) = _run_bf_subgraph(graph, excluded_edges=None, record_trace=True)

    seen_keys: Set[Tuple[str, ...]] = set()
    discovered_cycles: List[ArbitrageCycle] = []

    for w_vertex in witnesses:
        raw_loop = _extract_cycle_from_vertex(w_vertex, parent, n)
        if raw_loop is None:
            continue
        key = _canonical_cycle_key(raw_loop, graph.currencies)
        if key and key not in seen_keys:
            arb = _build_arbitrage_cycle(graph, raw_loop, starting_capital, preferred_start)
            if arb is not None:
                seen_keys.add(key)
                discovered_cycles.append(arb)

    # Secondary discovery: temporarily peel the bottleneck edge of each discovered cycle
    # so additional independent cycles (even those sharing hub currencies like USD) surface.
    if discover_secondary_cycles and discovered_cycles:
        excluded_edges: Set[Tuple[int, int]] = set()
        rounds = 0
        while rounds < 6:
            rounds += 1
            for cyc in discovered_cycles:
                # Peel the minimum-volume (or last) edge of this cycle
                bottleneck_step = min(cyc.steps, key=lambda s: (s.max_volume_usd, s.weight))
                u_idx = graph.symbol_to_idx[bottleneck_step.from_currency]
                v_idx = graph.symbol_to_idx[bottleneck_step.to_currency]
                excluded_edges.add((u_idx, v_idx))

            _, sub_parent, sub_witnesses, _, _, _, _ = _run_bf_subgraph(
                graph, excluded_edges=excluded_edges, record_trace=False
            )
            found_new = False
            for w_v in sub_witnesses:
                raw_loop = _extract_cycle_from_vertex(w_v, sub_parent, n)
                if raw_loop is None:
                    continue
                key = _canonical_cycle_key(raw_loop, graph.currencies)
                if key and key not in seen_keys:
                    arb = _build_arbitrage_cycle(
                        graph, raw_loop, starting_capital, preferred_start
                    )
                    if arb is not None:
                        seen_keys.add(key)
                        discovered_cycles.append(arb)
                        found_new = True
            if not found_new:
                break

    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    dist_map = {graph.currencies[i]: round(dist[i], 6) for i in range(n)}

    return BellmanFordResult(
        has_arbitrage=len(discovered_cycles) > 0,
        cycles=discovered_cycles,
        passes_executed=passes_executed,
        max_possible_passes=n,
        early_stopped=early_stopped,
        total_relaxations=total_relaxations,
        execution_time_ms=elapsed_ms,
        distances=dist_map,
        pass_traces=traces,
    )
