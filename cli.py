#!/usr/bin/env python3
"""
ArbiGraph Terminal CLI — CSE246 Term Project Runner.

Usage examples:
    python3 cli.py
    python3 cli.py --dataset fx_arbitrage_desk --capital 1000 --fee 0.0
    python3 cli.py --dataset bdt_remittance_corridor --capital 100000 --from-cur BDT --to-cur EUR
    python3 cli.py --dataset live_kraken --fee 0.0
    python3 cli.py --benchmark
"""

from __future__ import annotations
import argparse
import sys

from arbigraph.algorithms.benchmark import run_scaling_benchmark
from arbigraph.services.engine import run_full_market_analysis
from arbigraph.services.market_data import DATASET_CATALOG

BOLD = "\033[1m"
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RED = "\033[91m"
DIM = "\033[2m"
RESET = "\033[0m"


def print_banner() -> None:
    print(f"{BOLD}{CYAN}" + "=" * 78)
    print("  ArbiGraph — FX & Crypto Arbitrage + Multi-Hop Routing Engine (CSE246)")
    print("  Algorithms: Bellman-Ford | Johnson's (BF + Dijkstra) | MergeSort | BinSearch")
    print("=" * 78 + f"{RESET}")


def run_cli() -> int:
    parser = argparse.ArgumentParser(
        description="ArbiGraph CSE246 CLI — Arbitrage Detection & Optimal Currency Routing"
    )
    parser.add_argument(
        "--dataset",
        default="fx_arbitrage_desk",
        choices=[d["id"] for d in DATASET_CATALOG],
        help="Market dataset or live API feed to analyze",
    )
    parser.add_argument("--fee", type=float, default=0.0, help="Transaction fee %% per trade (e.g. 0.1)")
    parser.add_argument("--capital", type=float, default=1000.0, help="Starting trade amount")
    parser.add_argument("--budget", type=float, default=10000.0, help="Total USD budget for Knapsack")
    parser.add_argument("--from-cur", default=None, help="Source currency for Johnson's routing")
    parser.add_argument("--to-cur", default=None, help="Target currency for Johnson's routing")
    parser.add_argument(
        "--benchmark",
        action="store_true",
        help="Run empirical scaling benchmark (Johnson's vs Floyd-Warshall up to V=160)",
    )
    args = parser.parse_args()

    print_banner()

    if args.benchmark:
        print(f"\n{BOLD}Running Empirical Scaling Benchmark (Sparse Hub-and-Spoke FX Graphs)...{RESET}\n")
        pts = run_scaling_benchmark()
        print(
            f"{'Vertices (V)':<14}{'Edges (E)':<12}{'Bellman-Ford':<16}"
            f"{'Johnsons':<16}{'Floyd-Warshall':<18}{'FW/Johnsons':<14}{'Max Diff'}"
        )
        print("-" * 98)
        for p in pts:
            print(
                f"{p.vertices:<14}{p.edges:<12}{p.bellman_ford_ms:>8.3f} ms     "
                f"{p.johnsons_ms:>8.3f} ms     {p.floyd_warshall_ms:>9.3f} ms      "
                f"{GREEN}{p.speedup_factor:>6.2f}x{RESET}       {p.max_matrix_diff:.1e}"
            )
        print()
        return 0

    report = run_full_market_analysis(
        dataset_id=args.dataset,
        fee_pct=args.fee,
        starting_capital=args.capital,
        trader_budget_usd=args.budget,
        route_source=args.from_cur,
        route_target=args.to_cur,
    )

    snap = report["snapshot"]
    g = report["graph"]
    bf = report["bellman_ford"]
    be = report["break_even_fee"]

    print(f"\n{BOLD}Market Feed :{RESET} {snap['title']} ({snap['fetched_at_utc']})")
    if snap["warning"]:
        print(f"{YELLOW}Warning     : {snap['warning']}{RESET}")
    print(
        f"{BOLD}Topology    :{RESET} V = {g['num_vertices']} currencies | E = {g['num_edges']} directed quotes "
        f"| Negative -ln(R) edges = {g['negative_edges_count']} | Fee = {g['fee_pct']:.3f}%"
    )
    print(
        f"{BOLD}Bellman-Ford:{RESET} {bf['passes_executed']}/{bf['max_possible_passes']} passes "
        f"(Early-Exit={bf['early_stopped']}) in {bf['execution_time_ms']:.3f} ms"
    )

    if bf["has_arbitrage"]:
        print(f"\n{BOLD}{GREEN}[!] ARBITRAGE DETECTED — {bf['cycles_count']} Verified Negative-Weight Cycle(s):{RESET}")
        print("-" * 78)
        for idx, cyc in enumerate(bf["cycles"], start=1):
            route_str = " -> ".join(cyc["path"])
            print(
                f"  #{idx}  {BOLD}{route_str}{RESET}\n"
                f"      Log-Weight Sum : {cyc['total_log_weight']:.6f} (< 0)  |  "
                f"Profit: {GREEN}+{cyc['profit_pct']:.4f}%{RESET}  |  "
                f"Liquidity Cap: ${cyc['bottleneck_volume_usd']:,.0f}"
            )

        top = bf["cycles"][0]
        print(f"\n{BOLD}Step-by-Step Execution Ledger (Top Cycle #{1}, Start = {args.capital:,.2f} {top['path'][0]}):{RESET}")
        for st in top["steps"]:
            print(
                f"   Step {st['step_num']}: {st['amount_in']:>12,.4f} {st['from_currency']} "
                f"--(@ {st['effective_rate']:.6g}, w={st['weight']:+.5f}, {st['venue']})--> "
                f"{st['amount_out']:>12,.4f} {st['to_currency']}"
            )
        print(
            f"   {BOLD}Net Result:{RESET} {top['starting_capital']:,.2f} -> "
            f"{GREEN}{top['ending_capital']:,.2f} {top['path'][0]} (+{top['net_profit']:,.2f}){RESET}"
        )

        cmp_bf = report["brute_force_comparison"]
        print(
            f"\n{BOLD}Lab 1 Brute-Force 3-Hop Baseline:{RESET} Found {cmp_bf['profitable_3hop_count']} 3-hop loops, "
            f"MISSED {YELLOW}{cmp_bf['multi_hop_cycles_missed_by_brute_force']}{RESET} longer (4+/5-hop) arbitrage cycle(s)!"
        )
        print(
            f"{BOLD}Lab 1 Binary Search Break-Even Fee:{RESET} Arbitrage vanishes above fee = "
            f"{CYAN}{be['max_tolerable_fee_pct']:.4f}%{RESET} ({be['iterations']} bisection steps)"
        )

        alloc = report["capital_allocation"]
        print(
            f"\n{BOLD}Lab 4 Fractional Knapsack Capital Allocation (Budget = ${alloc['total_budget_usd']:,.2f}):{RESET}"
        )
        for item in alloc["allocations"]:
            print(
                f"   Allocate ${item['allocated_usd']:>9,.2f} / ${item['liquidity_cap_usd']:>8,.0f} cap "
                f"({item['fraction_of_cap_used']*100:>5.1f}%) to {' -> '.join(item['cycle_path'])} "
                f"=> Expected Profit: {GREEN}+${item['expected_profit_usd']:,.2f}{RESET}"
            )
        print(
            f"   {BOLD}Total Portfolio Profit:{RESET} {GREEN}+${alloc['total_expected_profit_usd']:,.2f}{RESET} "
            f"(Blended ROI: +{alloc['blended_roi_pct']:.3f}%)"
        )
    else:
        jn = report["johnsons"]
        print(f"\n{BOLD}{CYAN}[✓] MARKET EQUILIBRIUM (Zero Arbitrage) — Activating Johnson's All-Pairs Routing{RESET}")
        print(
            f"    Phase 1 (Bellman-Ford Potentials) + Phase 2 (w_hat >= 0 Reweighting) + "
            f"Phase 3 ({g['num_vertices']}x Custom-MinHeap Dijkstra)"
        )
        print(
            f"    Runtime: Johnson's = {jn['execution_time_ms']:.3f} ms | "
            f"Floyd-Warshall Cross-Check = {jn['floyd_warshall_time_ms']:.3f} ms"
        )
        rt = jn["selected_route"]
        if rt:
            print(f"\n{BOLD}Optimal Conversion Route ({rt['source']} -> {rt['target']} for {rt['amount_in']:,.2f} {rt['source']}):{RESET}")
            print(f"   Best Path   : {GREEN}{' -> '.join(rt['path'])}{RESET} ({rt['hops']} hop(s))")
            print(f"   Amount Out  : {GREEN}{rt['amount_out']:,.4f} {rt['target']}{RESET} (Eff. Rate: {rt['best_effective_rate']:.6g})")
            if rt["direct_amount_out"] is not None:
                print(
                    f"   Direct 1-Hop: {rt['direct_amount_out']:,.4f} {rt['target']} "
                    f"(Gain: {CYAN}+{rt['improvement_bps']:.1f} bps{RESET})"
                )
            else:
                print(f"   Direct 1-Hop: {DIM}No direct quote exists — routed via hub currencies!{RESET}")

    print()
    return 0


if __name__ == "__main__":
    sys.exit(run_cli())
