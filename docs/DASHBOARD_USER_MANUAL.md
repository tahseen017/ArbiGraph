# ArbiGraph Pro Terminal — User & Trader Manual

## 1. What Is Arbitrage (In Plain English)?
Normally, exchange rates across currencies are balanced. For example, if you convert **USD → EUR → GBP → USD**, you usually end up with slightly *less* money than you started with because of dealer spreads and fees.

**Currency Arbitrage** happens when two or more exchanges/desks temporarily misprice currencies relative to each other. By moving money around a closed loop—for example:
1. **Sell `$1,000.00 USD`** to buy **`€925.00 EUR`** *(London Desk)*
2. **Sell `€925.00 EUR`** to buy **`£809.38 GBP`** *(Frankfurt Desk)*
3. **Sell `£809.38 GBP`** to buy **`$1,020.62 USD`** *(New York Desk)*

You end up back in **USD** seconds later with **`$1,020.62` (`+$20.62` / `+2.062%` net profit)**—without betting on whether USD or BTC will go up or down tomorrow!

---

## 2. Are We Trading Real Money Here, or Generating Signals?
**ArbiGraph is a Real-Time Signal Scanner, Paper-Trade Simulator & Smart FX Router (Non-Custodial).**

* **It does NOT touch a bank account or auto-spend real money.** You never connect private wallet keys, so there is zero risk of losing funds.
* **Yes — It Generates Two Types of Actionable Financial Signals:**
  1. **🟢 Round-Trip Arbitrage Signals (Profit Generation):** When markets have a price mismatch larger than your trading fee, ArbiGraph flags an **Actionable Signal**, builds the exact leg-by-leg **Order Execution Ticket** (`SELL X → BUY Y @ Rate`), tells you your **exact simulated profit**, and caps your order size so you don't exceed market liquidity.
  2. **🔵 Smart Conversion Routes (Cost Saving when Arbitrage = 0):** Most of the time, live markets are efficient after fees (`0 Arbitrage`). Instead of becoming useless, ArbiGraph automatically switches into a **Smart Currency Router** (like Wise / 1inch for FX & Crypto)—finding cheaper multi-currency bridge routes (e.g., sending **`BDT → USD → SGD → EUR`** instead of a costly direct **`BDT → EUR`** bank transfer, saving **`+235.8 bps`** or **`+€17.59`** per `100,000 BDT`!).

---

## 3. Why Traders, Remitters & Treasury Desks Use This Terminal

| User Type | Why They Use ArbiGraph | What Output They Get |
| :--- | :--- | :--- |
| **Crypto / FX Arbitrageurs** | Spot 3-leg, 4-leg, and 5-leg cross-exchange price loops faster than humanly possible | Ranked signal list, exact leg-by-leg trade ticket, and break-even fee ceiling |
| **Prop Desk / Portfolio Managers** | Avoid ruining a trade by placing `$10,000` into a pair that only has `$3,000` of orderbook depth | Liquidity-capped capital split across multiple signals simultaneously |
| **Businesses / Remitters (`BDT`, `USD`, `EUR`)** | Pay lower FX spreads on international transfers when direct bank rates are expensive | Multi-currency bridge route + exact basis-point (`bps`) savings vs. direct bank quotes |

---

## 4. Step-by-Step Dashboard Manual

### A. Top Bar (Market Feed & Regime Indicator)
* **Status Pill (`LIVE SIGNAL` vs `MARKET BALANCED`):**
  * **Green (`LIVE SIGNAL`):** Risk-free arbitrage loops exist right now after subtracting your fee!
  * **Blue (`MARKET BALANCED · SMART ROUTER ACTIVE`):** No risk-free loops exist at your current fee tier; the terminal is now optimizing one-way currency conversions.
* **Market Feed Selector:** Switch between **3 Desk Snapshots** (Institutional FX, BDT Global Remittance, Multi-Exchange Crypto) and **2 Live Market Feeds** (`LIVE Kraken Spot Orderbook` & `LIVE Global FX + BDT Interbank Feed`).
* **`↻ Scan Orderbooks` Button:** Pulls fresh live prices and recalculates all signals and routes immediately.

---

### B. Left Sidebar (Your Trading & Treasury Controls)
1. **Trading Fee per Leg (`0.00%` – `1.20%`):**
   * Set this to match your exchange tier (e.g., `0.00%` VIP Maker, `0.10%` Binance/Kraken Spot, `0.50%` Retail App). Watch low-margin signals automatically disappear as fees rise!
   * **`⚡ Switch to Smart Routing` Button:** Automatically sets the fee just above the market's break-even threshold so you can see how the market behaves once arbitrage spreads are arbitraged away.
2. **Ticket Size & Desk Capital (`$`):**
   * **Ticket Size:** Amount of starting currency simulated in the right-hand **Actionable Order Ticket** (e.g., `1,000 USD` or `100,000 BDT`).
   * **Desk Capital (`$`):** Total portfolio budget (e.g., `$10,000`) split across multiple signals in Tab 1.
3. **Smart Currency Converter (`Pay Asset` → `Receive Asset`):**
   * Pick which currency you have (e.g., `BDT`) and which currency you want (e.g., `EUR`) when using Smart Routing.
4. **Custom Quote Simulator (What-If Desk):**
   * Did a local broker or OTC desk quote you a special rate (e.g., `Sell GBP → Buy USD @ 1.2950`)? Type it in and click **Apply Quote** to see instantaneously if that quote creates a new arbitrage signal against the rest of the market!

---

### C. Top 4 KPI Cards (At-a-Glance Desk Summary)
1. **Active Market Coverage:** How many currencies, pairs, and venues are currently being monitored.
2. **Arbitrage Signal Scanner:** Highest single-loop net ROI `%` and total count of profitable signals.
3. **Max Fee Tolerance:** The **exact maximum fee per trade** your account can pay before arbitrage profits drop to zero (your "margin cushion").
4. **Desk PnL / Routing Edge:**
   * In *Signal Mode*: Total dollar profit (`Est. PnL`) across your Desk Capital.
   * In *Balanced Mode*: Basis points saved (`100 bps = 1.00%`) by using the Smart Bridge vs. a direct quote.

---

### D. Center Flow Map & Right-Hand Order Ticket
* **Global Liquidity Flow Map (Left):**
  * **Animated Green Loop:** Shows the exact path of the selected Arbitrage Signal and the net exchange rate on each leg.
  * **Animated Blue Path:** Shows the cheapest multi-currency conversion bridge when no arbitrage exists.
  * *Tip:* Click any currency circle on the map to set your `Receive` currency (or `Shift + Click` to set your `Pay` currency).
* **Actionable Order Ticket (Right):**
  * Your ready-to-read trade sheet: tells you which currency to sell, which to buy, at which venue/desk, how much comes out at each step, your **Net Round-Trip Profit**, and the **Max Simultaneous Fill** (orderbook depth limit before price slippage occurs).

---

### E. Bottom 4 Workspace Tabs
* **Tab 1 — `Live Arbitrage Signals & Desk Allocation`:**
  * **Left Table:** Every profitable signal ranked from highest to lowest ROI `%`. **Click any row** to load that signal onto the map and ticket!
  * **Right Table:** Tells you how to divide your `$10,000` Desk Capital across the top signals without overflowing any market's liquidity cap (e.g., `$4,500` into Signal #1, `$3,200` into Signal #2, `$2,300` into Signal #3 = `+$162.71` total profit).
  * **Bottom Table:** Full raw & post-fee orderbook quotes across all venues.
* **Tab 2 — `Smart Currency Router & Rate Matrix`:**
  * **Left Table:** Lists currency pairs where bridging through intermediate hub currencies beats direct bank/exchange rates (click any row to inspect the transfer ticket).
  * **Bottom Matrix:** Complete cross-rate lookup table (`Pay \ Receive`) showing the best achievable conversion rate between every pair of currencies.
* **Tab 3 — `Fee Stress-Test & Margin Cushion`:**
  * Tests your strategy across tightening fee tiers to show exactly which fee levels keep signals `PROFITABLE SIGNAL` vs. `WIPED BY FEES`.
* **Tab 4 — `Scanner Speed & Market Throughput`:**
  * Live system latency monitor testing scan speeds from 15 regional assets up to 160 global currencies in milliseconds.
