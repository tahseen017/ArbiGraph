"""
Unified Quantitative Analysis Engine.

Orchestrates the CSE246 algorithm pipeline end-to-end for both the Web Dashboard (`app.py`)
and the Terminal CLI (`cli.py`), returning clean JSON-serializable payloads.
"""

from __future__ import annotations
from dataclasses import asdict
from typing import Any, Dict, List, Optional

from ..algorithms.bellman_ford import detect_arbitrage_bellman_ford
from ..algorithms.floyd_warshall import run_floyd_warshall
from ..algorithms.johnsons import extract_best_conversion_route, run_johnsons_algorithm
from ..algorithms.optimizations import (
    allocate_capital_fractional_knapsack,
    brute_force_triangular_arbitrage,
    find_max_tolerable_fee,
    merge_sort,
)
from .market_data import build_graph_from_snapshot, get_market_snapshot


def run_full_market_analysis(
    dataset_id: str = "fx_arbitrage_desk",
    fee_pct: float = 0.0,
    starting_capital: float = 1000.0,
    trader_budget_usd: float = 10000.0,
    route_source: Optional[str] = None,
    route_target: Optional[str] = None,
    rate_overrides: Optional[List[Dict[str, object]]] = None,
) -> Dict[str, Any]:
    """Execute Bellman-Ford, MergeSort, Binary Search, Knapsack, and Johnson's Algorithm."""
    snapshot = get_market_snapshot(dataset_id)
    graph = build_graph_from_snapshot(snapshot, fee_pct=fee_pct, rate_overrides=rate_overrides)

    currencies = list(graph.currencies)
    default_src = (
        route_source.upper()
        if route_source and route_source.upper() in graph.symbol_to_idx
        else ("BDT" if "BDT" in graph.symbol_to_idx else (currencies[0] if currencies else "USD"))
    )
    default_dst = (
        route_target.upper()
        if route_target and route_target.upper() in graph.symbol_to_idx
        else ("EUR" if "EUR" in graph.symbol_to_idx and default_src != "EUR" else (currencies[-1] if len(currencies) > 1 else default_src))
    )

    # 1. Bellman-Ford Negative Cycle Detection + Lab 3 MergeSort Ranking
    bf_res = detect_arbitrage_bellman_ford(
        graph,
        starting_capital=starting_capital,
        preferred_start=default_src if default_src in ("USD", "USDT", "BDT") else "USD",
    )
    ranked_cycles = merge_sort(bf_res.cycles, key_fn=lambda c: c.profit_pct, reverse=True)

    # 2. Lab 1 Binary Search on Break-Even Transaction Fee (computed against 0-fee base rates)
    zero_fee_graph = build_graph_from_snapshot(snapshot, fee_pct=0.0, rate_overrides=rate_overrides)
    break_even = find_max_tolerable_fee(zero_fee_graph)

    # 3. Lab 4 Fractional Knapsack Liquidity-Capped Capital Allocator
    knapsack = allocate_capital_fractional_knapsack(ranked_cycles, trader_budget_usd)

    # 4. Lab 1 Brute-Force 3-Hop Baseline Comparison
    bf3 = brute_force_triangular_arbitrage(graph)
    longer_cycles_count = sum(1 for c in ranked_cycles if len(c.steps) > 3)

    # 5. Lab 8 Johnson's All-Pairs Optimal Routing + Floyd-Warshall Cross-Check
    johnsons_res = run_johnsons_algorithm(graph)
    fw_res = run_floyd_warshall(graph)

    selected_route = None
    top_multi_hop_savings: List[Dict[str, Any]] = []

    if not johnsons_res.has_arbitrage and currencies:
        rt = extract_best_conversion_route(
            graph, johnsons_res, default_src, default_dst, amount=starting_capital
        )
        if rt is not None:
            selected_route = asdict(rt)

        # Discover all pairs where multi-hop routing beats direct 1-hop quote
        all_routes = []
        for s_sym in currencies:
            for t_sym in currencies:
                if s_sym == t_sym:
                    continue
                cand_rt = extract_best_conversion_route(
                    graph, johnsons_res, s_sym, t_sym, amount=starting_capital
                )
                if cand_rt and cand_rt.hops >= 2 and (
                    cand_rt.improvement_bps > 0.5 or cand_rt.direct_effective_rate is None
                ):
                    all_routes.append(cand_rt)

        sorted_routes = merge_sort(
            all_routes,
            key_fn=lambda r: r.improvement_bps if r.direct_effective_rate else 0.1,
            reverse=True,
        )
        top_multi_hop_savings = [asdict(r) for r in sorted_routes[:12]]

    negative_edge_count = sum(1 for e in graph.edges if e.weight < 0)

    return {
        "snapshot": {
            "dataset_id": snapshot.dataset_id,
            "title": snapshot.title,
            "description": snapshot.description,
            "is_live": snapshot.is_live,
            "fetched_at_utc": snapshot.fetched_at_utc,
            "warning": snapshot.warning,
        },
        "graph": {
            "num_vertices": graph.num_vertices,
            "num_edges": graph.num_edges,
            "negative_edges_count": negative_edge_count,
            "fee_pct": graph.fee_pct,
            "currencies": currencies,
            "edges": [asdict(e) for e in graph.edges],
        },
        "bellman_ford": {
            "has_arbitrage": bf_res.has_arbitrage,
            "cycles_count": len(ranked_cycles),
            "cycles": [asdict(c) for c in ranked_cycles],
            "passes_executed": bf_res.passes_executed,
            "max_possible_passes": bf_res.max_possible_passes,
            "early_stopped": bf_res.early_stopped,
            "total_relaxations": bf_res.total_relaxations,
            "execution_time_ms": round(bf_res.execution_time_ms, 4),
            "distances": bf_res.distances,
            "pass_traces": [asdict(pt) for pt in bf_res.pass_traces],
        },
        "break_even_fee": asdict(break_even),
        "capital_allocation": asdict(knapsack),
        "brute_force_comparison": {
            "triangles_checked": bf3.triangles_checked,
            "profitable_3hop_count": len(bf3.profitable_triangles),
            "bellman_ford_total_cycles": len(ranked_cycles),
            "multi_hop_cycles_missed_by_brute_force": longer_cycles_count,
            "execution_time_ms": round(bf3.execution_time_ms, 4),
        },
        "johnsons": {
            "has_arbitrage": johnsons_res.has_arbitrage,
            "potentials": johnsons_res.potentials,
            "reweighted_edges": [asdict(re) for re in johnsons_res.reweighted_edges],
            "best_rate_matrix": [
                [round(val, 6) for val in row] for row in johnsons_res.best_rate_matrix
            ],
            "currencies": johnsons_res.currencies,
            "execution_time_ms": round(johnsons_res.execution_time_ms, 4),
            "floyd_warshall_time_ms": round(fw_res.execution_time_ms, 4),
            "route_source": default_src,
            "route_target": default_dst,
            "selected_route": selected_route,
            "top_multi_hop_savings": top_multi_hop_savings,
        },
    }
