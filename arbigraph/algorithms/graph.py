"""
Lab 7: Directed Weighted Graph Representation for Currency Exchange Modeling.

Mathematical Transformation:
    Suppose currency u converts to currency v at rate R_{u->v} with broker fee f in [0, 1).
    Effective rate: R_eff = R_{u->v} * (1 - f)

    A cycle C_1 -> C_2 -> ... -> C_k -> C_1 yields risk-free arbitrage iff:
        R_eff(1,2) * R_eff(2,3) * ... * R_eff(k,1) > 1

    Taking natural logarithm and negating converts multiplication into addition:
        -ln(R_eff(1,2)) + -ln(R_eff(2,3)) + ... + -ln(R_eff(k,1)) < 0

    Therefore, setting edge weight w(u, v) = -ln(R_{u->v} * (1 - f)) maps:
        1. Profitable arbitrage loops  <-->  Negative-weight cycles (sum(w) < 0)
        2. Maximum conversion paths    <-->  Shortest paths (minimum sum(w))
"""

from __future__ import annotations
from dataclasses import dataclass
import math
from typing import Dict, List, Optional, Tuple


@dataclass(frozen=True)
class Edge:
    """Represents a directed currency conversion quote u -> v."""
    u: int                  # Source vertex index
    v: int                  # Target vertex index
    source: str             # Source currency code (e.g., "USD")
    target: str             # Target currency code (e.g., "EUR")
    raw_rate: float         # Quoted exchange rate before fee
    effective_rate: float   # Exchange rate after fee: raw_rate * (1 - fee)
    weight: float           # Transformed weight: -ln(effective_rate)
    max_volume_usd: float = 10000.0  # Liquidity cap for Fractional Knapsack allocator
    venue: str = "Spot"     # Market source / desk label


class CurrencyGraph:
    """
    Maintains three synchronized graph representations from Lab 7:
        1. Edge List        -> O(E) iteration for Bellman-Ford
        2. Adjacency List   -> O(deg(u)) neighbor traversal for Dijkstra / Johnson's
        3. Adjacency Matrix -> O(1) rate lookup for Floyd-Warshall & cycle verification
    """

    def __init__(self, fee_pct: float = 0.0) -> None:
        if not (0.0 <= fee_pct < 100.0):
            raise ValueError("fee_pct must be in [0, 100).")
        self.fee_pct: float = fee_pct
        self.fee_fraction: float = fee_pct / 100.0

        self.currencies: List[str] = []
        self.symbol_to_idx: Dict[str, int] = {}
        self.edges: List[Edge] = []
        self.adj_list: List[List[Edge]] = []
        # Maps (u, v) -> best Edge if multiple venues quote the same pair
        self._best_edge_map: Dict[Tuple[int, int], Edge] = {}

    @property
    def num_vertices(self) -> int:
        return len(self.currencies)

    @property
    def num_edges(self) -> int:
        return len(self.edges)

    def add_currency(self, symbol: str) -> int:
        """Register a currency vertex if not present and return its integer ID."""
        sym = symbol.strip().upper()
        if sym not in self.symbol_to_idx:
            idx = len(self.currencies)
            self.symbol_to_idx[sym] = idx
            self.currencies.append(sym)
            self.adj_list.append([])
            return idx
        return self.symbol_to_idx[sym]

    def add_exchange_rate(
        self,
        source: str,
        target: str,
        rate: float,
        max_volume_usd: float = 10000.0,
        venue: str = "Spot",
    ) -> Optional[Edge]:
        """
        Add or update a directed quote source -> target with weight = -ln(rate * (1 - fee)).
        If multiple quotes exist for the same (source, target), retains the highest rate
        (minimum log-weight) as best execution.
        """
        if rate <= 0 or source.strip().upper() == target.strip().upper():
            return None

        u = self.add_currency(source)
        v = self.add_currency(target)

        eff_rate = rate * (1.0 - self.fee_fraction)
        if eff_rate <= 0:
            return None

        weight = -math.log(eff_rate)
        candidate = Edge(
            u=u,
            v=v,
            source=self.currencies[u],
            target=self.currencies[v],
            raw_rate=rate,
            effective_rate=eff_rate,
            weight=weight,
            max_volume_usd=max_volume_usd,
            venue=venue,
        )

        existing = self._best_edge_map.get((u, v))
        if existing is None or candidate.weight < existing.weight:
            self._best_edge_map[(u, v)] = candidate
            self._rebuild_structures()
            return candidate
        return existing

    def _rebuild_structures(self) -> None:
        """Synchronize edge list and adjacency list from best-execution quotes."""
        self.edges = list(self._best_edge_map.values())
        self.adj_list = [[] for _ in range(len(self.currencies))]
        for edge in self.edges:
            self.adj_list[edge.u].append(edge)

    def get_edge(self, u: int, v: int) -> Optional[Edge]:
        return self._best_edge_map.get((u, v))

    def get_edge_by_symbol(self, src: str, dst: str) -> Optional[Edge]:
        u = self.symbol_to_idx.get(src.upper())
        v = self.symbol_to_idx.get(dst.upper())
        if u is None or v is None:
            return None
        return self._best_edge_map.get((u, v))

    def build_adjacency_matrix(self) -> List[List[float]]:
        """
        Build V x V weight matrix for Floyd-Warshall (Lab 7 / Lab 8).
        Diagonal entries are 0.0; missing edges are +inf.
        """
        n = self.num_vertices
        matrix = [[ math.inf ] * n for _ in range(n)]
        for i in range(n):
            matrix[i][i] = 0.0
        for edge in self.edges:
            if edge.weight < matrix[edge.u][edge.v]:
                matrix[edge.u][edge.v] = edge.weight
        return matrix

    def clone_with_fee(self, new_fee_pct: float) -> "CurrencyGraph":
        """Create a copy of this graph recomputed at a different transaction fee %."""
        g = CurrencyGraph(fee_pct=new_fee_pct)
        for sym in self.currencies:
            g.add_currency(sym)
        for e in self.edges:
            g._best_edge_map[(e.u, e.v)] = Edge(
                u=e.u,
                v=e.v,
                source=e.source,
                target=e.target,
                raw_rate=e.raw_rate,
                effective_rate=e.raw_rate * (1.0 - g.fee_fraction),
                weight=-math.log(e.raw_rate * (1.0 - g.fee_fraction)),
                max_volume_usd=e.max_volume_usd,
                venue=e.venue,
            )
        g._rebuild_structures()
        return g
