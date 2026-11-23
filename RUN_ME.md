# ArbiGraph — Quick Start Guide

**Zero Installation Required.** ArbiGraph runs on Python 3.10+ using only the standard library. No pip install, no Flask, no Node.js.

---

## 1. Download / Get the Project

Download the entire `ArbiGraph/` folder (zip or clone). Keep the folder structure intact:

```
ArbiGraph/
├── app.py                 # Web dashboard server (run this!)
├── cli.py                 # Terminal CLI
├── arbigraph/             # All source code (algorithms, services, web)
│   ├── algorithms/
│   ├── services/
│   └── web/
├── data/                  # Offline CSV snapshots
├── docs/                  # PDF guide, DOCX build docs, manuals
├── tests/                 # Unit tests
├── requirements.txt       # (zero external deps)
└── RUN_ME.md              # (this file)
```

---

## 2. Run the Web Dashboard (Recommended)

Open a terminal inside the `ArbiGraph/` folder and run:

```bash
python3 app.py
```

You should see:

```
ArbiGraph Quant Dashboard listening on http://0.0.0.0:8000
```

Then open your browser to:

```
http://localhost:8000
```

### What you'll see in the dashboard:
- **Top bar:** Market feed selector + Live Signal / Smart Router status badge
- **Left sidebar:** Trading fee slider, ticket size, desk capital, smart currency converter, custom quote simulator
- **4 KPI cards:** Market coverage, arbitrage scanner, max fee tolerance, desk PnL / routing edge
- **Center:** Animated currency flow map + actionable order ticket
- **Bottom 4 tabs:**
  1. Live Arbitrage Signals & Desk Allocation
  2. Smart Currency Router & Rate Matrix
  3. Fee Stress-Test & Margin Cushion
  4. Scanner Speed & Market Throughput

---

## 3. Run the Terminal CLI

Scan a dataset for arbitrage:

```bash
# Institutional FX desk (arbitrage exists)
python3 cli.py --dataset fx_arbitrage_desk --capital 1000 --fee 0.0

# BDT remittance corridor (zero arbitrage → smart routing)
python3 cli.py --dataset bdt_remittance_corridor --capital 100000 --from-cur BDT --to-cur EUR

# Multi-exchange crypto (arbitrage exists)
python3 cli.py --dataset crypto_multi_exchange --capital 1000 --fee 0.0
```

Run the scaling benchmark:

```bash
python3 cli.py --benchmark
```

---

## 4. Run Unit Tests

```bash
python3 -m unittest discover -s tests -v
```

Expected: **6 tests passed**

---

## 5. Run Scripts (One-Click)

### Linux / macOS
```bash
chmod +x run_dashboard.sh
./run_dashboard.sh
```

### Windows
Double-click:
```text
run_dashboard.bat
```

---

## 6. What Each File Does

| File / Folder | Purpose |
|--------------|---------|
| `app.py` | Web dashboard server — **run this to open the UI** |
| `cli.py` | Terminal command-line interface |
| `arbigraph/algorithms/` | All CSE246 algorithms from scratch (Bellman–Ford, Johnson's, Dijkstra, Floyd–Warshall, MergeSort, Binary Search, Knapsack, Brute-Force, MinHeap) |
| `arbigraph/services/` | Market data feeds (CSV + live Kraken/FX APIs) and analysis pipeline |
| `arbigraph/web/` | Dashboard frontend (HTML, CSS, JavaScript) |
| `data/` | Offline CSV snapshots (no internet needed) |
| `docs/` | Visual guide PDF, build documentation DOCX, user manual, viva guide |
| `tests/` | 6 automated unit tests |

---

## 7. Troubleshooting

**Port 8000 already in use?**
```bash
python3 app.py --port 8001
```
Then open `http://localhost:8001`

**"command not found: python3"?**
Try `python` instead of `python3`:
```bash
python app.py
```

**Tables appear empty?**
Make sure you're running `app.py` first and accessing `http://localhost:8000`. Opening `index.html` directly as a file (without the server) will not load data.

**Need help?**
- See `docs/DASHBOARD_USER_MANUAL.md` for a plain-English dashboard tour
- See `docs/ArbiGraph_Dashboard_Guide.pdf` for screenshots of every screen
- See `docs/VIVA_GUIDE.md` for common instructor questions & answers

---

## 8. System Requirements

- Python 3.10 or higher
- Any modern web browser (Chrome, Firefox, Edge, Safari)
- Internet access only needed for **live** Kraken/FX feeds (offline CSV snapshots work without internet)
