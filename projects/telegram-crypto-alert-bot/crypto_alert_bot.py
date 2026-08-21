"""
Crypto Price Alert Telegram Bot (KuCoin REST API Engine)
========================================================
An asynchronous Telegram bot that monitors cryptocurrency prices in real-time,
allows users to set custom target thresholds, and sends instant alert notifications.

Author: AI & Automation Specialist
License: MIT
"""

import asyncio
import json
import logging
import os
import uuid
from pathlib import Path
from typing import Dict, List, Optional

import aiohttp
from dotenv import load_dotenv
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

# 1. Configuration & Logging Setup
load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("CryptoAlertBot")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("Missing TELEGRAM_BOT_TOKEN in environment variables.")

ALERTS_FILE = Path("data_exports/alerts.json")
CHECK_INTERVAL_SECONDS = 30  # Price check frequency


# 2. Persistence Layer (JSON Alert Storage)
def load_alerts() -> List[Dict]:
    """Load active alerts from local JSON storage."""
    if ALERTS_FILE.exists():
        try:
            with open(ALERTS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading alerts file: {e}")
    return []


def save_alerts(alerts: List[Dict]) -> None:
    """Save active alerts to local JSON storage."""
    try:
        ALERTS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(ALERTS_FILE, "w", encoding="utf-8") as f:
            json.dump(alerts, f, indent=2)
    except Exception as e:
        logger.error(f"Error saving alerts file: {e}")


active_alerts: List[Dict] = load_alerts()


# 3. Market Data Fetcher Engine
class KuCoinFetcher:
    """Asynchronous fetcher for KuCoin real-time ticker endpoint."""

    BASE_URL = "https://api.kucoin.com/api/v1/market/orderbook/level1"

    @classmethod
    async def get_price(cls, session: aiohttp.ClientSession, symbol: str) -> Optional[float]:
        """Fetch current price for a symbol (e.g., BTC, ETH-USDT)."""
        formatted_symbol = symbol.upper()
        if not formatted_symbol.endswith("-USDT") and "-" not in formatted_symbol:
            formatted_symbol = f"{formatted_symbol}-USDT"

        url = f"{cls.BASE_URL}?symbol={formatted_symbol}"
        try:
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("code") == "200000" and data.get("data"):
                        return float(data["data"]["price"])
        except Exception as e:
            logger.error(f"Failed to fetch price for {formatted_symbol}: {e}")
        return None


# 4. Command Handlers
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send welcome message and command overview."""
    welcome_text = (
        "🤖 **Welcome to Crypto Price Alert Bot!**\n\n"
        "I monitor real-time cryptocurrency prices via the KuCoin API and deliver instant notifications when your price targets are hit.\n\n"
        "⚡ **Quick Start Guide:**\n"
        "1️⃣ Check current market price: `/price BTC`\n"
        "2️⃣ Set a target alert: `/alert BTC 95000`\n"
        "3️⃣ View your active alerts: `/alerts`\n\n"
        "🛠 **Available Commands:**\n"
        "• `/price <symbol>` — Fetch live price (e.g., `/price BTC` or `/price ETH`)\n"
        "• `/alert <symbol> <target_price>` — Set alert above/below target (e.g., `/alert SOL 200`)\n"
        "• `/alerts` — List all your active alerts and IDs\n"
        "• `/remove <alert_id>` — Cancel an active alert by ID\n"
        "• `/help` — Display this onboard guide anytime"
    )
    await update.message.reply_text(welcome_text, parse_mode=ParseMode.MARKDOWN)


async def price_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Fetch and display current market price for a given token."""
    if not context.args:
        await update.message.reply_text("⚠️ Usage: `/price <symbol>` (e.g., `/price BTC` or `/price ETH`)", parse_mode=ParseMode.MARKDOWN)
        return

    symbol = context.args[0].upper()
    async with aiohttp.ClientSession() as session:
        price = await KuCoinFetcher.get_price(session, symbol)

    if price is not None:
        clean_symbol = symbol.replace("-USDT", "")
        await update.message.reply_text(f"💰 Current Price of **{clean_symbol}**: `${price:,.2f}`", parse_mode=ParseMode.MARKDOWN)
    else:
        await update.message.reply_text(f"❌ Could not fetch price for **{symbol}**. Please check the symbol and try again.", parse_mode=ParseMode.MARKDOWN)


async def alert_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Create a new price alert threshold."""
    if len(context.args) < 2:
        await update.message.reply_text("⚠️ Usage: `/alert <symbol> <target_price>`\nExample: `/alert BTC 100000`", parse_mode=ParseMode.MARKDOWN)
        return

    raw_symbol = context.args[0].upper()
    try:
        target_price = float(context.args[1])
    except ValueError:
        await update.message.reply_text("❌ Invalid target price format. Please specify a numeric price.")
        return

    async with aiohttp.ClientSession() as session:
        current_price = await KuCoinFetcher.get_price(session, raw_symbol)

    if current_price is None:
        await update.message.reply_text(f"❌ Invalid market symbol: **{raw_symbol}**.", parse_mode=ParseMode.MARKDOWN)
        return

    clean_symbol = raw_symbol.replace("-USDT", "")
    condition = "ABOVE" if target_price > current_price else "BELOW"
    alert_id = str(uuid.uuid4())[:8]

    alert_item = {
        "id": alert_id,
        "chat_id": update.effective_chat.id,
        "symbol": clean_symbol,
        "target_price": target_price,
        "created_price": current_price,
        "condition": condition,
    }

    active_alerts.append(alert_item)
    save_alerts(active_alerts)

    icon = "📈" if condition == "ABOVE" else "📉"
    msg = (
        f"✅ **Alert Set Successfully!**\n\n"
        f"• **Symbol:** {clean_symbol}\n"
        f"• **Current Price:** `${current_price:,.2f}`\n"
        f"• **Target Price:** `${target_price:,.2f}` {icon}\n"
        f"• **Condition:** Trigger when price moves **{condition}** target\n"
        f"• **Alert ID:** `{alert_id}`"
    )
    await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)


async def alerts_list_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Display active alerts set by the requesting user."""
    chat_id = update.effective_chat.id
    user_alerts = [a for a in active_alerts if a["chat_id"] == chat_id]

    if not user_alerts:
        await update.message.reply_text("📭 You have no active alerts set. Use `/alert` to add one!")
        return

    response = "📋 **Your Active Price Alerts:**\n\n"
    for a in user_alerts:
        icon = "📈" if a["condition"] == "ABOVE" else "📉"
        response += f"• **{a['symbol']}** {icon} `${a['target_price']:,.2f}` | ID: `{a['id']}`\n"

    response += "\nTo remove an alert, use `/remove <alert_id>`"
    await update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)


async def remove_alert_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Remove an active alert by ID."""
    if not context.args:
        await update.message.reply_text("⚠️ Usage: `/remove <alert_id>`", parse_mode=ParseMode.MARKDOWN)
        return

    alert_id = context.args[0].strip()
    chat_id = update.effective_chat.id

    global active_alerts
    initial_count = len(active_alerts)
    active_alerts = [a for a in active_alerts if not (a["id"] == alert_id and a["chat_id"] == chat_id)]

    if len(active_alerts) < initial_count:
        save_alerts(active_alerts)
        await update.message.reply_text(f"🗑 Alert `{alert_id}` has been removed.", parse_mode=ParseMode.MARKDOWN)
    else:
        await update.message.reply_text(f"❌ Alert ID `{alert_id}` not found.", parse_mode=ParseMode.MARKDOWN)


# 5. Background Price Monitoring Loop
async def monitor_price_alerts(app: Application) -> None:
    """Background task running continuously to evaluate price conditions."""
    logger.info("Starting background price monitoring loop...")
    while True:
        try:
            if active_alerts:
                symbols_to_check = list({a["symbol"] for a in active_alerts})
                prices: Dict[str, float] = {}

                async with aiohttp.ClientSession() as session:
                    for sym in symbols_to_check:
                        price = await KuCoinFetcher.get_price(session, sym)
                        if price is not None:
                            prices[sym] = price

                triggered_alerts = []
                for alert in list(active_alerts):
                    sym = alert["symbol"]
                    if sym not in prices:
                        continue

                    current_price = prices[sym]
                    target_price = alert["target_price"]
                    condition = alert["condition"]

                    is_triggered = False
                    if condition == "ABOVE" and current_price >= target_price:
                        is_triggered = True
                    elif condition == "BELOW" and current_price <= target_price:
                        is_triggered = True

                    if is_triggered:
                        triggered_alerts.append(alert)
                        icon = "🚀" if condition == "ABOVE" else "🔻"
                        alert_msg = (
                            f"🔔 **PRICE ALERT TRIGGERED!** {icon}\n\n"
                            f"• **Asset:** {sym}\n"
                            f"• **Target Price:** `${target_price:,.2f}`\n"
                            f"• **Current Price:** `${current_price:,.2f}`\n\n"
                            f"Target threshold of **{condition} ${target_price:,.2f}** reached."
                        )
                        try:
                            await app.bot.send_message(
                                chat_id=alert["chat_id"],
                                text=alert_msg,
                                parse_mode=ParseMode.MARKDOWN,
                            )
                        except Exception as send_err:
                            logger.error(f"Failed to send alert to chat {alert['chat_id']}: {send_err}")

                if triggered_alerts:
                    for t_alert in triggered_alerts:
                        if t_alert in active_alerts:
                            active_alerts.remove(t_alert)
                    save_alerts(active_alerts)

        except Exception as e:
            logger.error(f"Error in price monitoring loop: {e}", exc_info=True)

        await asyncio.sleep(CHECK_INTERVAL_SECONDS)


async def post_init_callback(app: Application) -> None:
    """Lifecycle hook to launch non-blocking background task."""
    asyncio.create_task(monitor_price_alerts(app))


# 6. Bot Initialization & Main Entry Point
def main() -> None:
    """Initialize and run the Telegram bot."""
    proxy_url = os.getenv("PROXY_URL")
    
    builder = Application.builder().token(TELEGRAM_BOT_TOKEN).post_init(post_init_callback)

    if proxy_url:
        builder.proxy(proxy_url)
        builder.get_updates_proxy(proxy_url)
        logger.info(f"Proxy configured successfully: {proxy_url}")

    app = builder.build()

    # Command Handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", start_command))
    app.add_handler(CommandHandler("price", price_command))
    app.add_handler(CommandHandler("alert", alert_command))
    app.add_handler(CommandHandler("alerts", alerts_list_command))
    app.add_handler(CommandHandler("remove", remove_alert_command))

    logger.info("Starting Crypto Price Alert Bot polling...")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
