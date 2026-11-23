#!/bin/bash
# ArbiGraph Dashboard — Linux / macOS runner
cd "$(dirname "$0")"

echo "================================================"
echo "  ArbiGraph — FX & Crypto Arbitrage Terminal"
echo "================================================"
echo ""

if ! command -v python3 &> /dev/null; then
    echo "ERROR: python3 not found. Please install Python 3.10+."
    exit 1
fi

python3 --version
echo ""
echo "Starting ArbiGraph dashboard server..."
echo "Open your browser to: http://localhost:8000"
echo "Press Ctrl+C to stop."
echo ""

python3 app.py --host 0.0.0.0 --port 8000
