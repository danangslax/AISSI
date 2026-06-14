import asyncio
import os

from dotenv import load_dotenv

from telegram import Bot

from loguru import logger

# =========================================
# LOAD ENVIRONMENT VARIABLES
# =========================================

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


class TelegramEngine:

    # =====================================
    # SEND TELEGRAM MESSAGE
    # =====================================

    async def send_message(self, message: str):

        try:

            if not BOT_TOKEN:

                logger.error("Missing TELEGRAM_BOT_TOKEN")

                return

            if not CHAT_ID:

                logger.error("Missing TELEGRAM_CHAT_ID")

                return

            bot = Bot(token=BOT_TOKEN)

            await bot.send_message(chat_id=CHAT_ID, text=message)

            logger.success("Telegram alert sent")

        except Exception as e:

            logger.error(f"Telegram failed: {e}")

    # =====================================
    # PUBLIC SEND METHOD
    # =====================================

    def send(self, message: str):

        asyncio.run(self.send_message(message))
