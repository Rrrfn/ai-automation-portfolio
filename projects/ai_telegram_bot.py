import asyncio
import logging
import os
from collections import defaultdict, deque
from typing import Dict, List

from dotenv import load_dotenv
from groq import AsyncGroq
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ChatAction, ParseMode
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# 1. Configuration & Logging Setup
load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not TELEGRAM_BOT_TOKEN or not GROQ_API_KEY:
    raise ValueError("Missing TELEGRAM_BOT_TOKEN or GROQ_API_KEY in environment variables.")

# Initialize Async Groq Client
groq_client = AsyncGroq(api_key=GROQ_API_KEY)

# 2. System Prompts & Memory Management
SYSTEM_PROMPTS = {
    "crypto_expert": (
        "You are a senior Web3 & Crypto analyst. Provide precise, technical, and data-driven "
        "insights on blockchain technology, DeFi, and market analysis. Keep responses structured and clean."
    ),
    "dev_assistant": (
        "You are a principal Python & Automation Engineer. Provide production-grade, asynchronous, "
        "and clean code solutions with brief explanations."
    ),
    "general": (
        "You are a highly capable, concise, and helpful AI assistant."
    )
}

MEMORY_LIMIT = 10
user_memory: Dict[int, deque] = defaultdict(lambda: deque(maxlen=MEMORY_LIMIT))
user_modes: Dict[int, str] = defaultdict(lambda: "crypto_expert")


# 3. Helper Functions
def get_mode_keyboard() -> InlineKeyboardMarkup:
    """Generates inline keyboard for persona switching."""
    keyboard = [
        [
            InlineKeyboardButton("🌐 Web3 Analyst", callback_data="mode_crypto_expert"),
            InlineKeyboardButton("💻 Python Dev", callback_data="mode_dev_assistant"),
        ],
        [
            InlineKeyboardButton("🤖 General Assistant", callback_data="mode_general"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


# 4. Command Handlers
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles /start command with interactive mode selection."""
    user = update.effective_user
    welcome_text = (
        f"👋 Welcome, **{user.first_name}**!\n\n"
        "I am an enterprise-grade AI assistant powered by **Llama 3.3 (via Groq API)**.\n\n"
        "⚙️ **Features:**\n"
        "• Context-aware conversation memory.\n"
        "• Asynchronous low-latency stream processing.\n"
        "• Multi-persona system modes.\n\n"
        "Select an operational mode below to begin:"
    )
    await update.message.reply_text(
        welcome_text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=get_mode_keyboard(),
    )


async def reset_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Clears conversation history for the current user."""
    user_id = update.effective_user.id
    user_memory[user_id].clear()
    await update.message.reply_text("🔄 **Memory cleared successfully.** Context reset to initial state.")


async def mode_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Allows user to change bot persona."""
    await update.message.reply_text(
        "Select your desired AI persona mode:",
        reply_markup=get_mode_keyboard(),
    )


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles inline keyboard button interactions."""
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    selected_mode = query.data.replace("mode_", "")

    if selected_mode in SYSTEM_PROMPTS:
        user_modes[user_id] = selected_mode
        user_memory[user_id].clear()
        
        mode_names = {
            "crypto_expert": "Web3 Analyst",
            "dev_assistant": "Python Dev",
            "general": "General Assistant"
        }
        await query.edit_message_text(
            f"✅ Mode switched to: **{mode_names[selected_mode]}**\n"
            "Conversation memory has been reset for the new persona.",
            parse_mode=ParseMode.MARKDOWN,
        )


# 5. Core AI Message Processing Handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Processes user text input, manages memory context, and queries Groq API."""
    user_id = update.effective_user.id
    user_input = update.message.text.strip()

    if not user_input:
        return

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

    current_mode = user_modes[user_id]
    messages_payload: List[Dict[str, str]] = [
        {"role": "system", "content": SYSTEM_PROMPTS[current_mode]}
    ]

    for msg in user_memory[user_id]:
        messages_payload.append(msg)

    messages_payload.append({"role": "user", "content": user_input})

    try:
        chat_completion = await groq_client.chat.completions.create(
            messages=messages_payload,
            model="llama-3.3-70b-versatile",
            temperature=0.6,
            max_tokens=1500,
        )

        ai_response = chat_completion.choices[0].message.content

        user_memory[user_id].append({"role": "user", "content": user_input})
        user_memory[user_id].append({"role": "assistant", "content": ai_response})

        await update.message.reply_text(ai_response, parse_mode=ParseMode.MARKDOWN)

    except Exception as e:
        logger.error(f"Error processing AI response for user {user_id}: {e}", exc_info=True)
        await update.message.reply_text(
            "⚠️ **Error:** Failed to generate response from LLM backend. Please try again shortly.",
            parse_mode=ParseMode.MARKDOWN,
        )


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Global error logging handler."""
    logger.error(f"Update {update} caused error {context.error}")


# 6. Bot Initialization Loop
def main() -> None:
    """Starts the Telegram bot application."""
    
    # Configure Proxy dynamically if PROXY_URL is set in environment
    proxy_url = os.getenv("PROXY_URL")
    if proxy_url:
        os.environ["HTTP_PROXY"] = proxy_url
        os.environ["HTTPS_PROXY"] = proxy_url
        os.environ["ALL_PROXY"] = proxy_url
        logger.info(f"Proxy configured via environment variable: {proxy_url}")

    app = (
        Application.builder()
        .token(TELEGRAM_BOT_TOKEN)
        .build()
    )

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("reset", reset_command))
    app.add_handler(CommandHandler("mode", mode_command))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    app.add_error_handler(error_handler)

    logger.info("Starting AI Telegram Bot service...")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
