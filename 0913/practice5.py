"""
practice5.py
整合 Gemini 聯網搜尋 + Telegram 推播功能（每日定時版）
每天早上 8:00 自動推播一次，支援結束日期或手動中斷（Ctrl+C）
所有推播內容皆記錄至 broadcast.log
"""

import asyncio
import logging
import os
import signal
import sys
from datetime import datetime, date, time as dtime
import pytz
from dotenv import load_dotenv
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from google import genai
from google.genai import types

load_dotenv()

# ── Log 設定 ─────────────────────────────────────────────────
LOG_FILE = os.path.join(os.path.dirname(__file__), "broadcast.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),   # 同時輸出到終端機
    ],
)
logger = logging.getLogger(__name__)
# ─────────────────────────────────────────────────────────────

# Telegram 設定
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TARGET_USER_ID = 8655981429
TARGET_GROUP_ID = "-1003906108658"
TARGET_CHANNEL_ID = "-1003723503676"

# Gemini 設定
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# ── 排程設定 ────────────────────────────────────────────────
TIMEZONE = pytz.timezone("Asia/Taipei")   # 台北時區
BROADCAST_HOUR = 8                         # 每天幾點推播
BROADCAST_MINUTE = 0                       # 幾分推播

# 結束日期：設定後到該日（含）最後一次推播後自動停止。
# 設為 None 表示無限期執行，直到手動 Ctrl+C。
END_DATE = date(2026, 12, 31)             # 例：date(2026, 12, 31)
# ─────────────────────────────────────────────────────────────

# 全域旗標，用於優雅結束
_stop_event: asyncio.Event | None = None


def _handle_signal(sig, frame):
    """收到 SIGINT / SIGTERM 時設定停止旗標"""
    logger.warning("收到結束訊號，準備停止排程...")
    if _stop_event:
        _stop_event.set()


async def send_text_broadcast(
    chat_id: str | int,
    text: str,
    keyboard: InlineKeyboardMarkup | None = None
):
    """
    發送純文字訊息推播
    :param chat_id: 目標聊天室 ID (個人/群組/頻道)
    :param text: 訊息內容 (支援 HTML 格式)
    :param keyboard: 訊息底部的按鈕 (選填)
    """
    bot = Bot(token=TELEGRAM_TOKEN)
    try:
        await bot.send_message(
            chat_id=chat_id,
            text=text,
            parse_mode=ParseMode.HTML,
            reply_markup=keyboard,
            disable_web_page_preview=False
        )
        logger.info("✅ 成功發送訊息至：%s", chat_id)
    except Exception as e:
        logger.error("❌ 發送至 %s 失敗：%s", chat_id, e)


def gemini_search(prompt: str) -> str:
    """
    使用 Gemini API 進行聯網搜尋
    :param prompt: 搜尋提示詞
    :return: Gemini 回應的文字內容
    """
    try:
        logger.info("💬 搜尋提示：%s", prompt)
        logger.info("🌐 Gemini 正在自主聯網搜尋最新資料中...")

        client = genai.Client(api_key=GEMINI_API_KEY)
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())],
            ),
        )

        logger.info("✅ 搜尋完成！")
        return response.text
    except Exception as e:
        logger.error("❌ Gemini 搜尋失敗：%s", e)
        return f"搜尋時發生錯誤：{e}"


async def do_broadcast():
    """執行一次完整的搜尋 + 推播流程"""
    now_str = datetime.now(TIMEZONE).strftime("%Y-%m-%d %H:%M")
    logger.info("📢 [%s] 開始今日推播...", now_str)

    # 1. 定義搜尋查詢
    search_prompt = (
        "請查詢並告訴我今天最新的重要國際精品新聞三則"
        "（包含發生時間與簡要說明），使用繁體中文，並用美觀的排版呈現。"
    )

    # 2. 執行 Gemini 聯網搜尋
    search_result = gemini_search(search_prompt)

    # 3. 格式化訊息
    message_text = (
        "🔍 <b>國際精品新聞快報</b>\n"
        "━━━━━━━━━━━━━━━━━\n\n"
        f"{search_result}\n\n"
        "━━━━━━━━━━━━━━━━━\n"
        "📡 <i>資料來源：Gemini 即時搜尋</i>"
    )

    # 4. 互動按鈕
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🛍️ 立即下單", url="https://t.me/Guotang_LV"),
            InlineKeyboardButton("💬 聯絡店長", url="https://t.me/Guotang_LV")
        ]
    ])

    # 5. 記錄推播內容至 log（去除 HTML tag 後的純文字）
    import re
    plain_text = re.sub(r"<[^>]+>", "", message_text)
    logger.info(
        "━━━━ 推播內容（發送至 %d 個目標）━━━━\n%s\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        len([TARGET_USER_ID, TARGET_GROUP_ID, TARGET_CHANNEL_ID]),
        plain_text,
    )

    # 6. 發送至所有目標
    targets = [TARGET_USER_ID, TARGET_GROUP_ID, TARGET_CHANNEL_ID]
    for chat_id in targets:
        await send_text_broadcast(chat_id, message_text, keyboard)
        await asyncio.sleep(1)

    logger.info("✅ [%s] 今日推播完成", now_str)


def seconds_until_next_broadcast() -> float:
    """計算距離下一次推播（今天或明天的 BROADCAST_HOUR:BROADCAST_MINUTE）還有幾秒"""
    now = datetime.now(TIMEZONE)
    target_today = TIMEZONE.localize(
        datetime.combine(now.date(), dtime(BROADCAST_HOUR, BROADCAST_MINUTE))
    )
    if now >= target_today:
        # 今天的時間已過，改為明天
        from datetime import timedelta
        target_today += timedelta(days=1)
    delta = target_today - now
    return delta.total_seconds()


async def scheduler():
    """主排程迴圈：每天 08:00 觸發一次推播"""
    global _stop_event
    _stop_event = asyncio.Event()

    # 監聽 Ctrl+C / kill 訊號
    signal.signal(signal.SIGINT, _handle_signal)
    signal.signal(signal.SIGTERM, _handle_signal)

    end_str = END_DATE.strftime("%Y-%m-%d") if END_DATE else "無限期"
    logger.info("🕐 排程已啟動，每天 %02d:%02d 推播一次", BROADCAST_HOUR, BROADCAST_MINUTE)
    logger.info("📅 結束日期：%s（Ctrl+C 可隨時手動結束）", end_str)
    logger.info("📝 Log 檔案位置：%s", LOG_FILE)

    while not _stop_event.is_set():
        wait_secs = seconds_until_next_broadcast()
        from datetime import timedelta
        next_dt = datetime.now(TIMEZONE) + timedelta(seconds=wait_secs)
        logger.info(
            "⏳ 下次推播時間：%s（%.1f 小時後）",
            next_dt.strftime("%Y-%m-%d %H:%M:%S"),
            wait_secs / 3600,
        )

        # 等待到推播時間，或提前收到停止訊號
        try:
            await asyncio.wait_for(_stop_event.wait(), timeout=wait_secs)
            break  # 收到停止訊號
        except asyncio.TimeoutError:
            pass   # 時間到，繼續執行推播

        if _stop_event.is_set():
            break

        # 檢查是否超過結束日期
        today = datetime.now(TIMEZONE).date()
        if END_DATE and today > END_DATE:
            logger.info("📅 已超過結束日期 %s，排程自動停止。", end_str)
            break

        # 執行推播
        await do_broadcast()

        # 再次確認是否為最後一次（推播完當天即結束日）
        today = datetime.now(TIMEZONE).date()
        if END_DATE and today >= END_DATE:
            logger.info("📅 已完成結束日 %s 的推播，排程自動停止。", end_str)
            break

    logger.info("🛑 排程已結束，程式退出。")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        # 測試模式：立即執行一次推播，不等排程
        logger.info("🧪 測試模式啟動，立即執行一次推播...")
        asyncio.run(do_broadcast())
        logger.info("🧪 測試完成，請至 Telegram 確認是否收到訊息。")
    else:
        asyncio.run(scheduler())
