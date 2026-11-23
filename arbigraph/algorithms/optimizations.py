"""
CSE246 Syllabus Optimizations & Analytics (Labs 1, 3, and 4):

1. MergeSort (Lab 3 — Divide and Conquer, O(N log N)):
   Custom recursive MergeSort from scratch to rank discovered arbitrage cycles
   or multi-hop routes by highest net profit % without relying on built-in `sorted()`.

2. Binary Search Break-Even Fee Finder (Lab 1 — Binary Search on Monotonic Answer):
   Because arbitrage profit decreases monotonically as transaction fee `f` increases,
   we binary-search `f` in [0%, 10%] using Bellman-Ford as the feasibility check
   to pinpoint the exact maximum broker fee before all arbitrage disappears.

3. Brute-Force 3-Hop Scanner (Lab 1 — Brute Force Baseline, O(V^3)):
   Exhaustively enumerates all 3-currency triangles (i -> j -> k -> i) to benchmark
   speed and demonstrate that Bellman-Ford catches 4-hop/5-hop cycles that 3-hop
   brute force completely misses!

4. Fractional Knapsack Capital Allocator (Lab 4 — Greedy Algorithm):
   Real orderbooks have finite liquidity caps per cycle before slippage ruins the rate.
   Given trader budget `B` and multiple cycles sorted by profit density via MergeSort,
   greedily allocates capital up to each cycle's liquidity cap to maximize total profit.
"""

from __future__ import annotations
from dataclasses import dataclass
import time
from typing import Callable, List, Sequence, Tuple, TypeVar

from .bellman_ford import ArbitrageCycle, detect_arbitrage_bellman_ford
from .graph import CurrencyGraph

T = TypeVar("T")


# =============================================================================
# LAB 3: DIVIDE-AND-CONQUER MERGESORT (O(N log N))
# =============================================================================
def merge_sort(items: Sequence[T], key_fn: Callable[[T], float], reverse: bool = True) -> List[T]:
    """
    Pure divide-and-conquer MergeSort implemented from scratch.
    Defaults to descending order (`reverse=True`) to rank highest-profit cycles first.
    """
    arr = list(items)
    n = len(arr)
    if n <= 1:
        return arr

    mid = n // 2
    left_sorted = merge_sort(arr[:mid], key_fn=key_fn, reverse=reverse)
    right_sorted = merge_sort(arr[mid:], key_fn=key_fn, reverse=reverse)
    return _merge(left_sorted, right_sorted, key_fn=key_fn, reverse=reverse)


def _merge(
    left: List[T],
    right: List[T],
    key_fn: Callable[[T], float],
    reverse: bool,
) -> List[T]:
    merged: List[T] = []
    i, j = 0, 0
    len_l, len_r = len(left), len(right)

    while i < len_l and j < len_r:
        k_left = key_fn(left[i])
        k_right = key_fn(right[j])
        take_left = (k_left >= k_right) if reverse else (k_left <= k_right)
        if take_left:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    while i < len_l:
        merged.append(left[i])
        i += 1
    while j < len_r:
        merged.append(right[j])
        j += 1

    return merged


# =============================================================================
# LAB 1: BINARY SEARCH ON ANSWER — BREAK-EVEN TRANSACTION FEE
# =============================================================================
@dataclass
class BisectionStep:
    iteration: int
    low_pct: float
    high_pct: float
    mid_pct: float
    arbitrage_survives: bool
    surviving_best_profit_pct: float


@dataclass
class BreakEvenFeeResult:
    arbitrage_at_zero_fee: bool
    max_tolerable_fee_pct: float
    iterations: int
    execution_time_ms: float
    trace: List[BisectionStep]


def find_max_tolerable_fee(
    base_graph: CurrencyGraph,
    max_search_fee_pct: float = 10.0,
    tolerance_pct: float = 1e-4,
    max_iterations: int = 24,
) -> BreakEvenFeeResult:
    """
    Binary search the transaction fee f in [0%, max_search_fee_pct%] to find the exact
    threshold where the last negative-weight cycle vanishes.

    Predicate monotonicity:
        If arbitrage exists at fee f2, it MUST exist for all f1 < f2 because
        every edge weight w(f) = -ln(rate * (1 - f)) increases strictly with f.
    """
    t0 = time.perf_counter()
    zero_graph = base_graph.clone_with_fee(0.0)
    zero_res = detect_arbitrage_bellman_ford(zero_graph, discover_secondary_cycles=False)

    if not zero_res.has_arbitrage:
        return BreakEvenFeeResult(
            arbitrage_at_zero_fee=False,
            max_tolerable_fee_pct=0.0,
            iterations=1,
            execution_time_ms=(time.perf_counter() - t0) * 1000.0,
            trace=[],
        )

    low = 0.0
    high = max_search_fee_pct
    trace: List[BisectionStep] = []

    for it in range(1, max_iterations + 1):
        mid = (low + high) / 2.0
        test_graph = base_graph.clone_with_fee(mid)
        bf = detect_arbitrage_bellman_ford(test_graph, discover_secondary_cycles=False)

        best_profit = 0.0
        if bf.cycles:
            ranked = merge_sort(bf.cycles, key_fn=lambda c: c.profit_pct, reverse=True)
            best_profit = ranked[0].profit_pct

        trace.append(
            BisectionStep(
                iteration=it,
                low_pct=round(low, 6),
                high_pct=round(high, 6),
                mid_pct=round(mid, 6),
                arbitrage_survives=bf.has_arbitrage,
                surviving_best_profit_pct=round(best_profit, 5),
            )
        )

        if bf.has_arbitrage:
            low = mid
        else:
            high = mid

        if (high - low) <= tolerance_pct:
            break

    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    return BreakEvenFeeResult(
        arbitrage_at_zero_fee=True,
        max_tolerable_fee_pct=round(low, 4),
        iterations=len(trace),
        execution_time_ms=elapsed_ms,
        trace=trace,
    )


# =============================================================================
# LAB 4: GREEDY FRACTIONAL KNAPSACK — LIQUIDITY-CAPPED CAPITAL ALLOCATION
# =============================================================================
@dataclass
class CycleAllocation:
    cycle_path: List[str]
    profit_pct: float
    liquidity_cap_usd: float
    allocated_usd: float
    fraction_of_cap_used: float
    expected_profit_usd: float


@dataclass
class CapitalAllocationResult:
    total_budget_usd: float
    deployed_capital_usd: float
    unallocated_cash_usd: float
    total_expected_profit_usd: float
    blended_roi_pct: float
    allocations: List[CycleAllocation]


def allocate_capital_fractional_knapsack(
    cycles: Sequence[ArbitrageCycle],
    total_budget_usd: float,
) -> CapitalAllocationResult:
    """
    Lab 4 Fractional Knapsack Greedy Optimizer:
        - Each arbitrage cycle i is an 'item' with:
            * Capacity / weight limit = W_i (orderbook bottleneck liquidity cap in USD)
            * Value / profit at full cap = V_i = W_i * (profit_pct_i / 100)
            * Value-to-weight density    = V_i / W_i = profit_pct_i / 100
        - Step 1: Sort cycles in descending order of profit density using our Lab 3 MergeSort.
        - Step 2: Greedily fund whole or fractional liquidity caps until `total_budget_usd` is exhausted.
    """
    ranked_cycles = merge_sort(cycles, key_fn=lambda c: c.profit_pct, reverse=True)
    remaining = max(0.0, total_budget_usd)
    allocations: List[CycleAllocation] = []
    total_profit = 0.0

    for cyc in ranked_cycles:
        if remaining <= 1e-9:
            break
        cap = max(1.0, cyc.bottleneck_volume_usd)
        take = min(remaining, cap)
        fraction = take / cap
        profit = take * (cyc.profit_pct / 100.0)

        allocations.append(
            CycleAllocation(
                cycle_path=cyc.path,
                profit_pct=round(cyc.profit_pct, 4),
                liquidity_cap_usd=round(cap, 2),
                allocated_usd=round(take, 2),
                fraction_of_cap_used=round(fraction, 4),
                expected_profit_usd=round(profit, 2),
            )
        )
        remaining -= take
        total_profit += profit

    deployed = total_budget_usd - remaining
    blended_roi = (total_profit / total_budget_usd * 100.0) if total_budget_usd > 0 else 0.0

    return CapitalAllocationResult(
        total_budget_usd=round(total_budget_usd, 2),
        deployed_capital_usd=round(deployed, 2),
        unallocated_cash_usd=round(remaining, 2),
        total_expected_profit_usd=round(total_profit, 2),
        blended_roi_pct=round(blended_roi, 4),
        allocations=allocations,
    )


# =============================================================================
# LAB 1: BRUTE-FORCE 3-HOP BASELINE (O(V^3)) FOR BENCHMARKING
# =============================================================================
@dataclass
class BruteForceResult:
    triangles_checked: int
    profitable_triangles: List[Tuple[List[str], float]]
    execution_time_ms: float


def brute_force_triangular_arbitrage(graph: CurrencyGraph) -> BruteForceResult:
    """
    Naive O(V^3) triple-nested loop checking ONLY 3-currency loops (i -> j -> k -> i).
    Used to demonstrate why Bellman-Ford is superior:
        1. Brute force misses 4-hop and 5-hop arbitrage loops completely.
        2. Enumerating k-hop loops by brute force explodes as O(V^k)!
    """
    t0 = time.perf_counter()
    n = graph.num_vertices
    checked = 0
    seen = set()
    found: List[Tuple[List[str], float]] = []

    for i in range(n):
        for j in range(n):
            if j == i:
                continue
            e_ij = graph.get_edge(i, j)
            if e_ij is None:
                continue
            for k in range(n):
                if k == i or k == j:
                    continue
                checked += 1
                e_jk = graph.get_edge(j, k)
                e_ki = graph.get_edge(k, i)
                if e_jk is None or e_ki is None:
                    continue
                prod = e_ij.effective_rate * e_jk.effective_rate * e_ki.effective_rate
                if prod > 1.0 + 1e-6:
                    syms = [graph.currencies[i], graph.currencies[j], graph.currencies[k]]
                    min_s = min(syms)
                    r_idx = syms.index(min_s)
                    canon = tuple(syms[r_idx:] + syms[:r_idx])
                    if canon not in seen:
                        seen.add(canon)
                        found.append((list(canon) + [canon[0]], (prod - 1.0) * 100.0))

    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    ranked = merge_sort(found, key_fn=lambda x: x[1], reverse=True)
    return BruteForceResult(
        triangles_checked=checked,
        profitable_triangles=ranked,
        execution_time_ms=elapsed_ms,
    )
