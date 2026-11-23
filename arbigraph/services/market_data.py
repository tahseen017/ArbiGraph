"""
Market Data Service — Live Public REST APIs + Curated Offline CSV Snapshots.

Supports 5 Market Modes out of the box (Zero API keys required):
    1. `fx_arbitrage_desk`       : Institutional FX cross-desk snapshot (3 arbitrage loops: 3-hop & 4-hop)
    2. `bdt_remittance_corridor` : Calm arbitrage-free BDT/Global remittance network (showcases Johnson's Algorithm!)
    3. `crypto_multi_exchange`   : Multi-exchange BTC/ETH/SOL/USDT/EUR snapshot with liquidity caps
    4. `live_kraken`             : Real-time live orderbook Bid/Ask quotes from Kraken Public API
    5. `live_fiat`               : Real-time live global FX rates (including BDT) from Open Exchange Rates & ECB
"""

from __future__ import annotations
import csv
from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import urllib.request

from ..algorithms.graph import CurrencyGraph

DATA_DIR = Path(__file__).resolve().parents[2] / "data"


@dataclass
class QuoteRecord:
    source: str
    target: str
    rate: float
    max_volume_usd: float
    venue: str


@dataclass
class MarketSnapshot:
    dataset_id: str
    title: str
    description: str
    is_live: bool
    fetched_at_utc: str
    quotes: List[QuoteRecord]
    warning: Optional[str] = None


DATASET_CATALOG: List[Dict[str, str]] = [
    {
        "id": "fx_arbitrage_desk",
        "title": "Institutional FX Cross-Desk Feed",
        "mode": "Desk Snapshot",
        "description": "Spot quotes across London, NY, Frankfurt, Singapore, Tokyo, Zurich & Dhaka desks (USD, EUR, GBP, JPY, CHF, CAD, AUD, SGD, BDT) with cross-market price dislocations.",
    },
    {
        "id": "bdt_remittance_corridor",
        "title": "BDT & Global Remittance Corridors",
        "mode": "Desk Snapshot",
        "description": "10-currency international treasury & remittance network centered on BDT, USD, EUR, GBP, AED, SAR, SGD, MYR, INR & JPY for low-cost multi-currency routing.",
    },
    {
        "id": "crypto_multi_exchange",
        "title": "Multi-Exchange Crypto Spot Book",
        "mode": "Desk Snapshot",
        "description": "Aggregated spot quotes across Binance, Kraken, Coinbase & Bybit (BTC, ETH, SOL, BNB, USDT, USD, EUR, GBP) with real-style orderbook liquidity caps.",
    },
    {
        "id": "live_kraken",
        "title": "LIVE Kraken Spot Orderbook (Bid/Ask)",
        "mode": "Live Market",
        "description": "Real-time executable Bid and Ask orderbook quotes streamed from Kraken's public market feed (BTC, ETH, SOL, USDT, USD, EUR, GBP, JPY).",
    },
    {
        "id": "live_fiat",
        "title": "LIVE Global FX + BDT Interbank Feed",
        "mode": "Live Market",
        "description": "Live foreign exchange reference & interbank quotes across BDT, USD, EUR, GBP, JPY, SGD, AED, INR, CHF, CAD & AUD.",
    },
]

# Exact mapping of Kraken canonical asset pair keys -> (base_symbol, quote_symbol, est_liquidity_usd)
KRAKEN_PAIR_MAP: Dict[str, Tuple[str, str, float]] = {
    "XXBTZUSD": ("BTC", "USD", 25000.0),
    "XXBTZEUR": ("BTC", "EUR", 18000.0),
    "XXBTZGBP": ("BTC", "GBP", 10000.0),
    "XBTUSDT": ("BTC", "USDT", 22000.0),
    "XETHZUSD": ("ETH", "USD", 20000.0),
    "XETHZEUR": ("ETH", "EUR", 15000.0),
    "XETHZGBP": ("ETH", "GBP", 9000.0),
    "XETHXXBT": ("ETH", "BTC", 14000.0),
    "ETHUSDT": ("ETH", "USDT", 18000.0),
    "SOLUSD": ("SOL", "USD", 12000.0),
    "SOLEUR": ("SOL", "EUR", 8500.0),
    "SOLUSDT": ("SOL", "USDT", 12000.0),
    "ZEURZUSD": ("EUR", "USD", 30000.0),
    "ZGBPZUSD": ("GBP", "USD", 25000.0),
    "EURGBP": ("EUR", "GBP", 20000.0),
    "ZUSDZJPY": ("USD", "JPY", 25000.0),
    "EURJPY": ("EUR", "JPY", 16000.0),
    "USDTZUSD": ("USDT", "USD", 35000.0),
}


def _utc_now_str() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def _http_get_json(url: str, timeout: float = 6.0) -> dict:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "ArbiGraph-CSE246/1.0", "Accept": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def load_csv_snapshot(dataset_id: str) -> MarketSnapshot:
    csv_map = {
        "fx_arbitrage_desk": (
            "fx_arbitrage_desk.csv",
            "Institutional FX Cross-Desk Feed",
            "Spot currency quotes across London, NY, Frankfurt, Singapore, Tokyo, Zurich & Dhaka desks.",
        ),
        "bdt_remittance_corridor": (
            "bdt_remittance_corridor.csv",
            "BDT & Global Remittance Corridors",
            "International treasury & remittance network across BDT, USD, EUR, GBP, AED, SAR, SGD, MYR, INR & JPY.",
        ),
        "crypto_multi_exchange": (
            "crypto_multi_exchange.csv",
            "Multi-Exchange Crypto Spot Book",
            "Aggregated spot orderbooks across Binance, Kraken, Coinbase & Bybit with venue liquidity caps.",
        ),
    }
    if dataset_id not in csv_map:
        raise ValueError(f"Unknown CSV dataset_id: {dataset_id}")

    filename, title, desc = csv_map[dataset_id]
    path = DATA_DIR / filename
    quotes: List[QuoteRecord] = []
    with path.open("r", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            quotes.append(
                QuoteRecord(
                    source=row["source"].strip().upper(),
                    target=row["target"].strip().upper(),
                    rate=float(row["rate"]),
                    max_volume_usd=float(row.get("max_volume_usd", 10000.0)),
                    venue=row.get("venue", "CSV-Snapshot").strip(),
                )
            )

    return MarketSnapshot(
        dataset_id=dataset_id,
        title=title,
        description=desc,
        is_live=False,
        fetched_at_utc="Static Snapshot (Offline-Safe)",
        quotes=quotes,
    )


def fetch_live_kraken_snapshot() -> MarketSnapshot:
    """
    Pull real-time orderbook Bid and Ask prices from Kraken's public Ticker endpoint.
    Selling `base -> quote` executes at `bid`; buying `quote -> base` executes at `1 / ask`.
    """
    pairs_query = ",".join([
        "XBTUSD", "XBTEUR", "XBTGBP", "XBTUSDT",
        "ETHUSD", "ETHEUR", "ETHGBP", "ETHXBT", "ETHUSDT",
        "SOLUSD", "SOLEUR", "SOLUSDT",
        "EURUSD", "GBPUSD", "EURGBP", "USDJPY", "EURJPY", "USDTZUSD",
    ])
    url = f"https://api.kraken.com/0/public/Ticker?pair={pairs_query}"
    try:
        payload = _http_get_json(url, timeout=6.5)
        result = payload.get("result", {})
        quotes: List[QuoteRecord] = []

        for k_pair, info in result.items():
            mapping = KRAKEN_PAIR_MAP.get(k_pair)
            if not mapping:
                continue
            base, quote, vol = mapping
            ask = float(info["a"][0])
            bid = float(info["b"][0])
            if bid > 0:
                quotes.append(
                    QuoteRecord(
                        source=base,
                        target=quote,
                        rate=bid,
                        max_volume_usd=vol,
                        venue="Kraken-Bid",
                    )
                )
            if ask > 0:
                quotes.append(
                    QuoteRecord(
                        source=quote,
                        target=base,
                        rate=1.0 / ask,
                        max_volume_usd=vol,
                        venue="Kraken-Ask",
                    )
                )

        if not quotes:
            raise RuntimeError("Kraken returned an empty quote book.")

        return MarketSnapshot(
            dataset_id="live_kraken",
            title="LIVE Kraken Orderbook (Executable Bid/Ask)",
            description="Live real-time Bid/Ask orderbook prices from Kraken Public REST API.",
            is_live=True,
            fetched_at_utc=_utc_now_str(),
            quotes=quotes,
        )
    except Exception as exc:
        fallback = load_csv_snapshot("crypto_multi_exchange")
        fallback.dataset_id = "live_kraken"
        fallback.warning = f"Live Kraken API unreachable ({exc}); gracefully fell back to offline crypto snapshot."
        return fallback


def fetch_live_fiat_snapshot() -> MarketSnapshot:
    """
    Fetch live global FX rates (including BDT!) from Open Exchange Rates API
    and cross-pollinate European pairs from ECB Frankfurter API.
    """
    selected = ["USD", "EUR", "GBP", "BDT", "JPY", "SGD", "AED", "INR", "CHF", "CAD", "AUD"]
    try:
        usd_data = _http_get_json("https://open.er-api.com/v6/latest/USD", timeout=6.5)
        rates = usd_data.get("rates", {})
        if not rates:
            raise RuntimeError("Missing 'rates' in ER-API response.")

        quotes: List[QuoteRecord] = []
        # Hub USD quotes (tight 8 bps interbank half-spread)
        for sym in selected:
            if sym == "USD" or sym not in rates:
                continue
            r = float(rates[sym])
            quotes.append(QuoteRecord("USD", sym, r * 0.9992, 20000.0, "ER-Interbank"))
            quotes.append(QuoteRecord(sym, "USD", (1.0 / r) * 0.9992, 20000.0, "ER-Interbank"))

        # Regional direct retail quotes (wider 55 bps spread so Johnson's finds multi-hop savings!)
        retail_pairs = [
            ("BDT", "EUR"), ("EUR", "BDT"),
            ("BDT", "GBP"), ("GBP", "BDT"),
            ("BDT", "SGD"), ("AED", "BDT"),
            ("BDT", "INR"), ("INR", "BDT"),
            ("CAD", "AUD"), ("AUD", "JPY"),
        ]
        for a, b in retail_pairs:
            if a in rates and b in rates:
                cross = (float(rates[b]) / float(rates[a])) * 0.9935
                quotes.append(QuoteRecord(a, b, cross, 6000.0, "Retail-Desk"))

        # Overlay live ECB quotes from Frankfurter for EUR crosses (creates real cross-source pricing!)
        try:
            ecb = _http_get_json(
                "https://api.frankfurter.app/latest?from=EUR&to=USD,GBP,JPY,CHF,SGD,CAD,AUD",
                timeout=4.5,
            )
            ecb_rates = ecb.get("rates", {})
            for sym, val in ecb_rates.items():
                r_eur = float(val)
                quotes.append(QuoteRecord("EUR", sym, r_eur * 0.9994, 25000.0, "ECB-Spot"))
                quotes.append(QuoteRecord(sym, "EUR", (1.0 / r_eur) * 0.9994, 25000.0, "ECB-Spot"))
        except Exception:
            pass

        return MarketSnapshot(
            dataset_id="live_fiat",
            title="LIVE Global FX + BDT Interbank & ECB Feed",
            description="Live foreign exchange quotes fetched from Open Exchange Rates & European Central Bank.",
            is_live=True,
            fetched_at_utc=_utc_now_str(),
            quotes=quotes,
        )
    except Exception as exc:
        fallback = load_csv_snapshot("bdt_remittance_corridor")
        fallback.dataset_id = "live_fiat"
        fallback.warning = f"Live FX API unreachable ({exc}); gracefully fell back to offline BDT corridor."
        return fallback


def get_market_snapshot(dataset_id: str) -> MarketSnapshot:
    if dataset_id == "live_kraken":
        return fetch_live_kraken_snapshot()
    if dataset_id == "live_fiat":
        return fetch_live_fiat_snapshot()
    return load_csv_snapshot(dataset_id)


def build_graph_from_snapshot(
    snapshot: MarketSnapshot,
    fee_pct: float = 0.0,
    rate_overrides: Optional[List[Dict[str, object]]] = None,
) -> CurrencyGraph:
    """
    Construct a `CurrencyGraph` from `snapshot` and apply any interactive rate overrides
    entered by the user or instructor during a live demonstration.
    """
    graph = CurrencyGraph(fee_pct=fee_pct)
    override_map: Dict[Tuple[str, str], Tuple[float, float]] = {}

    if rate_overrides:
        for ov in rate_overrides:
            src = str(ov.get("source", "")).strip().upper()
            dst = str(ov.get("target", "")).strip().upper()
            rate = float(ov.get("rate", 0.0))
            vol = float(ov.get("max_volume_usd", 10000.0))
            if src and dst and rate > 0:
                override_map[(src, dst)] = (rate, vol)

    for q in snapshot.quotes:
        key = (q.source, q.target)
        if key in override_map:
            r_val, v_val = override_map.pop(key)
            graph.add_exchange_rate(q.source, q.target, r_val, v_val, venue="Custom-Override")
        else:
            graph.add_exchange_rate(q.source, q.target, q.rate, q.max_volume_usd, venue=q.venue)

    # Add brand-new custom edges that weren't in the base snapshot
    for (src, dst), (r_val, v_val) in override_map.items():
        graph.add_exchange_rate(src, dst, r_val, v_val, venue="Custom-Override")

    return graph
