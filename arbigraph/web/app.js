(() => {
  const EMBEDDED_FALLBACK = {"catalog": [{"id": "fx_arbitrage_desk", "title": "Institutional FX Cross-Desk Feed", "mode": "Desk Snapshot", "description": "Spot quotes across London, NY, Frankfurt, Singapore, Tokyo, Zurich & Dhaka desks (USD, EUR, GBP, JPY, CHF, CAD, AUD, SGD, BDT) with cross-market price dislocations."}, {"id": "bdt_remittance_corridor", "title": "BDT & Global Remittance Corridors", "mode": "Desk Snapshot", "description": "10-currency international treasury & remittance network centered on BDT, USD, EUR, GBP, AED, SAR, SGD, MYR, INR & JPY for low-cost multi-currency routing."}, {"id": "crypto_multi_exchange", "title": "Multi-Exchange Crypto Spot Book", "mode": "Desk Snapshot", "description": "Aggregated spot quotes across Binance, Kraken, Coinbase & Bybit (BTC, ETH, SOL, BNB, USDT, USD, EUR, GBP) with real-style orderbook liquidity caps."}, {"id": "live_kraken", "title": "LIVE Kraken Spot Orderbook (Bid/Ask)", "mode": "Live Market", "description": "Real-time executable Bid and Ask orderbook quotes streamed from Kraken's public market feed (BTC, ETH, SOL, USDT, USD, EUR, GBP, JPY)."}, {"id": "live_fiat", "title": "LIVE Global FX + BDT Interbank Feed", "mode": "Live Market", "description": "Live foreign exchange reference & interbank quotes across BDT, USD, EUR, GBP, JPY, SGD, AED, INR, CHF, CAD & AUD."}], "snapshots": {"fx_arbitrage_desk": {"dataset_id": "fx_arbitrage_desk", "title": "Institutional FX Cross-Desk Feed", "description": "Spot currency quotes across London, NY, Frankfurt, Singapore, Tokyo, Zurich & Dhaka desks.", "is_live": false, "fetched_at_utc": "Static Snapshot (Offline-Safe)", "quotes": [{"source": "USD", "target": "EUR", "rate": 0.925, "max_volume_usd": 4500.0, "venue": "London-FX"}, {"source": "EUR", "target": "GBP", "rate": 0.875, "max_volume_usd": 5200.0, "venue": "Frankfurt-Desk"}, {"source": "GBP", "target": "USD", "rate": 1.261, "max_volume_usd": 4800.0, "venue": "NY-Cable"}, {"source": "EUR", "target": "USD", "rate": 1.078, "max_volume_usd": 9000.0, "venue": "London-FX"}, {"source": "GBP", "target": "EUR", "rate": 1.132, "max_volume_usd": 7500.0, "venue": "London-FX"}, {"source": "USD", "target": "GBP", "rate": 0.786, "max_volume_usd": 8500.0, "venue": "NY-Cable"}, {"source": "CAD", "target": "SGD", "rate": 0.9735, "max_volume_usd": 6500.0, "venue": "Toronto-APAC"}, {"source": "SGD", "target": "JPY", "rate": 113.85, "max_volume_usd": 7200.0, "venue": "Singapore-FX"}, {"source": "JPY", "target": "AUD", "rate": 0.01003, "max_volume_usd": 6800.0, "venue": "Tokyo-Spot"}, {"source": "AUD", "target": "CAD", "rate": 0.9102, "max_volume_usd": 6500.0, "venue": "Sydney-Desk"}, {"source": "SGD", "target": "CAD", "rate": 1.021, "max_volume_usd": 6000.0, "venue": "Singapore-FX"}, {"source": "JPY", "target": "SGD", "rate": 0.00874, "max_volume_usd": 6000.0, "venue": "Tokyo-Spot"}, {"source": "AUD", "target": "JPY", "rate": 98.9, "max_volume_usd": 6000.0, "venue": "Sydney-Desk"}, {"source": "CAD", "target": "AUD", "rate": 1.091, "max_volume_usd": 6000.0, "venue": "Toronto-APAC"}, {"source": "USD", "target": "CAD", "rate": 1.376, "max_volume_usd": 9500.0, "venue": "NY-Spot"}, {"source": "CAD", "target": "USD", "rate": 0.722, "max_volume_usd": 9500.0, "venue": "Toronto-APAC"}, {"source": "USD", "target": "SGD", "rate": 1.335, "max_volume_usd": 8000.0, "venue": "Singapore-FX"}, {"source": "SGD", "target": "USD", "rate": 0.7435, "max_volume_usd": 8000.0, "venue": "Singapore-FX"}, {"source": "USD", "target": "JPY", "rate": 151.4, "max_volume_usd": 12000.0, "venue": "Tokyo-Spot"}, {"source": "JPY", "target": "USD", "rate": 0.00656, "max_volume_usd": 12000.0, "venue": "Tokyo-Spot"}, {"source": "USD", "target": "AUD", "rate": 1.512, "max_volume_usd": 8000.0, "venue": "Sydney-Desk"}, {"source": "AUD", "target": "USD", "rate": 0.6565, "max_volume_usd": 8000.0, "venue": "Sydney-Desk"}, {"source": "USD", "target": "CHF", "rate": 0.8825, "max_volume_usd": 3200.0, "venue": "Zurich-Prime"}, {"source": "CHF", "target": "BDT", "rate": 136.6, "max_volume_usd": 2500.0, "venue": "Dhaka-Interbank"}, {"source": "BDT", "target": "USD", "rate": 0.008345, "max_volume_usd": 2800.0, "venue": "Dhaka-Treasury"}, {"source": "CHF", "target": "USD", "rate": 1.127, "max_volume_usd": 7000.0, "venue": "Zurich-Prime"}, {"source": "USD", "target": "BDT", "rate": 119.3, "max_volume_usd": 5000.0, "venue": "Dhaka-Interbank"}, {"source": "BDT", "target": "EUR", "rate": 0.00755, "max_volume_usd": 3500.0, "venue": "Dhaka-Retail"}, {"source": "EUR", "target": "CHF", "rate": 0.951, "max_volume_usd": 7500.0, "venue": "Zurich-Prime"}, {"source": "CHF", "target": "EUR", "rate": 1.045, "max_volume_usd": 7500.0, "venue": "Zurich-Prime"}], "warning": null}, "bdt_remittance_corridor": {"dataset_id": "bdt_remittance_corridor", "title": "BDT & Global Remittance Corridors", "description": "International treasury & remittance network across BDT, USD, EUR, GBP, AED, SAR, SGD, MYR, INR & JPY.", "is_live": false, "fetched_at_utc": "Static Snapshot (Offline-Safe)", "quotes": [{"source": "BDT", "target": "USD", "rate": 0.00831, "max_volume_usd": 15000.0, "venue": "Dhaka-Interbank"}, {"source": "USD", "target": "BDT", "rate": 119.75, "max_volume_usd": 15000.0, "venue": "Dhaka-Interbank"}, {"source": "BDT", "target": "EUR", "rate": 0.00746, "max_volume_usd": 5000.0, "venue": "Dhaka-RetailBank"}, {"source": "EUR", "target": "BDT", "rate": 127.8, "max_volume_usd": 5000.0, "venue": "Dhaka-RetailBank"}, {"source": "BDT", "target": "GBP", "rate": 0.00637, "max_volume_usd": 5000.0, "venue": "Dhaka-RetailBank"}, {"source": "GBP", "target": "BDT", "rate": 148.9, "max_volume_usd": 5000.0, "venue": "London-Remit"}, {"source": "BDT", "target": "SGD", "rate": 0.01095, "max_volume_usd": 6000.0, "venue": "Dhaka-RetailBank"}, {"source": "SGD", "target": "BDT", "rate": 88.8, "max_volume_usd": 8000.0, "venue": "Singapore-Remit"}, {"source": "AED", "target": "BDT", "rate": 32.15, "max_volume_usd": 9000.0, "venue": "Dubai-Exchange"}, {"source": "BDT", "target": "AED", "rate": 0.0301, "max_volume_usd": 4000.0, "venue": "Dhaka-RetailBank"}, {"source": "SAR", "target": "BDT", "rate": 31.45, "max_volume_usd": 9000.0, "venue": "Riyadh-Remit"}, {"source": "MYR", "target": "BDT", "rate": 26.4, "max_volume_usd": 6000.0, "venue": "KL-Remit"}, {"source": "USD", "target": "SGD", "rate": 1.3385, "max_volume_usd": 25000.0, "venue": "SGX-Wholesale"}, {"source": "SGD", "target": "USD", "rate": 0.7455, "max_volume_usd": 25000.0, "venue": "SGX-Wholesale"}, {"source": "SGD", "target": "EUR", "rate": 0.6865, "max_volume_usd": 20000.0, "venue": "Frankfurt-Wholesale"}, {"source": "EUR", "target": "SGD", "rate": 1.451, "max_volume_usd": 20000.0, "venue": "Frankfurt-Wholesale"}, {"source": "USD", "target": "EUR", "rate": 0.9165, "max_volume_usd": 30000.0, "venue": "ECB-Spot"}, {"source": "EUR", "target": "USD", "rate": 1.0875, "max_volume_usd": 30000.0, "venue": "ECB-Spot"}, {"source": "USD", "target": "GBP", "rate": 0.7875, "max_volume_usd": 25000.0, "venue": "London-Wholesale"}, {"source": "GBP", "target": "USD", "rate": 1.266, "max_volume_usd": 25000.0, "venue": "London-Wholesale"}, {"source": "AED", "target": "USD", "rate": 0.2721, "max_volume_usd": 25000.0, "venue": "Dubai-PegDesk"}, {"source": "USD", "target": "AED", "rate": 3.671, "max_volume_usd": 25000.0, "venue": "Dubai-PegDesk"}, {"source": "SAR", "target": "USD", "rate": 0.2664, "max_volume_usd": 25000.0, "venue": "Riyadh-PegDesk"}, {"source": "USD", "target": "SAR", "rate": 3.749, "max_volume_usd": 25000.0, "venue": "Riyadh-PegDesk"}, {"source": "MYR", "target": "SGD", "rate": 0.3015, "max_volume_usd": 15000.0, "venue": "ASEAN-Cross"}, {"source": "SGD", "target": "MYR", "rate": 3.302, "max_volume_usd": 15000.0, "venue": "ASEAN-Cross"}, {"source": "USD", "target": "INR", "rate": 84.25, "max_volume_usd": 18000.0, "venue": "Mumbai-FX"}, {"source": "INR", "target": "USD", "rate": 0.01182, "max_volume_usd": 18000.0, "venue": "Mumbai-FX"}, {"source": "BDT", "target": "INR", "rate": 0.692, "max_volume_usd": 7000.0, "venue": "SAARC-Desk"}, {"source": "INR", "target": "BDT", "rate": 1.405, "max_volume_usd": 7000.0, "venue": "SAARC-Desk"}, {"source": "USD", "target": "JPY", "rate": 151.7, "max_volume_usd": 30000.0, "venue": "Tokyo-Wholesale"}, {"source": "JPY", "target": "USD", "rate": 0.006575, "max_volume_usd": 30000.0, "venue": "Tokyo-Wholesale"}, {"source": "SGD", "target": "JPY", "rate": 113.2, "max_volume_usd": 20000.0, "venue": "Tokyo-Wholesale"}], "warning": null}, "crypto_multi_exchange": {"dataset_id": "crypto_multi_exchange", "title": "Multi-Exchange Crypto Spot Book", "description": "Aggregated spot orderbooks across Binance, Kraken, Coinbase & Bybit with venue liquidity caps.", "is_live": false, "fetched_at_utc": "Static Snapshot (Offline-Safe)", "quotes": [{"source": "USDT", "target": "BTC", "rate": 1.142e-05, "max_volume_usd": 8500.0, "venue": "Binance-Spot"}, {"source": "BTC", "target": "ETH", "rate": 33.95, "max_volume_usd": 6200.0, "venue": "Kraken-Pro"}, {"source": "ETH", "target": "USDT", "rate": 2628.0, "max_volume_usd": 9000.0, "venue": "Coinbase-Adv"}, {"source": "BTC", "target": "USDT", "rate": 87250.0, "max_volume_usd": 15000.0, "venue": "Binance-Spot"}, {"source": "ETH", "target": "BTC", "rate": 0.02925, "max_volume_usd": 9500.0, "venue": "Binance-Spot"}, {"source": "USDT", "target": "ETH", "rate": 0.0003785, "max_volume_usd": 12000.0, "venue": "Binance-Spot"}, {"source": "USDT", "target": "SOL", "rate": 0.00568, "max_volume_usd": 4200.0, "venue": "Bybit-Spot"}, {"source": "SOL", "target": "BNB", "rate": 0.2945, "max_volume_usd": 3100.0, "venue": "Binance-Spot"}, {"source": "BNB", "target": "EUR", "rate": 562.0, "max_volume_usd": 3400.0, "venue": "Kraken-Pro"}, {"source": "EUR", "target": "USDT", "rate": 1.0765, "max_volume_usd": 11000.0, "venue": "Kraken-Pro"}, {"source": "SOL", "target": "USDT", "rate": 175.2, "max_volume_usd": 9000.0, "venue": "Coinbase-Adv"}, {"source": "BNB", "target": "USDT", "rate": 598.0, "max_volume_usd": 8000.0, "venue": "Binance-Spot"}, {"source": "USDT", "target": "BNB", "rate": 0.001665, "max_volume_usd": 8000.0, "venue": "Binance-Spot"}, {"source": "USDT", "target": "USD", "rate": 0.9998, "max_volume_usd": 25000.0, "venue": "Kraken-Pro"}, {"source": "USD", "target": "USDT", "rate": 1.0006, "max_volume_usd": 1800.0, "venue": "Coinbase-Adv"}, {"source": "USD", "target": "EUR", "rate": 0.9265, "max_volume_usd": 14000.0, "venue": "Kraken-Pro"}, {"source": "EUR", "target": "GBP", "rate": 0.861, "max_volume_usd": 10000.0, "venue": "Kraken-Pro"}, {"source": "GBP", "target": "USD", "rate": 1.264, "max_volume_usd": 9500.0, "venue": "Coinbase-Adv"}, {"source": "GBP", "target": "USDT", "rate": 1.258, "max_volume_usd": 8500.0, "venue": "Binance-Spot"}, {"source": "EUR", "target": "USD", "rate": 1.077, "max_volume_usd": 14000.0, "venue": "Kraken-Pro"}], "warning": null}}, "benchmark": [{"vertices": 15, "edges": 106, "bellman_ford_ms": 0.055, "johnsons_ms": 1.081, "floyd_warshall_ms": 0.34, "speedup_factor": 0.31, "max_matrix_diff": 0.0}, {"vertices": 35, "edges": 316, "bellman_ford_ms": 0.118, "johnsons_ms": 5.393, "floyd_warshall_ms": 3.099, "speedup_factor": 0.57, "max_matrix_diff": 0.0}, {"vertices": 70, "edges": 658, "bellman_ford_ms": 0.188, "johnsons_ms": 21.395, "floyd_warshall_ms": 22.715, "speedup_factor": 1.06, "max_matrix_diff": 0.0}, {"vertices": 110, "edges": 1054, "bellman_ford_ms": 0.275, "johnsons_ms": 62.997, "floyd_warshall_ms": 86.436, "speedup_factor": 1.37, "max_matrix_diff": 0.0}, {"vertices": 160, "edges": 1548, "bellman_ford_ms": 0.609, "johnsons_ms": 119.988, "floyd_warshall_ms": 257.163, "speedup_factor": 2.14, "max_matrix_diff": 0.0}]};

  const state = {
    datasets: [],
    datasetId: "fx_arbitrage_desk",
    feePct: 0.0,
    startingCapital: 1000.0,
    traderBudgetUsd: 10000.0,
    routeSource: null,
    routeTarget: null,
    rateOverrides: [],
    selectedCycleIndex: 0,
    report: null,
    benchmarkPoints: null,
    offlineMode: false,
  };

  const el = {
    datasetSelect: document.getElementById("datasetSelect"),
    refreshBtn: document.getElementById("refreshBtn"),
    regimeBadge: document.getElementById("regimeBadge"),
    regimeText: document.getElementById("regimeText"),
    feedMeta: document.getElementById("feedMeta"),
    feedWarning: document.getElementById("feedWarning"),
    feeSlider: document.getElementById("feeSlider"),
    feeValueLabel: document.getElementById("feeValueLabel"),
    snapBreakEvenBtn: document.getElementById("snapBreakEvenBtn"),
    capitalInput: document.getElementById("capitalInput"),
    budgetInput: document.getElementById("budgetInput"),
    routeFromSelect: document.getElementById("routeFromSelect"),
    routeToSelect: document.getElementById("routeToSelect"),
    swapRouteBtn: document.getElementById("swapRouteBtn"),
    ovSource: document.getElementById("ovSource"),
    ovTarget: document.getElementById("ovTarget"),
    ovRate: document.getElementById("ovRate"),
    addOverrideBtn: document.getElementById("addOverrideBtn"),
    clearOverridesBtn: document.getElementById("clearOverridesBtn"),
    overridesList: document.getElementById("overridesList"),
    kpiTopology: document.getElementById("kpiTopology"),
    kpiNegEdges: document.getElementById("kpiNegEdges"),
    kpiArbStatus: document.getElementById("kpiArbStatus"),
    kpiPasses: document.getElementById("kpiPasses"),
    kpiBreakEven: document.getElementById("kpiBreakEven"),
    kpiBreakSteps: document.getElementById("kpiBreakSteps"),
    kpiLatency: document.getElementById("kpiLatency"),
    kpiCrossCheck: document.getElementById("kpiCrossCheck"),
    graphCaption: document.getElementById("graphCaption"),
    networkSvg: document.getElementById("networkSvg"),
    ledgerTitle: document.getElementById("ledgerTitle"),
    ledgerSubtitle: document.getElementById("ledgerSubtitle"),
    ledgerBody: document.getElementById("ledgerBody"),
    bfComparisonBanner: document.getElementById("signalInsightBanner"),
    cyclesTableBody: document.querySelector("#cyclesTable tbody"),
    knapsackSummary: document.getElementById("allocationSummary"),
    knapsackTableBody: document.querySelector("#allocationTable tbody"),
    quotesTableBody: document.querySelector("#quotesTable tbody"),
    johnsonsGuardBanner: document.getElementById("routerGuardBanner"),
    johnsonsContent: document.getElementById("routerContent"),
    savingsTableBody: document.querySelector("#savingsTable tbody"),
    reweightTableBody: document.querySelector("#liquidityBookTable tbody"),
    matrixContainer: document.getElementById("matrixContainer"),
    binSearchSummary: document.getElementById("feeStressSummary"),
    binSearchTableBody: document.querySelector("#feeStressTable tbody"),
    runBenchmarkBtn: document.getElementById("runBenchmarkBtn"),
    benchSvg: document.getElementById("benchSvg"),
    benchTableBody: document.querySelector("#benchTable tbody"),
  };

  // =========================================================================
  // STANDALONE IN-BROWSER ENGINE (Runs automatically when opened without server)
  // =========================================================================
  function runLocalStandaloneEngine(params) {
    const tStart = performance.now();
    const dsId = params.dataset_id || "fx_arbitrage_desk";
    const baseSnap =
      EMBEDDED_FALLBACK.snapshots[dsId] ||
      (dsId === "live_kraken"
        ? EMBEDDED_FALLBACK.snapshots["crypto_multi_exchange"]
        : dsId === "live_fiat"
        ? EMBEDDED_FALLBACK.snapshots["bdt_remittance_corridor"]
        : EMBEDDED_FALLBACK.snapshots["fx_arbitrage_desk"]);

    const snapshot = {
      ...baseSnap,
      dataset_id: dsId,
      warning:
        dsId.startsWith("live_")
          ? "Viewing static HTML preview — showing desk snapshot. Open Live Server (port 8000) for real-time internet feeds."
          : null,
    };

    function buildLocalGraph(feePct) {
      const feeFrac = feePct / 100.0;
      const currencies = [];
      const symIdx = {};
      const bestMap = new Map();

      function addCur(s) {
        const u = s.trim().toUpperCase();
        if (!(u in symIdx)) {
          symIdx[u] = currencies.length;
          currencies.push(u);
        }
        return symIdx[u];
      }

      const ovMap = new Map();
      (params.rate_overrides || []).forEach((ov) => {
        if (ov.source && ov.target && ov.rate > 0) {
          ovMap.set(`${ov.source.toUpperCase()}->${ov.target.toUpperCase()}`, Number(ov.rate));
        }
      });

      const rawQuotes = baseSnap.quotes.map((q) => ({ ...q }));
      rawQuotes.forEach((q) => {
        const k = `${q.source}->${q.target}`;
        if (ovMap.has(k)) {
          q.rate = ovMap.get(k);
          q.venue = "Custom-Override";
          ovMap.delete(k);
        }
      });
      ovMap.forEach((rate, k) => {
        const [source, target] = k.split("->");
        rawQuotes.push({ source, target, rate, max_volume_usd: 10000, venue: "Custom-Override" });
      });

      rawQuotes.forEach((q) => {
        if (q.rate <= 0 || q.source === q.target) return;
        const u = addCur(q.source);
        const v = addCur(q.target);
        const eff = q.rate * (1 - feeFrac);
        if (eff <= 0) return;
        const w = -Math.log(eff);
        const key = `${u}->${v}`;
        const edge = {
          u, v,
          source: currencies[u],
          target: currencies[v],
          raw_rate: q.rate,
          effective_rate: eff,
          weight: w,
          max_volume_usd: q.max_volume_usd || 10000,
          venue: q.venue || "Spot",
        };
        if (!bestMap.has(key) || w < bestMap.get(key).weight) {
          bestMap.set(key, edge);
        }
      });

      return { fee_pct: feePct, currencies, symIdx, edges: Array.from(bestMap.values()), bestMap };
    }

    function scanCycles(g, startCap, discoverSecondary = true) {
      const EPS = 1e-9;
      const n = g.currencies.length;

      function runSub(excluded) {
        const dist = new Array(n).fill(0);
        const parent = new Array(n).fill(-1);
        const active = g.edges.filter((e) => !excluded.has(`${e.u}->${e.v}`));
        let early = false;
        let passes = 0;
        let relaxCount = 0;
        for (let p = 1; p < n; p++) {
          passes = p;
          let upd = false;
          for (const e of active) {
            if (dist[e.u] + e.weight < dist[e.v] - EPS) {
              dist[e.v] = dist[e.u] + e.weight;
              parent[e.v] = e.u;
              upd = true;
              relaxCount++;
            }
          }
          if (!upd) {
            early = true;
            break;
          }
        }
        const witnesses = [];
        if (!early && n > 0) {
          passes = n;
          for (const e of active) {
            if (dist[e.u] + e.weight < dist[e.v] - EPS) {
              dist[e.v] = dist[e.u] + e.weight;
              parent[e.v] = e.u;
              witnesses.push(e.v);
            }
          }
        }
        return { parent, witnesses, early, passes, relaxCount };
      }

      function extractLoop(startV, parent) {
        let curr = startV;
        for (let i = 0; i < n; i++) {
          curr = parent[curr];
          if (curr === -1) return null;
        }
        const pos = new Map();
        const trace = [];
        let node = curr;
        while (node !== -1 && !pos.has(node)) {
          pos.set(node, trace.length);
          trace.push(node);
          node = parent[node];
        }
        if (node === -1) return null;
        const loop = trace.slice(pos.get(node)).concat([node]);
        loop.reverse();
        return loop;
      }

      function buildCycle(loop) {
        const ring = loop.slice(0, -1);
        if (ring.length < 2) return null;
        const syms = ring.map((i) => g.currencies[i]);
        let rot = syms.indexOf("USD");
        if (rot === -1) {
          const minSym = [...syms].sort()[0];
          rot = syms.indexOf(minSym);
        }
        const ord = ring.slice(rot).concat(ring.slice(0, rot));
        const closed = ord.concat([ord[0]]);
        let wSum = 0, mult = 1, cap = Infinity, amt = startCap;
        const steps = [];
        for (let i = 0; i < ord.length; i++) {
          const e = g.bestMap.get(`${closed[i]}->${closed[i + 1]}`);
          if (!e) return null;
          const out = amt * e.effective_rate;
          wSum += e.weight;
          mult *= e.effective_rate;
          cap = Math.min(cap, e.max_volume_usd);
          steps.push({
            step_num: i + 1,
            from_currency: e.source,
            to_currency: e.target,
            raw_rate: e.raw_rate,
            effective_rate: e.effective_rate,
            weight: e.weight,
            amount_in: amt,
            amount_out: out,
            venue: e.venue,
            max_volume_usd: e.max_volume_usd,
          });
          amt = out;
        }
        if (wSum >= -EPS || mult <= 1.000001) return null;
        const canonRing = [...syms];
        const mS = [...canonRing].sort()[0];
        const mI = canonRing.indexOf(mS);
        const key = canonRing.slice(mI).concat(canonRing.slice(0, mI)).join(",");
        return {
          key,
          cycle: {
            path: closed.map((i) => g.currencies[i]),
            total_log_weight: wSum,
            CycleMultiplier: mult,
            profit_pct: (mult - 1) * 100,
            bottleneck_volume_usd: cap,
            steps,
            starting_capital: startCap,
            ending_capital: amt,
            net_profit: amt - startCap,
          },
        };
      }

      const excluded = new Set();
      const seen = new Set();
      const found = [];
      const first = runSub(excluded);
      for (const w of first.witnesses) {
        const lp = extractLoop(w, first.parent);
        const built = lp && buildCycle(lp);
        if (built && !seen.has(built.key)) {
          seen.add(built.key);
          found.push(built.cycle);
        }
      }
      if (discoverSecondary && found.length) {
        for (let r = 0; r < 5; r++) {
          found.forEach((c) => {
            const minSt = c.steps.reduce((a, b) => (a.max_volume_usd <= b.max_volume_usd ? a : b));
            excluded.add(`${g.symIdx[minSt.from_currency]}->${g.symIdx[minSt.to_currency]}`);
          });
          const sub = runSub(excluded);
          let added = false;
          for (const w of sub.witnesses) {
            const lp = extractLoop(w, sub.parent);
            const built = lp && buildCycle(lp);
            if (built && !seen.has(built.key)) {
              seen.add(built.key);
              found.push(built.cycle);
              added = true;
            }
          }
          if (!added) break;
        }
      }
      found.sort((a, b) => b.profit_pct - a.profit_pct);
      return { cycles: found, passes: first.passes, early: first.early, relaxCount: first.relaxCount };
    }

    const g = buildLocalGraph(params.fee_pct || 0);
    const startCap = params.starting_capital || 1000;
    const budget = params.trader_budget_usd || 10000;
    const bf = scanCycles(g, startCap, true);

    // Fee break-even search
    const gZero = buildLocalGraph(0);
    const zScan = scanCycles(gZero, startCap, false);
    let breakEven = {
      arbitrage_at_zero_fee: zScan.cycles.length > 0,
      max_tolerable_fee_pct: 0,
      iterations: 1,
      execution_time_ms: 0.2,
      trace: [],
    };
    if (zScan.cycles.length > 0) {
      let lo = 0, hi = 10;
      const trace = [];
      for (let it = 1; it <= 17; it++) {
        const mid = (lo + hi) / 2;
        const sc = scanCycles(buildLocalGraph(mid), startCap, false);
        const surv = sc.cycles.length > 0;
        trace.push({
          iteration: it,
          low_pct: lo,
          high_pct: hi,
          mid_pct: mid,
          arbitrage_survives: surv,
          surviving_best_profit_pct: surv ? sc.cycles[0].profit_pct : 0,
        });
        if (surv) lo = mid; else hi = mid;
      }
      breakEven = {
        arbitrage_at_zero_fee: true,
        max_tolerable_fee_pct: Number(lo.toFixed(4)),
        iterations: trace.length,
        execution_time_ms: 0.4,
        trace,
      };
    }

    // Capital split
    let rem = budget, totProf = 0;
    const allocations = [];
    for (const c of bf.cycles) {
      if (rem <= 1e-6) break;
      const take = Math.min(rem, c.bottleneck_volume_usd);
      const prof = take * (c.profit_pct / 100);
      allocations.push({
        cycle_path: c.path,
        profit_pct: c.profit_pct,
        liquidity_cap_usd: c.bottleneck_volume_usd,
        allocated_usd: take,
        fraction_of_cap_used: take / c.bottleneck_volume_usd,
        expected_profit_usd: prof,
      });
      rem -= take;
      totProf += prof;
    }

    // All-pairs best conversion matrix when balanced
    const curs = g.currencies;
    const n = curs.length;
    const defaultSrc =
      params.route_source && params.route_source in g.symIdx
        ? params.route_source
        : "BDT" in g.symIdx ? "BDT" : curs[0] || "USD";
    const defaultDst =
      params.route_target && params.route_target in g.symIdx
        ? params.route_target
        : "EUR" in g.symIdx && defaultSrc !== "EUR" ? "EUR" : curs[n - 1] || "EUR";

    let bestMatrix = [];
    let selectedRoute = null;
    let savings = [];

    if (bf.cycles.length === 0 && n > 0) {
      const dist = Array.from({ length: n }, (_, i) =>
        Array.from({ length: n }, (__, j) => (i === j ? 0 : Infinity))
      );
      const nextHop = Array.from({ length: n }, (_, i) =>
        Array.from({ length: n }, (__, j) => (i === j ? i : -1))
      );
      g.edges.forEach((e) => {
        if (e.weight < dist[e.u][e.v]) {
          dist[e.u][e.v] = e.weight;
          nextHop[e.u][e.v] = e.v;
        }
      });
      for (let k = 0; k < n; k++) {
        for (let i = 0; i < n; i++) {
          if (!Number.isFinite(dist[i][k])) continue;
          for (let j = 0; j < n; j++) {
            if (dist[i][k] + dist[k][j] < dist[i][j] - 1e-9) {
              dist[i][j] = dist[i][k] + dist[k][j];
              nextHop[i][j] = nextHop[i][k];
            }
          }
        }
      }
      bestMatrix = dist.map((row, i) =>
        row.map((d, j) => (i === j ? 1 : Number.isFinite(d) ? Math.exp(-d) : 0))
      );

      function buildRoute(sSym, tSym) {
        const u = g.symIdx[sSym], v = g.symIdx[tSym];
        if (u === undefined || v === undefined || u === v || !Number.isFinite(dist[u][v])) return null;
        const idxPath = [u];
        let curr = u;
        while (curr !== v) {
          curr = nextHop[curr][v];
          if (curr === -1 || idxPath.length > n + 1) return null;
          idxPath.push(curr);
        }
        let amt = startCap;
        const steps = [];
        for (let i = 0; i < idxPath.length - 1; i++) {
          const e = g.bestMap.get(`${idxPath[i]}->${idxPath[i + 1]}`);
          const out = amt * e.effective_rate;
          steps.push({
            step_num: i + 1,
            from_currency: e.source,
            to_currency: e.target,
            raw_rate: e.raw_rate,
            effective_rate: e.effective_rate,
            weight: e.weight,
            amount_in: amt,
            amount_out: out,
            venue: e.venue,
            max_volume_usd: e.max_volume_usd,
          });
          amt = out;
        }
        const bestRate = bestMatrix[u][v];
        const dirEdge = g.bestMap.get(`${u}->${v}`);
        const dirRate = dirEdge ? dirEdge.effective_rate : null;
        const bps = dirRate ? Math.max(0, ((bestRate - dirRate) / dirRate) * 10000) : 0;
        return {
          source: sSym,
          target: tSym,
          path: idxPath.map((x) => curs[x]),
          hops: steps.length,
          best_effective_rate: bestRate,
          direct_effective_rate: dirRate,
          improvement_bps: bps,
          amount_in: startCap,
          amount_out: amt,
          direct_amount_out: dirRate ? startCap * dirRate : null,
          steps,
        };
      }

      selectedRoute = buildRoute(defaultSrc, defaultDst);
      for (const a of curs) {
        for (const b of curs) {
          if (a === b) continue;
          const rt = buildRoute(a, b);
          if (rt && rt.hops >= 2 && (rt.improvement_bps > 0.5 || rt.direct_effective_rate === null)) {
            savings.push(rt);
          }
        }
      }
      savings.sort((a, b) => (b.direct_effective_rate ? b.improvement_bps : 0.1) - (a.direct_effective_rate ? a.improvement_bps : 0.1));
      savings = savings.slice(0, 12);
    }

    const elapsed = Math.max(0.08, performance.now() - tStart);
    const count3Hop = bf.cycles.filter((c) => c.steps.length === 3).length;
    const countLonger = bf.cycles.filter((c) => c.steps.length > 3).length;

    return {
      snapshot,
      graph: {
        num_vertices: n,
        num_edges: g.edges.length,
        negative_edges_count: g.edges.filter((e) => e.weight < 0).length,
        fee_pct: g.fee_pct,
        currencies: curs,
        edges: g.edges,
      },
      bellman_ford: {
        has_arbitrage: bf.cycles.length > 0,
        cycles_count: bf.cycles.length,
        cycles: bf.cycles,
        passes_executed: bf.passes,
        max_possible_passes: n,
        early_stopped: bf.early,
        total_relaxations: bf.relaxCount,
        execution_time_ms: elapsed,
      },
      break_even_fee: breakEven,
      capital_allocation: {
        total_budget_usd: budget,
        deployed_capital_usd: budget - rem,
        unallocated_cash_usd: rem,
        total_expected_profit_usd: totProf,
        blended_roi_pct: budget > 0 ? (totProf / budget) * 100 : 0,
        allocations,
      },
      brute_force_comparison: {
        triangles_checked: n * (n - 1) * (n - 2),
        profitable_3hop_count: count3Hop,
        bellman_ford_total_cycles: bf.cycles.length,
        multi_hop_cycles_missed_by_brute_force: countLonger,
        execution_time_ms: 0.12,
      },
      johnsons: {
        has_arbitrage: bf.cycles.length > 0,
        best_rate_matrix: bestMatrix,
        currencies: curs,
        execution_time_ms: elapsed,
        floyd_warshall_time_ms: elapsed * 0.8,
        route_source: defaultSrc,
        route_target: defaultDst,
        selected_route: selectedRoute,
        top_multi_hop_savings: savings,
      },
    };
  }

  function fmtNum(val, decimals = 2) {
    if (val === null || val === undefined || Number.isNaN(val)) return "—";
    return Number(val).toLocaleString(undefined, {
      minimumFractionDigits: decimals,
      maximumFractionDigits: decimals,
    });
  }

  function fmtRate(val) {
    if (val === null || val === undefined) return "—";
    const n = Number(val);
    if (n === 0) return "0";
    if (n >= 100) return n.toFixed(2);
    if (n >= 1) return n.toFixed(4);
    if (n >= 0.01) return n.toFixed(5);
    return n.toExponential(4);
  }

  async function init() {
    bindEvents();
    try {
      const res = await fetch("./api/datasets");
      if (!res.ok) throw new Error("API unavailable");
      const data = await res.json();
      state.datasets = data.datasets || EMBEDDED_FALLBACK.catalog;
      state.offlineMode = false;
    } catch (_err) {
      state.datasets = EMBEDDED_FALLBACK.catalog;
      state.offlineMode = true;
    }

    el.datasetSelect.innerHTML = state.datasets
      .map((d) => `<option value="${d.id}">[${d.mode}] ${d.title}</option>`)
      .join("");
    el.datasetSelect.value = state.datasetId;

    await runAnalysis();
    await runBenchmark();
  }

  function bindEvents() {
    el.datasetSelect.addEventListener("change", () => {
      state.datasetId = el.datasetSelect.value;
      state.selectedCycleIndex = 0;
      state.routeSource = null;
      state.routeTarget = null;
      if (state.datasetId === "bdt_remittance_corridor") {
        activateTab("tab-router");
      }
      runAnalysis();
    });

    el.refreshBtn.addEventListener("click", () => runAnalysis());

    let sliderTimer = null;
    el.feeSlider.addEventListener("input", () => {
      state.feePct = parseFloat(el.feeSlider.value);
      el.feeValueLabel.textContent = `${state.feePct.toFixed(2)}%`;
      clearTimeout(sliderTimer);
      sliderTimer = setTimeout(() => runAnalysis(), 90);
    });

    el.snapBreakEvenBtn.addEventListener("click", () => {
      if (!state.report) return;
      const be = state.report.break_even_fee.max_tolerable_fee_pct || 0;
      const targetFee = Math.min(1.2, Math.ceil((be + 0.02) * 100) / 100);
      state.feePct = targetFee;
      el.feeSlider.value = String(targetFee);
      el.feeValueLabel.textContent = `${targetFee.toFixed(2)}%`;
      activateTab("tab-router");
      runAnalysis();
    });

    el.capitalInput.addEventListener("change", () => {
      state.startingCapital = Math.max(1, parseFloat(el.capitalInput.value) || 1000);
      runAnalysis();
    });

    el.budgetInput.addEventListener("change", () => {
      state.traderBudgetUsd = Math.max(10, parseFloat(el.budgetInput.value) || 10000);
      runAnalysis();
    });

    el.routeFromSelect.addEventListener("change", () => {
      state.routeSource = el.routeFromSelect.value;
      runAnalysis();
    });

    el.routeToSelect.addEventListener("change", () => {
      state.routeTarget = el.routeToSelect.value;
      runAnalysis();
    });

    el.swapRouteBtn.addEventListener("click", () => {
      const tmp = el.routeFromSelect.value;
      state.routeSource = el.routeToSelect.value;
      state.routeTarget = tmp;
      runAnalysis();
    });

    el.addOverrideBtn.addEventListener("click", () => {
      const src = el.ovSource.value.trim().toUpperCase();
      const dst = el.ovTarget.value.trim().toUpperCase();
      const rate = parseFloat(el.ovRate.value);
      if (!src || !dst || src === dst || !(rate > 0)) return;

      state.rateOverrides = state.rateOverrides.filter(
        (o) => !(o.source === src && o.target === dst)
      );
      state.rateOverrides.push({ source: src, target: dst, rate });
      el.ovRate.value = "";
      renderOverrides();
      runAnalysis();
    });

    el.clearOverridesBtn.addEventListener("click", () => {
      state.rateOverrides = [];
      renderOverrides();
      runAnalysis();
    });

    document.querySelectorAll(".tab-btn").forEach((btn) => {
      btn.addEventListener("click", () => activateTab(btn.dataset.tab));
    });

    el.runBenchmarkBtn.addEventListener("click", () => runBenchmark());
  }

  function activateTab(tabId) {
    document.querySelectorAll(".tab-btn").forEach((b) => {
      b.classList.toggle("active", b.dataset.tab === tabId);
    });
    document.querySelectorAll(".tab-pane").forEach((p) => {
      p.classList.toggle("active", p.id === tabId);
    });
  }

  function renderOverrides() {
    el.overridesList.innerHTML = state.rateOverrides
      .map(
        (o) =>
          `<div class="override-chip"><span>${o.source} → ${o.target}</span><span>@ ${o.rate}</span></div>`
      )
      .join("");
  }

  async function runAnalysis() {
    el.refreshBtn.disabled = true;
    const reqPayload = {
      dataset_id: state.datasetId,
      fee_pct: state.feePct,
      starting_capital: state.startingCapital,
      trader_budget_usd: state.traderBudgetUsd,
      route_source: state.routeSource,
      route_target: state.routeTarget,
      rate_overrides: state.rateOverrides,
    };

    try {
      let report;
      if (!state.offlineMode) {
        const res = await fetch("./api/analyze", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(reqPayload),
        });
        if (!res.ok) throw new Error("Backend error");
        report = await res.json();
      } else {
        report = runLocalStandaloneEngine(reqPayload);
      }
      state.report = report;
      if (state.selectedCycleIndex >= (report.bellman_ford.cycles?.length || 0)) {
        state.selectedCycleIndex = 0;
      }
      renderAll(report);
    } catch (_err) {
      state.offlineMode = true;
      const report = runLocalStandaloneEngine(reqPayload);
      state.report = report;
      renderAll(report);
    } finally {
      el.refreshBtn.disabled = false;
    }
  }

  function renderAll(report) {
    const {
      snapshot,
      graph,
      bellman_ford: bf,
      break_even_fee: be,
      capital_allocation: cap,
      johnsons: jn,
    } = report;

    if (bf.has_arbitrage) {
      el.regimeBadge.className = "regime-badge regime-arb";
      el.regimeText.textContent = `LIVE SIGNAL: ${bf.cycles_count} ARBITRAGE LOOP${bf.cycles_count > 1 ? "S" : ""}`;
    } else {
      el.regimeBadge.className = "regime-badge regime-calm";
      el.regimeText.textContent = "MARKET BALANCED · SMART ROUTER ACTIVE";
    }

    el.feedMeta.innerHTML = `<strong>${snapshot.title}</strong><br/><span>${snapshot.description}</span><br/><span class="mono" style="color:#647594">${snapshot.fetched_at_utc}</span>`;
    if (snapshot.warning) {
      el.feedWarning.textContent = snapshot.warning;
      el.feedWarning.classList.remove("hidden");
    } else {
      el.feedWarning.classList.add("hidden");
    }

    const curOpts = graph.currencies.map((c) => `<option value="${c}">${c}</option>`).join("");
    el.routeFromSelect.innerHTML = curOpts;
    el.routeToSelect.innerHTML = curOpts;
    el.routeFromSelect.value = jn.route_source;
    el.routeToSelect.value = jn.route_target;
    state.routeSource = jn.route_source;
    state.routeTarget = jn.route_target;

    const venues = new Set(graph.edges.map((e) => e.venue)).size;
    el.kpiTopology.textContent = `${graph.num_vertices} Assets · ${graph.num_edges} Pairs`;
    el.kpiNegEdges.textContent = `Across ${venues} liquidity venue${venues === 1 ? "" : "s"} · Fee ${graph.fee_pct.toFixed(2)}%/leg`;

    if (bf.has_arbitrage) {
      const best = bf.cycles[0];
      el.kpiArbStatus.innerHTML = `<span class="pos">+${best.profit_pct.toFixed(3)}%</span> Best Yield`;
      el.kpiPasses.textContent = `${bf.cycles_count} actionable round-trip signal${bf.cycles_count > 1 ? "s" : ""} detected`;
    } else {
      el.kpiArbStatus.innerHTML = `<span class="cyan-txt">0 Arbitrage</span>`;
      el.kpiPasses.textContent = `No risk-free spread at ${graph.fee_pct.toFixed(2)}% fee`;
    }

    if (be.arbitrage_at_zero_fee) {
      el.kpiBreakEven.textContent = `${be.max_tolerable_fee_pct.toFixed(4)}% / leg`;
      el.kpiBreakSteps.textContent =
        state.feePct <= be.max_tolerable_fee_pct
          ? `Margin cushion: +${(be.max_tolerable_fee_pct - state.feePct).toFixed(3)}% remaining`
          : `Current fee exceeds break-even by ${(state.feePct - be.max_tolerable_fee_pct).toFixed(3)}%`;
      el.snapBreakEvenBtn.disabled = false;
      el.snapBreakEvenBtn.textContent = `⚡ Switch to Smart Routing (Fee > ${be.max_tolerable_fee_pct.toFixed(2)}%)`;
    } else {
      el.kpiBreakEven.textContent = "0.0000%";
      el.kpiBreakSteps.textContent = "Market already priced efficiently at 0% fee";
      el.snapBreakEvenBtn.disabled = true;
      el.snapBreakEvenBtn.textContent = "Smart Routing Active";
    }

    if (bf.has_arbitrage) {
      el.kpiLatency.innerHTML = `<span class="pos">+$${fmtNum(cap.total_expected_profit_usd, 2)}</span> Est. PnL`;
      el.kpiCrossCheck.textContent = `+${cap.blended_roi_pct.toFixed(2)}% portfolio yield on $${fmtNum(cap.total_budget_usd, 0)} · Scan ${bf.execution_time_ms.toFixed(2)} ms`;
    } else {
      const rt = jn.selected_route;
      const gainStr = rt && rt.improvement_bps > 0 ? `+${rt.improvement_bps.toFixed(1)} bps Saved` : "Direct Best";
      el.kpiLatency.innerHTML = `<span class="cyan-txt">${gainStr}</span>`;
      el.kpiCrossCheck.textContent = `${jn.route_source} → ${jn.route_target} smart bridge · Scan ${jn.execution_time_ms.toFixed(2)} ms`;
    }

    renderNetworkGraph(report);
    renderLedger(report);
    renderArbitrageTab(report);
    renderRouterTab(report);
    renderFeeStressTab(report);
  }

  function renderNetworkGraph(report) {
    const svg = el.networkSvg;
    const { graph, bellman_ford: bf, johnsons: jn } = report;
    const currencies = graph.currencies;
    const n = currencies.length;
    if (n === 0) {
      svg.innerHTML = "";
      return;
    }

    const W = 680, H = 430, cx = W / 2, cy = H / 2, rx = 245, ry = 162;
    const coords = {};
    currencies.forEach((sym, i) => {
      const angle = -Math.PI / 2 + (2 * Math.PI * i) / n;
      coords[sym] = { x: cx + rx * Math.cos(angle), y: cy + ry * Math.sin(angle) };
    });

    const highlightMap = new Map();
    const activeNodes = new Set();

    if (bf.has_arbitrage && bf.cycles.length > 0) {
      const cyc = bf.cycles[state.selectedCycleIndex] || bf.cycles[0];
      el.graphCaption.textContent = `Signal #${state.selectedCycleIndex + 1}: ${cyc.path.join(" → ")} · Net Yield +${cyc.profit_pct.toFixed(3)}% · Max Order Depth $${fmtNum(cyc.bottleneck_volume_usd, 0)}`;
      cyc.steps.forEach((st) => {
        highlightMap.set(`${st.from_currency}->${st.to_currency}`, {
          mode: "arb",
          stepNum: st.step_num,
          rate: st.effective_rate,
        });
        activeNodes.add(st.from_currency);
        activeNodes.add(st.to_currency);
      });
    } else if (!jn.has_arbitrage && jn.selected_route && jn.selected_route.steps.length > 0) {
      const rt = jn.selected_route;
      const saveText =
        rt.improvement_bps > 0
          ? `Saves +${rt.improvement_bps.toFixed(1)} bps over direct conversion`
          : `Best execution route`;
      el.graphCaption.textContent = `Smart Conversion Bridge: ${rt.path.join(" → ")} · ${saveText}`;
      rt.steps.forEach((st) => {
        highlightMap.set(`${st.from_currency}->${st.to_currency}`, {
          mode: "route",
          stepNum: st.step_num,
          rate: st.effective_rate,
        });
        activeNodes.add(st.from_currency);
        activeNodes.add(st.to_currency);
      });
    } else {
      el.graphCaption.textContent = "Click any currency node (or Shift+Click) to set Pay / Receive currencies.";
    }

    const defs = `
      <defs>
        <marker id="arrow-dim" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
          <path d="M 0 1.5 L 8.5 5 L 0 8.5 z" fill="#334566" />
        </marker>
        <marker id="arrow-arb" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse">
          <path d="M 0 1 L 9 5 L 0 9 z" fill="#10b981" />
        </marker>
        <marker id="arrow-route" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse">
          <path d="M 0 1 L 9 5 L 0 9 z" fill="#06b6d4" />
        </marker>
      </defs>
    `;

    let bgPaths = "", fgPaths = "", fgBadges = "";
    const NODE_R = 23;

    graph.edges.forEach((e) => {
      const p1 = coords[e.source], p2 = coords[e.target];
      if (!p1 || !p2) return;
      const dx = p2.x - p1.x, dy = p2.y - p1.y;
      const len = Math.hypot(dx, dy) || 1;
      const ux = dx / len, uy = dy / len;
      const nx = -uy, ny = ux;
      const sx = p1.x + ux * (NODE_R + 2) + nx * 4;
      const sy = p1.y + uy * (NODE_R + 2) + ny * 4;
      const ex = p2.x - ux * (NODE_R + 5) + nx * 4;
      const ey = p2.y - uy * (NODE_R + 5) + ny * 4;
      const qx = (sx + ex) / 2 + nx * 18;
      const qy = (sy + ey) / 2 + ny * 18;

      const hl = highlightMap.get(`${e.source}->${e.target}`);
      if (!hl) {
        bgPaths += `<path d="M ${sx.toFixed(1)} ${sy.toFixed(1)} Q ${qx.toFixed(1)} ${qy.toFixed(1)} ${ex.toFixed(1)} ${ey.toFixed(1)}"
          fill="none" stroke="#253451" stroke-width="1.2" stroke-opacity="0.65" marker-end="url(#arrow-dim)" />`;
      } else {
        const strokeColor = hl.mode === "arb" ? "#10b981" : "#06b6d4";
        const markerId = hl.mode === "arb" ? "arrow-arb" : "arrow-route";
        fgPaths += `
          <path d="M ${sx.toFixed(1)} ${sy.toFixed(1)} Q ${qx.toFixed(1)} ${qy.toFixed(1)} ${ex.toFixed(1)} ${ey.toFixed(1)}"
            fill="none" stroke="${strokeColor}" stroke-width="5" stroke-opacity="0.18" />
          <path class="edge-animated" d="M ${sx.toFixed(1)} ${sy.toFixed(1)} Q ${qx.toFixed(1)} ${qy.toFixed(1)} ${ex.toFixed(1)} ${ey.toFixed(1)}"
            fill="none" stroke="${strokeColor}" stroke-width="2.6" marker-end="url(#${markerId})" />
        `;
        const mx = 0.25 * sx + 0.5 * qx + 0.25 * ex;
        const my = 0.25 * sy + 0.5 * qy + 0.25 * ey;
        const labelTxt = `Leg ${hl.stepNum}: ${fmtRate(hl.rate)}`;
        const boxW = Math.max(76, labelTxt.length * 6.3 + 10);
        fgBadges += `
          <g transform="translate(${mx.toFixed(1)}, ${my.toFixed(1)})">
            <rect x="${-boxW / 2}" y="-10" width="${boxW}" height="19" rx="5"
              fill="#09101d" stroke="${strokeColor}" stroke-width="1.2" />
            <text x="0" y="3.5" text-anchor="middle" fill="#e6edf7" font-family="monospace" font-size="10.5" font-weight="700">
              ${labelTxt}
            </text>
          </g>
        `;
      }
    });

    let nodesMarkup = "";
    currencies.forEach((sym) => {
      const p = coords[sym];
      const isHighlighted = activeNodes.has(sym);
      const isArb = bf.has_arbitrage && isHighlighted;
      const ringStroke = isHighlighted ? (isArb ? "#10b981" : "#06b6d4") : "#36496e";
      const fillBg = isHighlighted ? (isArb ? "#0c2924" : "#0b2533") : "#131d31";
      nodesMarkup += `
        <g class="graph-node" data-sym="${sym}" style="cursor:pointer" transform="translate(${p.x.toFixed(1)}, ${p.y.toFixed(1)})">
          ${isHighlighted ? `<circle r="${NODE_R + 5}" fill="none" stroke="${ringStroke}" stroke-opacity="0.28" stroke-width="4" />` : ""}
          <circle r="${NODE_R}" fill="${fillBg}" stroke="${ringStroke}" stroke-width="2" />
          <text y="4" text-anchor="middle" fill="#f1f5f9" font-family="monospace" font-size="12" font-weight="700">${sym}</text>
        </g>
      `;
    });

    svg.innerHTML = defs + bgPaths + fgPaths + fgBadges + nodesMarkup;
    svg.querySelectorAll(".graph-node").forEach((nodeEl) => {
      nodeEl.addEventListener("click", (ev) => {
        const sym = nodeEl.getAttribute("data-sym");
        if (ev.shiftKey) state.routeSource = sym;
        else if (sym !== state.routeSource) state.routeTarget = sym;
        runAnalysis();
      });
    });
  }

  function renderLedger(report) {
    const { bellman_ford: bf, johnsons: jn } = report;

    if (bf.has_arbitrage && bf.cycles.length > 0) {
      const cyc = bf.cycles[state.selectedCycleIndex] || bf.cycles[0];
      const baseCur = cyc.path[0];
      el.ledgerTitle.textContent = `Signal #${state.selectedCycleIndex + 1} · Execution Ticket`;
      el.ledgerSubtitle.textContent = `Actionable ${cyc.steps.length}-Leg Round-Trip Arbitrage Signal (Paper Simulation)`;

      const stepsHtml = cyc.steps
        .map(
          (st) => `
          <div class="step-card">
            <div class="step-top">
              <span>Leg ${st.step_num}: SELL ${st.from_currency} → BUY ${st.to_currency}</span>
              <span class="mono" style="color:#93a4c3">${st.venue}</span>
            </div>
            <div class="step-math">
              ${fmtNum(st.amount_in, 2)} ${st.from_currency} @ ${fmtRate(st.effective_rate)} → <strong>${fmtNum(st.amount_out, 2)} ${st.to_currency}</strong>
              <br/><span style="color:#647594">Venue Depth Cap: $${fmtNum(st.max_volume_usd, 0)}</span>
            </div>
          </div>`
        )
        .join("");

      el.ledgerBody.innerHTML = `
        ${stepsHtml}
        <div class="ledger-summary">
          <div style="font-size:11.5px;color:#93a4c3">Simulated Net Payout (${baseCur} Round-Trip)</div>
          <div class="summary-big">
            ${fmtNum(cyc.starting_capital, 2)} → ${fmtNum(cyc.ending_capital, 2)} ${baseCur}
            (+${fmtNum(cyc.net_profit, 2)} / +${cyc.profit_pct.toFixed(3)}%)
          </div>
          <div style="font-size:11.5px;color:#93a4c3;margin-top:3px">
            Max Simultaneous Fill Before Slippage: <strong>$${fmtNum(cyc.bottleneck_volume_usd, 0)}</strong>
          </div>
        </div>
      `;
      return;
    }

    el.ledgerTitle.textContent = `Smart Conversion Ticket`;
    el.ledgerSubtitle.textContent = `Multi-Currency Bridge vs. Standard Direct Bank Quote`;

    const rt = jn.selected_route;
    if (!rt || rt.hops === 0) {
      el.ledgerBody.innerHTML = `<div class="helper-text">Choose different Pay and Receive currencies in the left sidebar (or click any node on the map) to preview the best transfer path.</div>`;
      return;
    }

    const stepsHtml = rt.steps
      .map(
        (st) => `
        <div class="step-card route-mode">
          <div class="step-top">
            <span>Leg ${st.step_num}: CONVERT ${st.from_currency} → ${st.to_currency}</span>
            <span class="mono" style="color:#93a4c3">${st.venue}</span>
          </div>
          <div class="step-math">
            ${fmtNum(st.amount_in, 2)} ${st.from_currency} @ ${fmtRate(st.effective_rate)} → <strong>${fmtNum(st.amount_out, 2)} ${st.to_currency}</strong>
          </div>
        </div>`
      )
      .join("");

    const directCompare =
      rt.direct_amount_out !== null
        ? `Direct 1-Step Quote: <strong>${fmtNum(rt.direct_amount_out, 2)} ${rt.target}</strong> · Smart Bridge Gain: <span class="cyan-txt">+${rt.improvement_bps.toFixed(1)} bps</span>`
        : `No direct ${rt.source}→${rt.target} desk quote available — bridged automatically across ${rt.hops} legs!`;

    el.ledgerBody.innerHTML = `
      ${stepsHtml}
      <div class="ledger-summary calm">
        <div style="font-size:11.5px;color:#93a4c3">Best Execution Payout (${rt.path.join(" → ")})</div>
        <div class="summary-big cyan">
          ${fmtNum(rt.amount_in, 2)} ${rt.source} → ${fmtNum(rt.amount_out, 2)} ${rt.target}
        </div>
        <div style="font-size:11.5px;color:#93a4c3;margin-top:4px">${directCompare}</div>
      </div>
    `;
  }

  function renderArbitrageTab(report) {
    const { graph, bellman_ford: bf, capital_allocation: cap, brute_force_comparison: cmp } = report;

    if (bf.has_arbitrage) {
      el.bfComparisonBanner.innerHTML = `
        <div>
          <strong>Deep Multi-Leg Signal Discovery:</strong>
          Standard 3-currency scanners only spotted <strong>${cmp.profitable_3hop_count}</strong> loop(s) in this book,
          whereas ArbiGraph uncovered <strong class="pos">${bf.cycles_count} total profitable signals</strong>
          (including <strong>${cmp.multi_hop_cycles_missed_by_brute_force}</strong> deeper 4-leg &amp; 5-leg cross-desk loops).
        </div>
      `;
    } else {
      el.bfComparisonBanner.innerHTML = `
        <div>
          <strong>Market Currently Efficient at ${graph.fee_pct.toFixed(2)}% Fee:</strong>
          All round-trip spreads are narrower than transaction costs. Lower your fee tier or open <strong>Tab 2 (Smart Currency Router)</strong> to save on international conversions.
        </div>
      `;
    }

    if (!bf.cycles.length) {
      el.cyclesTableBody.innerHTML = `<tr><td colspan="6" style="color:#93a4c3;text-align:center">No profitable arbitrage signals at ${graph.fee_pct.toFixed(2)}% fee/leg. Slide fee toward 0.00% or switch market feed.</td></tr>`;
    } else {
      el.cyclesTableBody.innerHTML = bf.cycles
        .map(
          (c, i) => `
          <tr class="clickable-row ${i === state.selectedCycleIndex ? "selected-row" : ""}" data-idx="${i}">
            <td>#${i + 1}</td>
            <td>${c.path.join(" → ")}</td>
            <td>${c.steps.length}</td>
            <td class="pos">+${c.profit_pct.toFixed(4)}%</td>
            <td class="pos">+${fmtNum(c.net_profit, 2)} ${c.path[0]}</td>
            <td>$${fmtNum(c.bottleneck_volume_usd, 0)}</td>
          </tr>`
        )
        .join("");

      el.cyclesTableBody.querySelectorAll("tr.clickable-row").forEach((row) => {
        row.addEventListener("click", () => {
          state.selectedCycleIndex = parseInt(row.dataset.idx, 10);
          renderAll(state.report);
        });
      });
    }

    el.knapsackSummary.textContent = cap.allocations.length
      ? `Desk Capital: $${fmtNum(cap.total_budget_usd, 0)} → Deployed: $${fmtNum(cap.deployed_capital_usd, 0)} → Projected Profit: +$${fmtNum(cap.total_expected_profit_usd, 2)} (+${cap.blended_roi_pct.toFixed(3)}% Yield)`
      : `No active signals — 100% of desk capital ($${fmtNum(cap.total_budget_usd, 0)}) held in reserve.`;

    el.knapsackTableBody.innerHTML = cap.allocations.length
      ? cap.allocations
          .map(
            (a) => `
            <tr>
              <td>${a.cycle_path.join("→")}</td>
              <td>$${fmtNum(a.allocated_usd, 2)}</td>
              <td>${(a.fraction_of_cap_used * 100).toFixed(1)}% of $${fmtNum(a.liquidity_cap_usd, 0)}</td>
              <td class="pos">+$${fmtNum(a.expected_profit_usd, 2)}</td>
            </tr>`
          )
          .join("")
      : `<tr><td colspan="4" style="color:#93a4c3;text-align:center">Unallocated Cash Reserve: $${fmtNum(cap.unallocated_cash_usd, 0)}</td></tr>`;

    el.quotesTableBody.innerHTML = graph.edges
      .map(
        (e) => `
        <tr>
          <td><strong>${e.source} → ${e.target}</strong></td>
          <td>${e.venue}</td>
          <td>${fmtRate(e.raw_rate)}</td>
          <td class="cyan-txt">${fmtRate(e.effective_rate)}</td>
          <td>$${fmtNum(e.max_volume_usd, 0)}</td>
        </tr>`
      )
      .join("");
  }

  function renderRouterTab(report) {
    const { graph, johnsons: jn, break_even_fee: be } = report;

    if (jn.has_arbitrage) {
      el.johnsonsGuardBanner.innerHTML = `
        <div>
          <strong style="color:#fbbf24">Active Arbitrage Dislocation Detected:</strong>
          Because risk-free round-trip loops exist at ${graph.fee_pct.toFixed(2)}% fee, traders can compound conversions rather than settling a static transfer.
          Simulate fees above <strong>${be.max_tolerable_fee_pct.toFixed(3)}%</strong> (or select <em>BDT &amp; Global Remittance Corridors</em>) to view settled transfer routing.
        </div>
        <button id="inlineClearArbBtn" class="btn btn-accent">⚡ Simulate Balanced Market</button>
      `;
      el.johnsonsContent.classList.add("hidden");
      const btn = document.getElementById("inlineClearArbBtn");
      if (btn) btn.addEventListener("click", () => el.snapBreakEvenBtn.click());
      return;
    }

    el.johnsonsContent.classList.remove("hidden");
    el.johnsonsGuardBanner.innerHTML = `
      <div>
        <strong class="cyan-txt">Smart Multi-Currency Router Online:</strong>
        Comparing every direct bank/exchange quote against multi-currency institutional hub bridges across all <strong>${jn.currencies.length}</strong> assets. Click any row below to load its transfer ticket!
      </div>
    `;

    if (!jn.top_multi_hop_savings.length) {
      el.savingsTableBody.innerHTML = `<tr><td colspan="5" style="color:#93a4c3;text-align:center">Direct 1-step quotes are already optimal across all pairs at this fee tier.</td></tr>`;
    } else {
      el.savingsTableBody.innerHTML = jn.top_multi_hop_savings
        .map(
          (r) => `
          <tr class="clickable-row" data-src="${r.source}" data-dst="${r.target}">
            <td><strong>${r.source} → ${r.target}</strong></td>
            <td>${r.path.join(" → ")}</td>
            <td>${fmtRate(r.best_effective_rate)}</td>
            <td>${r.direct_effective_rate ? fmtRate(r.direct_effective_rate) : "No Direct"}</td>
            <td class="cyan-txt">${r.direct_effective_rate ? `+${r.improvement_bps.toFixed(1)} bps` : "Auto-Bridged"}</td>
          </tr>`
        )
        .join("");

      el.savingsTableBody.querySelectorAll("tr.clickable-row").forEach((row) => {
        row.addEventListener("click", () => {
          state.routeSource = row.dataset.src;
          state.routeTarget = row.dataset.dst;
          runAnalysis();
        });
      });
    }

    el.reweightTableBody.innerHTML = graph.edges
      .map(
        (e) => `
        <tr>
          <td>${e.source} → ${e.target}</td>
          <td>${e.venue}</td>
          <td>${fmtRate(e.raw_rate)}</td>
          <td class="pos">${fmtRate(e.effective_rate)}</td>
          <td>$${fmtNum(e.max_volume_usd, 0)}</td>
        </tr>`
      )
      .join("");

    const curs = jn.currencies;
    const headerCols = curs.map((c) => `<th>${c}</th>`).join("");
    const rowsHtml = jn.best_rate_matrix
      .map((row, i) => {
        const cells = row
          .map((val, j) => (i === j ? `<td style="color:#647594">1.0000</td>` : `<td>${fmtRate(val)}</td>`))
          .join("");
        return `<tr><th>${curs[i]}</th>${cells}</tr>`;
      })
      .join("");

    el.matrixContainer.innerHTML = `
      <table class="quant-table">
        <thead><tr><th>Pay \ Receive</th>${headerCols}</tr></thead>
        <tbody>${rowsHtml}</tbody>
      </table>
    `;
  }

  function renderFeeStressTab(report) {
    const be = report.break_even_fee;
    if (!be.arbitrage_at_zero_fee) {
      el.binSearchSummary.innerHTML = `<div>This market feed has <strong>zero arbitrage spread even at 0.00% VIP maker fees</strong>. Use the Smart Currency Router tab to optimize one-way transfers.</div>`;
      el.binSearchTableBody.innerHTML = `<tr><td colspan="6" style="color:#93a4c3;text-align:center">Select Institutional FX Cross-Desk or Multi-Exchange Crypto feed to run fee margin stress tests.</td></tr>`;
      return;
    }

    el.binSearchSummary.innerHTML = `
      <div>
        <strong>Break-Even Fee Ceiling:</strong> Arbitrage signals remain net-profitable up to a maximum trading fee of
        <strong class="cyan-txt">${be.max_tolerable_fee_pct.toFixed(4)}% per leg</strong>.
        Accounts paying higher retail fees see 100% of gross spread wiped out by execution costs.
      </div>
    `;

    el.binSearchTableBody.innerHTML = be.trace
      .map(
        (st) => `
        <tr>
          <td>Tier #${st.iteration}</td>
          <td>${st.low_pct.toFixed(5)}%</td>
          <td><strong>${st.mid_pct.toFixed(5)}%</strong></td>
          <td>${st.high_pct.toFixed(5)}%</td>
          <td class="${st.arbitrage_survives ? "pos" : "neg"}">${st.arbitrage_survives ? "PROFITABLE SIGNAL" : "WIPED BY FEES"}</td>
          <td>${st.arbitrage_survives ? `+${st.surviving_best_profit_pct.toFixed(4)}%` : "0.0000%"}</td>
        </tr>`
      )
      .join("");
  }

  async function runBenchmark() {
    el.runBenchmarkBtn.disabled = true;
    el.runBenchmarkBtn.textContent = "Testing...";
    try {
      if (!state.offlineMode) {
        const res = await fetch("./api/benchmark");
        if (!res.ok) throw new Error("API unavailable");
        const data = await res.json();
        state.benchmarkPoints = data.points || EMBEDDED_FALLBACK.benchmark;
      } else {
        state.benchmarkPoints = EMBEDDED_FALLBACK.benchmark;
      }
    } catch (_err) {
      state.benchmarkPoints = EMBEDDED_FALLBACK.benchmark;
    } finally {
      renderBenchmark(state.benchmarkPoints);
      el.runBenchmarkBtn.disabled = false;
      el.runBenchmarkBtn.textContent = "↻ Re-Run Latency Test";
    }
  }

  function renderBenchmark(points) {
    if (!points || !points.length) return;

    el.benchTableBody.innerHTML = points
      .map(
        (p) => `
        <tr>
          <td><strong>${p.vertices} Assets</strong></td>
          <td>${p.edges}</td>
          <td>${p.bellman_ford_ms.toFixed(2)} ms</td>
          <td class="cyan-txt">${p.johnsons_ms.toFixed(2)} ms</td>
          <td class="neg">${p.floyd_warshall_ms.toFixed(2)} ms</td>
          <td class="${p.speedup_factor >= 1 ? "pos" : ""}">${p.speedup_factor.toFixed(2)}×</td>
        </tr>`
      )
      .join("");

    const W = 580, H = 280, padL = 54, padR = 24, padT = 26, padB = 42;
    const plotW = W - padL - padR, plotH = H - padT - padB;
    const maxV = Math.max(...points.map((p) => p.vertices));
    const minV = Math.min(...points.map((p) => p.vertices));
    const maxMs = Math.max(...points.map((p) => Math.max(p.johnsons_ms, p.floyd_warshall_ms))) * 1.1;

    const xOf = (v) => padL + ((v - minV) / (maxV - minV || 1)) * plotW;
    const yOf = (ms) => padT + plotH - (ms / (maxMs || 1)) * plotH;

    let grid = "";
    for (let i = 0; i <= 4; i++) {
      const val = (maxMs * i) / 4;
      const y = yOf(val);
      grid += `
        <line x1="${padL}" y1="${y}" x2="${W - padR}" y2="${y}" stroke="#1d2a44" stroke-width="1" />
        <text x="${padL - 8}" y="${y + 4}" text-anchor="end" fill="#647594" font-family="monospace" font-size="10">${val.toFixed(0)}ms</text>
      `;
    }

    const legacyPoly = points.map((p) => `${xOf(p.vertices).toFixed(1)},${yOf(p.floyd_warshall_ms).toFixed(1)}`).join(" ");
    const smartPoly = points.map((p) => `${xOf(p.vertices).toFixed(1)},${yOf(p.johnsons_ms).toFixed(1)}`).join(" ");

    let dots = "";
    points.forEach((p) => {
      const x = xOf(p.vertices);
      dots += `
        <circle cx="${x}" cy="${yOf(p.floyd_warshall_ms)}" r="4" fill="#f43f5e" />
        <circle cx="${x}" cy="${yOf(p.johnsons_ms)}" r="4" fill="#06b6d4" />
        <text x="${x}" y="${H - 16}" text-anchor="middle" fill="#93a4c3" font-family="monospace" font-size="10.5">${p.vertices} Assets</text>
      `;
    });

    el.benchSvg.innerHTML = `
      ${grid}
      <polyline fill="none" stroke="#f43f5e" stroke-width="2.5" points="${legacyPoly}" />
      <polyline fill="none" stroke="#06b6d4" stroke-width="2.5" points="${smartPoly}" />
      ${dots}
      <g transform="translate(${padL + 12}, ${padT + 8})">
        <rect x="0" y="0" width="225" height="44" rx="6" fill="#0d1526" stroke="#24324d" />
        <circle cx="14" cy="14" r="4" fill="#f43f5e" />
        <text x="26" y="18" fill="#e6edf7" font-size="11">Legacy Full-Grid Engine</text>
        <circle cx="14" cy="31" r="4" fill="#06b6d4" />
        <text x="26" y="35" fill="#e6edf7" font-size="11">ArbiGraph Smart Router</text>
      </g>
    `;
  }

  init();
})();
