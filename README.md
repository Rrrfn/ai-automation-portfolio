# 🚀 AI Automation Portfolio

> AI Automation • LLM Applications • Web3 Intelligence • Telegram Bots • API Integrations • n8n

A collection of practical AI and automation systems built with Python, LLM APIs, Telegram, Web3 data sources, and workflow automation.

The portfolio focuses on building systems that transform raw data and user activity into actionable information, automated decisions, and business intelligence.

---

## 🌟 Featured Project

### Web3 Signal Hunter

**AI-powered B2B Community Intelligence for Web3 teams**

Web3 Signal Hunter analyzes community conversations and transforms unstructured messages into structured business intelligence.

The system can:

- 🧑‍💻 Detect developer demand
- 🛠️ Identify product and support issues
- 💰 Detect revenue opportunities
- 🏷️ Classify community signals
- 🎯 Calculate explainable priority scores
- 🔗 Cluster related conversations
- 📊 Generate Excel intelligence reports
- 📱 Deliver executive summaries through Telegram
- 🔄 Use multi-provider LLM fallback for resilience

### Intelligence Pipeline

```text
Community Messages
        ↓
Batch Processing
        ↓
LLM Analysis
        ↓
Structured Signal Extraction
        ↓
Deterministic Priority Scoring
        ↓
Global Signal Clustering
        ↓
Business Intelligence
        ↓
Excel + Telegram Executive Reports
Technologies

Python Pandas Groq Gemini HTTPX OpenPyXL Telegram Bot API LLM APIs

Repository

View Web3 Signal Hunter →

🤖 Other Automation Projects
1. AI Telegram Assistant

File: projects/ai_telegram_bot.py

An asynchronous multi-persona AI Telegram assistant powered by Groq and Llama.

Features
🌐 Web3 analyst mode
💻 Python developer mode
🤖 General assistant mode
🧠 Per-user conversation memory
🎛️ Inline keyboard mode switching
⚡ Asynchronous LLM requests
📱 Telegram integration
🌐 Optional proxy support
🛡️ Error handling and logging
Architecture
Telegram User
      ↓
Telegram Bot
      ↓
Persona Selection
      ↓
Conversation Memory
      ↓
Groq / Llama
      ↓
AI Response
      ↓
Telegram
Technologies

Python asyncio python-telegram-bot Groq API Llama

2. Crypto Price Alert Bot

File: projects/crypto_alert_bot (1).py

An asynchronous cryptocurrency price monitoring bot that retrieves real-time market prices and sends Telegram alerts when configured thresholds are reached.

Features
📈 Real-time KuCoin market data
🔔 Custom price alerts
💱 Multiple trading pairs
💾 Persistent JSON alert storage
⚙️ Background monitoring
🚨 Automatic alert triggering
📱 Telegram command interface
✅ Input validation
🛡️ Error handling
Commands
/start
/help
/price <symbol>
/alert <symbol> <target_price>
/alerts
/remove <alert_id>
Example
/alert BTC 110000
Architecture
KuCoin API
    ↓
Market Price Fetcher
    ↓
Alert Monitoring Engine
    ↓
Threshold Detection
    ↓
Telegram Notification
Technologies

Python asyncio aiohttp KuCoin REST API Telegram Bot API

3. Crypto Market Analytics Engine

File: projects/crypto_tracker.py

An asynchronous cryptocurrency market analytics engine that collects market data and calculates technical indicators for multiple trading pairs.

Features
📡 Real-time market data collection
🕯️ Historical OHLCV data
📊 RSI-14
📈 SMA-20
📉 EMA-50
🎯 Technical signal generation
💱 Multiple trading-pair support
📄 CSV export
🗂️ JSON export
⚙️ Command-line configuration
⚡ Concurrent market processing
Example
python projects/crypto_tracker.py \
  --symbols BTC-USDT ETH-USDT SOL-USDT \
  --export csv
Processing Pipeline
KuCoin REST API
      ↓
Market Data
      ↓
Historical Candles
      ↓
Technical Indicators
      ↓
Signal Evaluation
      ↓
CSV / JSON Reports
Technologies

Python asyncio aiohttp Pandas NumPy KuCoin REST API

This project is an analytics and automation demonstration and does not provide financial advice.

4. AI Crypto News Automation

File: projects/n8n_news_automation.json

An n8n workflow that automatically collects cryptocurrency news, analyzes articles with an LLM, filters low-impact items, and publishes relevant updates to Telegram.

Workflow
Scheduled Trigger
      ↓
Crypto RSS Feed
      ↓
Duplicate Removal
      ↓
Article Limiting
      ↓
Groq AI Analysis
      ↓
JSON Parsing
      ↓
Impact Filtering
      ↓
Telegram Broadcast
Features
⏰ Scheduled execution
📰 RSS ingestion
🔍 Duplicate detection
🧹 Article filtering
🧠 LLM-powered analysis
📊 Sentiment classification
🎯 Impact scoring
📱 Telegram formatting
🤖 Automated publishing
Technologies

n8n Groq API RSS JavaScript Telegram Bot API

🧠 Technical Capabilities

These projects demonstrate practical experience with:

AI & LLM
🔌 LLM API integration
📋 Structured LLM output
✍️ Prompt engineering
🔄 Multi-model fallback
🏷️ AI classification
🔎 Business signal extraction
🎯 Deterministic scoring
Automation
📱 Telegram automation
🔗 n8n workflows
⏰ Scheduled processing
⚙️ Background workers
🔌 API-driven automation
🚨 Event-based notifications
Python
⚡ Async programming
🔌 REST API integration
📊 Data processing
💻 CLI applications
🛡️ Error handling
📝 Logging
💾 Persistent storage
Web3 & Crypto
₿ Cryptocurrency market APIs
🧠 Web3 community intelligence
🧑‍💻 Developer demand detection
🛠️ Product signal detection
📰 Crypto news automation
📈 Trading-pair analytics
Business Intelligence
🏷️ Signal classification
🎯 Priority scoring
💰 Revenue opportunity detection
🧩 Product intelligence
📊 Executive reporting
💡 Data-driven recommendations
🏗️ Portfolio Architecture

The projects in this portfolio represent different layers of an automation stack:

                    AI / LLM
                       │
                       ▼
Data Sources ──→ Processing ──→ Intelligence
    │                │               │
    │                │               │
    ▼                ▼               ▼
Telegram          Python          Scoring
Crypto APIs       Pandas          Classification
RSS               asyncio         Clustering
Web3 Data         n8n             Analysis
                                      │
                                      ▼
                              Business Actions
                                      │
                         ┌────────────┴────────────┐
                         ▼                         ▼
                    Telegram                   Reports
                    Alerts                     Excel
📈 Project Evolution

The projects show an evolution from API automation toward AI-powered business intelligence.

API Integration
      ↓
Crypto Automation
      ↓
Telegram Bots
      ↓
LLM Integration
      ↓
Workflow Automation
      ↓
Signal Detection
      ↓
Business Intelligence

The goal is not simply to build chatbots or scripts.

The focus is on building systems that connect:

Data
 ↓
Automation
 ↓
AI
 ↓
Decision Support
 ↓
Business Action
🧰 Tech Stack
Category	Technologies
Programming	Python
AI / LLM	Groq, Gemini, OpenAI-compatible APIs
Telegram	Telegram Bot API, python-telegram-bot
Automation	n8n
Web3 / Crypto	KuCoin REST API, Web3 community data
Data Processing	Pandas, NumPy
HTTP / Async	aiohttp, HTTPX, asyncio
Reporting	OpenPyXL, CSV, JSON
Storage	JSON / local persistence
Version Control	Git, GitHub
📁 Repository Structure
ai-automation-portfolio/
│
├── projects/
│   ├── ai_telegram_bot.py
│   ├── crypto_alert_bot (1).py
│   ├── crypto_tracker.py
│   └── n8n_news_automation.json
│
├── .env.example
├── .gitignore
├── requirements.txt
├── README.backup.md
└── README.md

The flagship Web3 intelligence project is maintained in a separate repository:

web3-signal-hunter/

View Web3 Signal Hunter →

🚀 Getting Started
Requirements
🐍 Python 3.10+
📱 Telegram Bot Token for Telegram projects
🔑 Groq API Key for AI projects
⚙️ n8n instance for the workflow automation project
Clone
git clone https://github.com/Rrrfn/ai-automation-portfolio.git
cd ai-automation-portfolio
Environment

Create a .env file based on .env.example.

Example:

TELEGRAM_BOT_TOKEN=your_telegram_bot_token
GROQ_API_KEY=your_groq_api_key
PROXY_URL=optional_proxy_url

🔐 Never commit real API keys or credentials.

▶️ Running the Projects
Crypto Analytics
python projects/crypto_tracker.py

Custom symbols:

python projects/crypto_tracker.py \
  --symbols BTC-USDT ETH-USDT SOL-USDT \
  --export csv
Crypto Price Alerts
python "projects/crypto_alert_bot (1).py"

Example:

/price BTC
/alert BTC 110000
/alerts
/remove <alert_id>
AI Telegram Assistant
python projects/ai_telegram_bot.py

Commands:

/start
/mode
/reset
⚙️ n8n Workflow

Import:

projects/n8n_news_automation.json

Then configure:

🔑 Groq credentials
📱 Telegram credentials
📢 Target Telegram channel
📰 RSS source
⏰ Workflow schedule

The workflow is provided as a portfolio/demo automation template and may require configuration before production use.

🔐 Security

This repository is designed to keep credentials outside the source code.

Never publish:

🔑 Telegram bot tokens
🔐 Groq API keys
🔐 Gemini API keys
🔑 Private keys
👛 Wallet credentials
🎫 Personal access tokens
🗄️ Production database credentials

Use environment variables or the credential management system of the relevant platform.

🎯 Portfolio Focus

Current focus:

AI Automation · LLM Applications · Web3 · Business Intelligence · Telegram Automation · API Integrations

The long-term direction is to build automation systems that move beyond simple scripts and connect:

Unstructured Data
       ↓
AI Analysis
       ↓
Structured Intelligence
       ↓
Prioritization
       ↓
Automated Action
👤 Author

Rrrfn

AI Automation & Python Developer

Focus areas:

🤖 AI Automation
🧠 LLM Applications
🐍 Python
🌐 Web3
📊 Business Intelligence
📱 Telegram Automation
🔌 API Integrations
⚙️ n8n

GitHub:

https://github.com/Rrrfn

🌟 Featured Repository

Web3 Signal Hunter

AI-powered B2B community intelligence for Web3 teams.

https://github.com/Rrrfn/web3-signal-hunter