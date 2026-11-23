"""
Lab 8: Johnson's All-Pairs Shortest Path Algorithm for Currency Conversion Routing.

Why Johnson's Algorithm Is Ideal for Currency Markets:
    1. Even in calm markets with ZERO arbitrage, ~50% of edges have negative weights
       because w(u, v) = -ln(rate) < 0 whenever rate > 1.0 (e.g. 1 USD = 120 BDT).
       Thus plain Dijkstra cannot be applied directly.
    2. Johnson's Algorithm unifies both regimes seamlessly:
       - PHASE 1 (Bellman-Ford from Virtual Node q):
         Adds virtual vertex q with 0-weight edges q -> v for all currencies v.
         Runs Bellman-Ford from q:
           * If a negative cycle exists -> Market has ARBITRAGE! Halts & flags cycle.
           * Otherwise -> Computes vertex potential h(v) = shortest_path(q -> v).
       - PHASE 2 (Potential Reweighting):
         By the triangle inequality, h(v) <= h(u) + w(u, v), so:
             w_hat(u, v) = w(u, v) + h(u) - h(v) >= 0  for EVERY edge!
         Crucially, for any path P = (v_0 -> v_1 -> ... -> v_k), intermediate potentials
         telescope and cancel out:
             sum(w_hat(P)) = sum(w(P)) + h(v_0) - h(v_k)
         Hence shortest paths under w_hat are IDENTICAL to shortest paths under w!
       - PHASE 3 (V x Dijkstra with Custom MinHeap):
         Runs fast O((V + E) log V) Dijkstra from each currency u, then recovers true
         log-distance d(u, v) = d_hat(u, v) - h(u) + h(v) and optimal exchange rate:
             BestRate(u -> v) = exp(-d(u, v)).

Time Complexity:  O(V^2 log V + V * E)  -- faster than Floyd-Warshall O(V^3) on sparse graphs!
Space Complexity: O(V^2) for the all-pairs optimal routing matrix.
"""

from __future__ import annotations
from dataclasses import dataclass
import math
import time
from typing import Dict, List, Optional

from .bellman_ford import TradeStep, detect_arbitrage_bellman_ford
from .dijkstra import ReweightedEdge, dijkstra_single_source
from .graph import CurrencyGraph

EPS = 1e-9


@dataclass
class ReweightedEdgeInfo:
    """Telemetry showing how Johnson's potential transform eliminates negative weights."""
    source: str
    target: str
    raw_rate: float
    original_weight: float
    h_u: float
    h_v: float
    reweighted_weight: float


@dataclass
class ConversionRoute:
    """Optimal multi-hop conversion route between two currencies."""
    source: str
    target: str
    path: List[str]
    hops: int
    best_effective_rate: float
    direct_effective_rate: Optional[float]
    improvement_bps: float          # Basis points gain vs direct conversion (1% = 100 bps)
    amount_in: float
    amount_out: float
    direct_amount_out: Optional[float]
    steps: List[TradeStep]


@dataclass
class JohnsonsResult:
    """Complete output of Johnson's Algorithm across all currency pairs."""
    has_arbitrage: bool
    potentials: Dict[str, float]                # Phase 1: h(v) per currency
    reweighted_edges: List[ReweightedEdgeInfo]  # Phase 2: w_hat(u,v) >= 0 proof table
    best_rate_matrix: List[List[float]]         # Phase 3: V x V optimal exchange rates
    log_dist_matrix: List[List[float]]          # V x V true log-distances d(u, v)
    parent_matrix: List[List[int]]              # V x V predecessor pointers
    currencies: List[str]
    execution_time_ms: float


def run_johnsons_algorithm(graph: CurrencyGraph) -> JohnsonsResult:
    """
    Execute all 3 phases of Johnson's Algorithm from scratch.
    If the graph contains a negative cycle (arbitrage), `has_arbitrage=True` is returned
    immediately after Phase 1.
    """
    t0 = time.perf_counter()
    n = graph.num_vertices
    if n == 0:
        return JohnsonsResult(
            has_arbitrage=False,
            potentials={},
            reweighted_edges=[],
            best_rate_matrix=[],
            log_dist_matrix=[],
            parent_matrix=[],
            currencies=[],
            execution_time_ms=0.0,
        )

    # -------------------------------------------------------------------------
    # PHASE 1: Virtual Node q + Bellman-Ford to compute potentials h(v)
    # Setting h[v] = 0.0 initially for all v in [0..n-1] is identical to
    # relaxing all 0-weight edges (q -> v) in round 1 from virtual node q!
    # -------------------------------------------------------------------------
    h = [0.0] * n
    early_ok = False
    for _ in range(n - 1):
        updated = False
        for edge in graph.edges:
            if h[edge.u] + edge.weight < h[edge.v] - EPS:
                h[edge.v] = h[edge.u] + edge.weight
                updated = True
        if not updated:
            early_ok = True
            break

    # Check V-th pass for negative-weight cycles
    if not early_ok:
        for edge in graph.edges:
            if h[edge.u] + edge.weight < h[edge.v] - EPS:
                # Confirm genuine arbitrage (not sub-epsilon float drift)
                bf_check = detect_arbitrage_bellman_ford(graph, discover_secondary_cycles=False)
                if bf_check.has_arbitrage:
                    elapsed_ms = (time.perf_counter() - t0) * 1000.0
                    return JohnsonsResult(
                        has_arbitrage=True,
                        potentials={graph.currencies[i]: round(h[i], 6) for i in range(n)},
                        reweighted_edges=[],
                        best_rate_matrix=[],
                        log_dist_matrix=[],
                        parent_matrix=[],
                        currencies=list(graph.currencies),
                        execution_time_ms=elapsed_ms,
                    )

    # -------------------------------------------------------------------------
    # PHASE 2: Reweight all edges using w_hat(u, v) = w(u, v) + h(u) - h(v) >= 0
    # -------------------------------------------------------------------------
    reweighted_adj: List[List[ReweightedEdge]] = [[] for _ in range(n)]
    reweighted_info: List[ReweightedEdgeInfo] = []

    for edge in graph.edges:
        w_hat = edge.weight + h[edge.u] - h[edge.v]
        # Clamp tiny floating-point rounding noise like -1e-16 to 0.0
        if w_hat < 0.0:
            w_hat = 0.0

        reweighted_adj[edge.u].append(
            ReweightedEdge(
                u=edge.u,
                v=edge.v,
                original_weight=edge.weight,
                reweighted_weight=w_hat,
            )
        )
        reweighted_info.append(
            ReweightedEdgeInfo(
                source=edge.source,
                target=edge.target,
                raw_rate=edge.raw_rate,
                original_weight=round(edge.weight, 6),
                h_u=round(h[edge.u], 6),
                h_v=round(h[edge.v], 6),
                reweighted_weight=round(w_hat, 6),
            )
        )

    # -------------------------------------------------------------------------
    # PHASE 3: Run Dijkstra from every vertex u in V and invert potential shift
    # -------------------------------------------------------------------------
    log_dist_matrix: List[List[float]] = [[math.inf] * n for _ in range(n)]
    best_rate_matrix: List[List[float]] = [[0.0] * n for _ in range(n)]
    parent_matrix: List[List[int]] = [[-1] * n for _ in range(n)]

    for u in range(n):
        dist_hat, parent = dijkstra_single_source(n, reweighted_adj, u)
        parent_matrix[u] = parent
        for v in range(n):
            if u == v:
                log_dist_matrix[u][v] = 0.0
                best_rate_matrix[u][v] = 1.0
            elif math.isfinite(dist_hat[v]):
                true_d = dist_hat[v] - h[u] + h[v]
                log_dist_matrix[u][v] = true_d
                best_rate_matrix[u][v] = math.exp(-true_d)

    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    potentials_map = {graph.currencies[i]: round(h[i], 6) for i in range(n)}

    return JohnsonsResult(
        has_arbitrage=False,
        potentials=potentials_map,
        reweighted_edges=reweighted_info,
        best_rate_matrix=best_rate_matrix,
        log_dist_matrix=log_dist_matrix,
        parent_matrix=parent_matrix,
        currencies=list(graph.currencies),
        execution_time_ms=elapsed_ms,
    )


def extract_best_conversion_route(
    graph: CurrencyGraph,
    johnsons: JohnsonsResult,
    source_currency: str,
    target_currency: str,
    amount: float = 1000.0,
) -> Optional[ConversionRoute]:
    """
    Reconstruct the optimal multi-hop conversion route source -> ... -> target
    from Johnson's parent matrix and compare against the direct 1-hop quote.
    """
    if johnsons.has_arbitrage or not johnsons.currencies:
        return None

    u = graph.symbol_to_idx.get(source_currency.upper())
    v = graph.symbol_to_idx.get(target_currency.upper())
    if u is None or v is None:
        return None

    if u == v:
        return ConversionRoute(
            source=graph.currencies[u],
            target=graph.currencies[v],
            path=[graph.currencies[u]],
            hops=0,
            best_effective_rate=1.0,
            direct_effective_rate=1.0,
            improvement_bps=0.0,
            amount_in=amount,
            amount_out=amount,
            direct_amount_out=amount,
            steps=[],
        )

    if not math.isfinite(johnsons.log_dist_matrix[u][v]):
        return None

    # Reconstruct path from parent_matrix[u]
    idx_path: List[int] = []
    curr = v
    visited = set()
    while curr != -1 and curr != u:
        if curr in visited:
            return None
        visited.add(curr)
        idx_path.append(curr)
        curr = johnsons.parent_matrix[u][curr]

    if curr != u:
        return None
    idx_path.append(u)
    idx_path.reverse()

    steps: List[TradeStep] = []
    running_amt = amount
    for i in range(len(idx_path) - 1):
        a, b = idx_path[i], idx_path[i + 1]
        edge = graph.get_edge(a, b)
        if edge is None:
            return None
        out_amt = running_amt * edge.effective_rate
        steps.append(
            TradeStep(
                step_num=i + 1,
                from_currency=edge.source,
                to_currency=edge.target,
                raw_rate=edge.raw_rate,
                effective_rate=edge.effective_rate,
                weight=edge.weight,
                amount_in=running_amt,
                amount_out=out_amt,
                venue=edge.venue,
                max_volume_usd=edge.max_volume_usd,
            )
        )
        running_amt = out_amt

    best_rate = johnsons.best_rate_matrix[u][v]
    direct_edge = graph.get_edge(u, v)
    direct_rate = direct_edge.effective_rate if direct_edge else None
    direct_out = amount * direct_rate if direct_rate is not None else None

    improvement_bps = 0.0
    if direct_rate and direct_rate > 0:
        improvement_bps = ((best_rate - direct_rate) / direct_rate) * 10000.0

    return ConversionRoute(
        source=graph.currencies[u],
        target=graph.currencies[v],
        path=[graph.currencies[i] for i in idx_path],
        hops=len(steps),
        best_effective_rate=best_rate,
        direct_effective_rate=direct_rate,
        improvement_bps=max(0.0, improvement_bps),
        amount_in=amount,
        amount_out=running_amt,
        direct_amount_out=direct_out,
        steps=steps,
    )
