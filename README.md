# 🚀 Telegram Bots & Crypto Automation

A collection of practical Python and n8n automation projects focused on **Telegram bots, cryptocurrency monitoring, market data, and AI-powered workflows**.

These projects demonstrate how I build lightweight automation tools that connect APIs, process data, monitor crypto markets, and deliver useful information through Telegram.

---

## 💼 What I Build

I focus on practical automation solutions such as:

* 🤖 Custom Telegram bots
* 📈 Crypto price monitoring and alerts
* 🔔 Automated Telegram notifications
* ⚙️ n8n workflows and API automation
* 🧠 AI-powered Telegram assistants
* 📰 Crypto news monitoring and summarization
* 📊 Cryptocurrency data collection and technical analysis
* 🔗 API integrations and automation workflows

---

## 🧩 Featured Projects

### 1. 📈 Crypto Price Alert Telegram Bot

**File:** `crypto_alert_bot.py`

A Telegram bot that monitors cryptocurrency prices and sends alerts when configured target prices are reached.

**Key features**

* Real-time price monitoring through the KuCoin API
* Asynchronous background monitoring
* Custom price alerts for multiple trading pairs
* Persistent alert storage
* Telegram command-based interaction
* Error handling and input validation

**Available commands**

```text
/start
/help
/price <symbol>
/alert <symbol> <target_price>
/alerts
/remove <alert_id>
```

**Example**

```text
/alert BTC 110000
```

The bot continuously monitors the selected market and sends a Telegram notification when the target price is reached.

**Technologies**

`Python` · `asyncio` · `aiohttp` · `KuCoin API` · `Telegram Bot API`

---

### 2. 📊 Crypto Market Analytics Engine

**File:** `crypto_tracker.py`

An asynchronous cryptocurrency market analysis tool that retrieves market data from the KuCoin REST API and calculates common technical indicators.

**Key features**

* Cryptocurrency market data collection
* RSI-14 calculation
* SMA-20 calculation
* EMA-50 calculation
* Basic signal generation
* Multiple trading-pair support
* CSV and JSON data export
* Command-line configuration

**Example**

```bash
python crypto_tracker.py --symbols BTC-USDT ETH-USDT SOL-USDT --export csv
```

**Technologies**

`Python` · `asyncio` · `aiohttp` · `Pandas` · `NumPy` · `KuCoin REST API`

> This project is an analytics and automation tool. It does not provide financial advice or guarantee trading results.

---

### 3. 🤖 Multi-Persona AI Telegram Bot

**File:** `ai_telegram_bot.py`

An asynchronous Telegram assistant powered by the Groq API and Llama 3.3, with multiple operational modes and per-user conversation context.

**Key features**

* Multiple assistant modes
* Web3-focused analysis mode
* Python development mode
* General assistant mode
* Per-user conversation memory
* Inline keyboard interaction
* Asynchronous message processing
* Optional HTTP/HTTPS proxy configuration

**Available modes**

```text
Web3 Analyst
Python Developer
General Assistant
```

**Technologies**

`Python` · `asyncio` · `python-telegram-bot` · `Groq API` · `Llama 3.3`

---

### 4. 📰 AI Crypto News Automation with n8n

**File:** `n8n_news_automation.json`

An n8n workflow that collects crypto news, analyzes articles using an LLM, filters low-impact items, and publishes selected updates to Telegram.

### Workflow

```text
Crypto RSS Feed
      ↓
Remove Duplicates
      ↓
Limit Articles
      ↓
Groq AI Analysis
      ↓
Parse & Format
      ↓
Impact Filter
      ↓
Telegram
```

**Key features**

* Scheduled RSS feed collection
* Duplicate filtering
* Automatic article limiting
* LLM-powered news analysis
* Bullish / Bearish / Neutral sentiment classification
* Impact scoring from 1–100
* Automatic filtering of low-impact articles
* HTML-formatted Telegram messages

**Technologies**

`n8n` · `Groq API` · `RSS` · `Telegram Bot API` · `JavaScript`

> API keys, Telegram credentials, and other sensitive values are intentionally excluded from the repository.

---

## 🛠️ Tech Stack

| Category          | Technologies                          |
| ----------------- | ------------------------------------- |
| Programming       | Python                                |
| Telegram          | Telegram Bot API, python-telegram-bot |
| Automation        | n8n, scheduled workflows, webhooks    |
| Crypto Data       | KuCoin REST API                       |
| AI / LLM          | Groq API, Llama 3.3                   |
| Data Processing   | Pandas, NumPy                         |
| Async Programming | asyncio, aiohttp                      |
| Storage           | JSON-based local persistence          |
| Version Control   | Git, GitHub                           |

---

## 📁 Repository Structure

```text
.
├── ai_telegram_bot.py
├── crypto_alert_bot.py
├── crypto_tracker.py
├── n8n_news_automation.json
├── requirements.txt
└── .gitignore
```

---

## ⚙️ Getting Started

### Requirements

* Python 3.10+
* A Telegram Bot Token for the Telegram bot projects
* A Groq API Key for the AI-powered projects
* An n8n instance for the automation workflow

---

### 1. Clone the repository

```bash
git clone https://github.com/Rrrfn/ai-automation-portfolio.git
cd ai-automation-portfolio
```

### 2. Create a virtual environment

#### Linux / macOS

```bash
python -m venv .venv
source .venv/bin/activate
```

#### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Configuration

Create a `.env` file based on the provided example:

```bash
cp .env.example .env
```

Then configure the required credentials:

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
GROQ_API_KEY=your_groq_api_key
PROXY_URL=optional_proxy_url
```

> Never commit real API keys, bot tokens, or other sensitive credentials to GitHub.

---

## ▶️ Running the Projects

### Crypto Market Analytics

```bash
python crypto_tracker.py
```

Custom symbols:

```bash
python crypto_tracker.py --symbols BTC-USDT ETH-USDT SOL-USDT --export csv
```

---

### Crypto Price Alert Bot

```bash
python crypto_alert_bot.py
```

Example Telegram commands:

```text
/price BTC
/alert BTC 110000
/alerts
/remove 1
```

---

### AI Telegram Bot

```bash
python ai_telegram_bot.py
```

Available commands include:

```text
/start
/mode
/reset
```

---

## 🔄 Importing the n8n Workflow

1. Open your n8n instance.
2. Import `n8n_news_automation.json`.
3. Configure the required Groq credentials.
4. Configure your Telegram bot credentials.
5. Set the target Telegram channel or chat.
6. Review the workflow settings.
7. Activate the workflow.

The workflow is provided as a **portfolio/demo automation template** and may require configuration or adaptation for a specific production environment.

---

## 🔒 Security

This repository does not contain real API credentials.

Sensitive configuration should be provided through environment variables or the credential management system of the relevant platform.

Do not publish:

* Telegram bot tokens
* Groq API keys
* Private keys
* Wallet credentials
* Personal access tokens
* Production database credentials

---

## 🎯 Project Focus

This portfolio is primarily focused on:

**Telegram Bots · Crypto Automation · Python Automation · n8n Workflows · AI API Integration**

The projects are designed as practical demonstrations of API integration, asynchronous programming, data processing, automation, and Telegram-based delivery.

---

## 📬 Contact

Interested in a custom Telegram bot, crypto automation tool, or n8n workflow?

Feel free to reach out through my freelance profile or GitHub.

**Available for custom automation projects and integrations.**

---

## 📄 License

This repository is released under the MIT License.
