# CSE246 Viva & Presentation Cheat-Sheet (`ArbiGraph`)

Use this guide before presenting to your instructor—these are the **top 7 questions** professors ask on Currency Arbitrage & Johnson’s Algorithm, with exact answers matching your code.

---

### Q1. Why do we set edge weights to $w(u,v) = -\ln(\text{rate})$ instead of using the exchange rate directly?
* **Answer:** Shortest-path algorithms **add** edge weights along a path, whereas currency conversions **multiply** exchange rates ($R_1 \times R_2 \times R_3$). Taking $\ln(\cdot)$ turns multiplication into addition ($\ln(a \cdot b) = \ln a + \ln b$). Multiplying by $-1$ flips $> 1$ (profit) into $< 0$ (a **negative-weight cycle**) and flips "maximum rate path" into "minimum weight path."

---

### Q2. In Bellman–Ford (`bellman_ford.py`), why do you walk backward `V` times (`curr = parent[curr]`) before extracting the cycle?
* **Answer:** When an edge $(u, v)$ relaxes on the $V$-th pass, vertex $v$ is guaranteed to be **reachable** from a negative cycle,- **not necessarily inside** the cycle itself (for example, `USD -> EUR -> GBP -> USD` could feed into a branch `-> BDT`). Because any simple path in a graph of $V$ vertices has at most $V - 1$ edges, walking backward $V$ steps along `parent` pointers is mathematically guaranteed to enter the negative cycle itself!

---

### Q3. Why did you initialize `dist[v] = 0.0` for all vertices instead of `dist[source] = 0` and `+inf` for others?
* **Answer:** If a market graph has disconnected regional clusters or one-way quotes, starting from a single currency might miss an arbitrage loop in another component. Setting `dist[v] = 0` for all $v$ is mathematically identical to adding Johnson’s virtual super-source node $q$ with $0$-weight edges $q \to v$ to every currency—after 1 pass from $q$, every vertex has distance $0$.

---

### Q4. Why can’t we run Dijkstra directly when there is NO arbitrage? Why can’t we just add `+10` to every edge to make weights positive?
* **Answer:**
  1. Even with zero arbitrage, any exchange rate $> 1.0$ (like $1\text{ USD} = 119.75\text{ BDT}$) has weight $-\ln(119.75) = -4.785 < 0$, which breaks Dijkstra's greedy assumption.
  2. **Adding a constant `+C` to every edge changes which path is shortest!** A 3-hop path gets $+3C$ penalty while a 1-hop path gets $+1C$ penalty, unfairly punishing multi-hop routes.
  3. **Johnson’s potential reweighting** $\hat{w}(u,v) = w(u,v) + h(u) - h(v) \ge 0$ telescopically cancels intermediate vertices along any path $u \to x \to y \to v$:
     $$\hat{w}(P) = w(P) + h(u) - h(v)$$
     Since $h(u) - h(v)$ depends **only** on start $u$ and end $v$ (not the number of hops!), shortest paths never change!

---

### Q5. When is Johnson’s Algorithm faster than Floyd–Warshall?
* **Answer:** Floyd–Warshall is always $\Theta(V^3)$. Johnson’s is $O(V^2 \log V + VE)$. Real-world FX and crypto markets are **sparse hub-and-spoke graphs** ($E \approx 5V$, because minor currencies quote against hubs like `USD`/`EUR`/`USDT` rather than all 160 world currencies quoting against each other). In our live benchmark (`Tab 4` / `python3 cli.py --benchmark`), Johnson’s crosses over Floyd–Warshall around $V \approx 65$ and is **>2.3× faster at $V = 160$** with `0.0` matrix discrepancy.

---

### Q6. How do you prevent floating-point rounding noise from reporting fake `0.00000001%` arbitrage?
* **Answer:** Two safeguards in `bellman_ford.py`:
  1. Relaxation requires strict improvement beyond `EPS = 1e-9`: `dist[u] + w < dist[v] - 1e-9`.
  2. Every candidate cycle is verified by multiplying actual effective rates (`multiplier > 1.000001`) before accepting it.

---

### Q7. How does Binary Search find the Break-Even Fee (`optimizations.py`)?
* **Answer:** As fee $f$ increases, every edge weight $w(f) = -\ln(R(1 - f))$ strictly increases, so arbitrage profitability is a **monotonic boolean predicate** (`True, True, ..., True, False, False`). Binary Search bisects $f \in [0\%, 10\%]$ in 24 steps using Bellman–Ford as the oracle to pinpoint the exact maximum fee down to $0.0001\%$.
