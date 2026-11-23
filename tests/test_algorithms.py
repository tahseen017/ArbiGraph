"""
Unit Test Suite for ArbiGraph Core CSE246 Algorithms.

Run with:
    python3 -m unittest discover -s tests -v
"""

from __future__ import annotations
import math
import unittest

from arbigraph.algorithms.bellman_ford import detect_arbitrage_bellman_ford
from arbigraph.algorithms.floyd_warshall import run_floyd_warshall
from arbigraph.algorithms.graph import CurrencyGraph
from arbigraph.algorithms.johnsons import extract_best_conversion_route, run_johnsons_algorithm
from arbigraph.algorithms.min_heap import MinHeap
from arbigraph.algorithms.optimizations import (
    allocate_capital_fractional_knapsack,
    brute_force_triangular_arbitrage,
    find_max_tolerable_fee,
    merge_sort,
)


class TestArbiGraphAlgorithms(unittest.TestCase):
    def test_min_heap_ordering(self) -> None:
        heap: MinHeap[str] = MinHeap()
        samples = [(4.2, "EUR"), (0.1, "USD"), (-2.5, "BDT"), (1.8, "GBP"), (0.1, "CHF")]
        for prio, sym in samples:
            heap.push(prio, sym)

        popped = [heap.pop()[0] for _ in range(len(samples))]
        self.assertEqual(popped, sorted(p for p, _ in samples))
        self.assertTrue(heap.is_empty())

    def test_merge_sort_descending_and_ascending(self) -> None:
        nums = [3.5, -1.2, 9.8, 0.0, 3.5, 4.1]
        desc = merge_sort(nums, key_fn=lambda x: x, reverse=True)
        asc = merge_sort(nums, key_fn=lambda x: x, reverse=False)
        self.assertEqual(desc, sorted(nums, reverse=True))
        self.assertEqual(asc, sorted(nums))

    def test_bellman_ford_detects_exact_arbitrage_loop(self) -> None:
        g = CurrencyGraph(fee_pct=0.0)
        # 0.92 * 0.88 * 1.26 = 1.020096 (+2.0096% profit)
        g.add_exchange_rate("USD", "EUR", 0.92, max_volume_usd=4000)
        g.add_exchange_rate("EUR", "GBP", 0.88, max_volume_usd=3000)
        g.add_exchange_rate("GBP", "USD", 1.26, max_volume_usd=5000)

        res = detect_arbitrage_bellman_ford(g, starting_capital=1000.0)
        self.assertTrue(res.has_arbitrage)
        self.assertEqual(len(res.cycles), 1)
        cyc = res.cycles[0]
        self.assertEqual(cyc.path, ["USD", "EUR", "GBP", "USD"])
        self.assertAlmostEqual(cyc.profit_pct, 2.0096, places=4)
        self.assertAlmostEqual(cyc.ending_capital, 1020.096, places=3)
        self.assertEqual(cyc.bottleneck_volume_usd, 3000.0)

    def test_bellman_ford_catches_4hop_missed_by_3hop_brute_force(self) -> None:
        g = CurrencyGraph(fee_pct=0.0)
        # Pure 4-hop cycle A -> B -> C -> D -> A with product > 1
        g.add_exchange_rate("USD", "CAD", 1.38)
        g.add_exchange_rate("CAD", "SGD", 0.98)
        g.add_exchange_rate("SGD", "JPY", 112.0)
        g.add_exchange_rate("JPY", "USD", 0.0067)  # 1.38 * 0.98 * 112 * 0.0067 = 1.01484

        bf = detect_arbitrage_bellman_ford(g)
        bf3 = brute_force_triangular_arbitrage(g)
        self.assertTrue(bf.has_arbitrage)
        self.assertEqual(len(bf3.profitable_triangles), 0)

    def test_johnsons_matches_floyd_warshall_with_negative_edges(self) -> None:
        # Calm market with large rates (> 1 => negative log-weights!)
        g = CurrencyGraph(fee_pct=0.0)
        g.add_exchange_rate("BDT", "USD", 0.00831)
        g.add_exchange_rate("USD", "BDT", 119.75)   # w = -ln(119.75) = -4.7854 < 0!
        g.add_exchange_rate("USD", "SGD", 1.3385)   # w < 0!
        g.add_exchange_rate("SGD", "EUR", 0.6865)
        g.add_exchange_rate("BDT", "EUR", 0.00746)  # Expensive direct retail rate

        jn = run_johnsons_algorithm(g)
        fw = run_floyd_warshall(g)

        self.assertFalse(jn.has_arbitrage)
        self.assertFalse(fw.has_arbitrage)

        # Verify all reweighted edges are strictly >= 0
        for re in jn.reweighted_edges:
            self.assertGreaterEqual(re.reweighted_weight, 0.0)

        # Verify Johnson's and Floyd-Warshall produce identical shortest log-distances
        n = g.num_vertices
        for i in range(n):
            for j in range(n):
                if math.isfinite(jn.log_dist_matrix[i][j]):
                    self.assertAlmostEqual(
                        jn.log_dist_matrix[i][j], fw.log_dist_matrix[i][j], places=9
                    )

        # Verify multi-hop BDT -> USD -> SGD -> EUR beats direct BDT -> EUR
        route = extract_best_conversion_route(g, jn, "BDT", "EUR", amount=100000.0)
        self.assertIsNotNone(route)
        assert route is not None
        self.assertEqual(route.path, ["BDT", "USD", "SGD", "EUR"])
        self.assertGreater(route.amount_out, route.direct_amount_out or 0.0)

    def test_binary_search_break_even_fee_and_knapsack(self) -> None:
        g = CurrencyGraph(fee_pct=0.0)
        # Product = 1.030301 -> per-leg break-even fee: 1 - (1/1.030301)^(1/3) ~ 0.9901%
        g.add_exchange_rate("USD", "EUR", 1.01, max_volume_usd=3000)
        g.add_exchange_rate("EUR", "GBP", 1.01, max_volume_usd=3000)
        g.add_exchange_rate("GBP", "USD", 1.01, max_volume_usd=3000)

        be = find_max_tolerable_fee(g)
        self.assertTrue(be.arbitrage_at_zero_fee)
        expected_fee_pct = (1.0 - (1.0 / 1.01)) * 100.0  # 0.990099%
        self.assertAlmostEqual(be.max_tolerable_fee_pct, expected_fee_pct, places=2)

        bf = detect_arbitrage_bellman_ford(g)
        alloc = allocate_capital_fractional_knapsack(bf.cycles, total_budget_usd=5000.0)
        self.assertEqual(alloc.deployed_capital_usd, 3000.0)
        self.assertEqual(alloc.unallocated_cash_usd, 2000.0)


if __name__ == "__main__":
    unittest.main()
