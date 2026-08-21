"""
Advanced Crypto Analytics & Market Tracker (KuCoin API Engine)
==============================================================
An asynchronous Python utility to fetch real-time cryptocurrency data from KuCoin,
compute technical indicators (RSI, Moving Averages), evaluate market sentiment,
and export structured analytics reports.

Author: AI & Automation Specialist
License: MIT
"""

import asyncio
import aiohttp
import pandas as pd
import numpy as np
import logging
import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from tabulate import tabulate

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("CryptoTracker")


class TechnicalAnalysis:
    """Computes technical indicators using pandas and numpy."""

    @staticmethod
    def calculate_rsi(prices: pd.Series, period: int = 14) -> float:
        """Calculate Relative Strength Index (RSI)."""
        if len(prices) < period:
            return 50.0
        
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

        rs = gain / loss.replace(0, np.nan)
        rsi = 100 - (100 / (1 + rs))
        val = rsi.iloc[-1]
        return round(val, 2) if not np.isnan(val) else 50.0

    @staticmethod
    def calculate_sma(prices: pd.Series, period: int = 20) -> float:
        """Calculate Simple Moving Average (SMA)."""
        if len(prices) < period:
            return float(prices.iloc[-1])
        return round(prices.rolling(window=period).mean().iloc[-1], 2)

    @staticmethod
    def calculate_ema(prices: pd.Series, period: int = 50) -> float:
        """Calculate Exponential Moving Average (EMA)."""
        if len(prices) < period:
            return float(prices.iloc[-1])
        return round(prices.ewm(span=period, adjust=False).mean().iloc[-1], 2)

    @classmethod
    def evaluate_signal(cls, price: float, rsi: float, sma: float) -> str:
        """Evaluate overall technical bias."""
        if rsi < 30 and price > sma:
            return "STRONG_BUY"
        elif rsi < 35:
            return "BUY"
        elif rsi > 70 and price < sma:
            return "STRONG_SELL"
        elif rsi > 65:
            return "SELL"
        return "NEUTRAL"


class KuCoinFetcher:
    """Asynchronous fetcher for KuCoin Public REST API."""

    BASE_URL = "https://api.kucoin.com/api/v1/market"

    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    async def get_24h_ticker(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Fetch 24-hour price change statistics for a symbol (e.g. BTC-USDT)."""
        url = f"{self.BASE_URL}/stats?symbol={symbol}"
        try:
            async with self.session.get(url, timeout=10) as response:
                if response.status == 200:
                    res = await response.json()
                    if res.get("code") == "200000":
                        return res.get("data")
                logger.error(f"Failed to fetch ticker for {symbol}: HTTP {response.status}")
        except Exception as e:
            logger.error(f"Exception fetching ticker for {symbol}: {e}")
        return None

    async def get_klines(self, symbol: str, interval: str = "1hour", limit: int = 100) -> Optional[List[float]]:
        """Fetch historical close prices from OHLCV klines."""
        url = f"{self.BASE_URL}/candles?symbol={symbol}&type={interval}"
        try:
            async with self.session.get(url, timeout=10) as response:
                if response.status == 200:
                    res = await response.json()
                    if res.get("code") == "200000" and res.get("data"):
                        # KuCoin payload: [time, open, close, high, low, volume, turnover]
                        raw_candles = res["data"][:limit]
                        close_prices = [float(candle[2]) for candle in reversed(raw_candles)]
                        return close_prices
                logger.error(f"Failed to fetch klines for {symbol}: HTTP {response.status}")
        except Exception as e:
            logger.error(f"Exception fetching klines for {symbol}: {e}")
        return None


class CryptoTrackerEngine:
    """Main Orchestrator for data processing and analysis pipeline."""

    DEFAULT_SYMBOLS = ["BTC-USDT", "ETH-USDT", "SOL-USDT", "KCS-USDT", "ADA-USDT", "XRP-USDT", "AVAX-USDT"]

    def __init__(self, symbols: Optional[List[str]] = None):
        self.symbols = symbols or self.DEFAULT_SYMBOLS

    async def process_symbol(self, fetcher: KuCoinFetcher, symbol: str) -> Optional[Dict[str, Any]]:
        """Process price data and technical indicators for a single symbol."""
        ticker_task = fetcher.get_24h_ticker(symbol)
        klines_task = fetcher.get_klines(symbol, interval="1hour", limit=100)

        ticker, klines = await asyncio.gather(ticker_task, klines_task)

        if not ticker or not klines:
            return None

        prices_series = pd.Series(klines)
        current_price = float(ticker["last"]) if ticker.get("last") else klines[-1]
        
        # Calculate 24h change percentage
        change_24h = float(ticker.get("changeRate", 0)) * 100
        volume_24h = float(ticker.get("volValue", 0))

        rsi_14 = TechnicalAnalysis.calculate_rsi(prices_series, period=14)
        sma_20 = TechnicalAnalysis.calculate_sma(prices_series, period=20)
        ema_50 = TechnicalAnalysis.calculate_ema(prices_series, period=50)
        signal = TechnicalAnalysis.evaluate_signal(current_price, rsi_14, sma_20)

        return {
            "Symbol": symbol.replace("-USDT", ""),
            "Price (USD)": current_price,
            "24h Change (%)": round(change_24h, 2),
            "24h Volume ($M)": round(volume_24h / 1_000_000, 2),
            "RSI (14)": rsi_14,
            "SMA (20)": sma_20,
            "EMA (50)": ema_50,
            "Signal": signal,
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    async def run_pipeline(self) -> List[Dict[str, Any]]:
        """Run full asynchronous tracking pipeline across all target symbols."""
        logger.info(f"Starting analysis for {len(self.symbols)} symbols via KuCoin API...")
        async with aiohttp.ClientSession() as session:
            fetcher = KuCoinFetcher(session)
            tasks = [self.process_symbol(fetcher, sym) for sym in self.symbols]
            results = await asyncio.gather(*tasks)

        processed_data = [res for res in results if res is not None]
        return processed_data


def export_reports(data: List[Dict[str, Any]], export_format: str = "all") -> None:
    """Export analytical output into CSV and JSON logs."""
    if not data:
        logger.warning("No data available to export.")
        return

    df = pd.DataFrame(data)
    output_dir = Path("data_exports")
    output_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if export_format in ["csv", "all"]:
        csv_path = output_dir / f"crypto_report_{timestamp}.csv"
        df.to_csv(csv_path, index=False)
        logger.info(f"Exported CSV report to {csv_path}")

    if export_format in ["json", "all"]:
        json_path = output_dir / f"crypto_report_{timestamp}.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        logger.info(f"Exported JSON report to {json_path}")

    print("\n" + tabulate(df[["Symbol", "Price (USD)", "24h Change (%)", "RSI (14)", "Signal"]], headers="keys", tablefmt="heavy_outline"))


def parse_arguments():
    """Command Line Interface argument parser."""
    parser = argparse.ArgumentParser(description="Advanced Crypto Market Tracker CLI")
    parser.add_argument("--symbols", nargs="+", help="Custom crypto trading pairs (e.g. BTC-USDT ETH-USDT)")
    parser.add_argument("--export", choices=["csv", "json", "all", "none"], default="all", help="Output export format")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    engine = CryptoTrackerEngine(symbols=args.symbols)
    
    # Run async loop
    analytics_results = asyncio.run(engine.run_pipeline())
    
    if args.export != "none":
        export_reports(analytics_results, export_format=args.export)
