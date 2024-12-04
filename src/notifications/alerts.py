import aiohttp
import asyncio
from typing import List, Dict
from enum import Enum
from datetime import datetime
from ..config.settings import Settings

class AlertLevel(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class AlertManager:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.webhook_url = settings.WEBHOOK_URL
        self.telegram_token = settings.TELEGRAM_TOKEN
        self.telegram_chat_id = settings.TELEGRAM_CHAT_ID
        self.notification_queue = asyncio.Queue()
        self.is_running = False

    async def start(self):
        """Start the alert manager"""
        self.is_running = True
        await self._process_notifications()

    async def stop(self):
        """Stop the alert manager"""
        self.is_running = False

    async def send_alert(self, message: str, level: AlertLevel = AlertLevel.INFO):
        """Queue an alert for sending"""
        await self.notification_queue.put({
            "message": message,
            "level": level,
            "timestamp": datetime.utcnow()
        })

    async def _process_notifications(self):
        """Process queued notifications"""
        while self.is_running:
            try:
                notification = await self.notification_queue.get()
                await self._send_to_all_channels(notification)
                self.notification_queue.task_done()
            except Exception as e:
                print(f"Error processing notification: {e}")
            await asyncio.sleep(0.1)

    async def _send_to_all_channels(self, notification: Dict):
        """Send notification to all configured channels"""
        tasks = []
        if self.webhook_url:
            tasks.append(self._send_webhook(notification))
        if self.telegram_token and self.telegram_chat_id:
            tasks.append(self._send_telegram(notification))
        
        await asyncio.gather(*tasks)

    async def _send_webhook(self, notification: Dict):
        """Send notification to webhook"""
        async with aiohttp.ClientSession() as session:
            try:
                await session.post(self.webhook_url, json=notification)
            except Exception as e:
                print(f"Error sending webhook: {e}")

    async def _send_telegram(self, notification: Dict):
        """Send notification to Telegram"""
        if not (self.telegram_token and self.telegram_chat_id):
            return

        url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
        message = self._format_telegram_message(notification)
        
        async with aiohttp.ClientSession() as session:
            try:
                await session.post(url, json={
                    "chat_id": self.telegram_chat_id,
                    "text": message,
                    "parse_mode": "HTML"
                })
            except Exception as e:
                print(f"Error sending Telegram message: {e}")

    def _format_telegram_message(self, notification: Dict) -> str:
        """Format notification for Telegram"""
        level_emoji = {
            AlertLevel.INFO: "ℹ️",
            AlertLevel.WARNING: "⚠️",
            AlertLevel.ERROR: "❌",
            AlertLevel.CRITICAL: "🚨"
        }
        
        emoji = level_emoji.get(notification["level"], "ℹ️")
        timestamp = notification["timestamp"].strftime("%Y-%m-%d %H:%M:%S UTC")
        
        return f"{emoji} <b>{notification['level'].value.upper()}</b>\n\n{notification['message']}\n\n<i>{timestamp}</i>"