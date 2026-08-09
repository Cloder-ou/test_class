import random
import time

# ── 猜數字遊戲 ──────────────────────────────────────────────────────────────
# 電腦偷偷想一個 1～100 之間的數字，挑戰你幾步猜中！

TITLE = r"""
  _____                   _   _                 _
 / ____|                 | \ | |               | |
| |  __ _   _  ___  ___  |  \| |_   _ _ __ ___ | |__   ___ _ __
| | |_ | | | |/ _ \/ __| | . ` | | | | '_ ` _ \| '_ \ / _ \ '__|
| |__| | |_| |  __/\__ \ | |\  | |_| | | | | | | |_) |  __/ |
 \_____|\__,_|\___||___/ |_| \_|\__,_|_| |_| |_|_.__/ \___|_|
"""

FACES = {
    "too_low":  "(＞﹏＜)  太小了！往上猜～",
    "too_high": "(╬ Ò益Ó)  太大了！往下猜～",
    "perfect":  "٩(◕‿◕｡)۶  答對了！你是讀心術大師！",
}

MAX_GUESSES = 7


def slow_print(text: str, delay: float = 0.03) -> None:
    """逐字慢慢印出，增加戲劇感。"""
    for ch in text:
        print(ch, end="", flush=True)
        time.sleep(delay)
    print()


def play() -> None:
    print(TITLE)
    slow_print("歡迎來到猜數字遊戲！電腦已經偷偷想好一個 1～100 的整數……")
    slow_print(f"你只有 {MAX_GUESSES} 次機會，挑戰開始！\n")

    secret = random.randint(1, 100)
    history: list[int] = []

    for attempt in range(1, MAX_GUESSES + 1):
        # ── 提示剩餘次數與進度條 ──────────────────────
        remaining = MAX_GUESSES - attempt + 1
        bar = "❤️ " * remaining + "🖤 " * (MAX_GUESSES - remaining)
        print(f"\n第 {attempt} 次  {bar}")

        # ── 讀取輸入 ──────────────────────────────────
        try:
            guess = int(input("  你的猜測："))
        except ValueError:
            print("  請輸入一個整數！這次不算哦 >.< ")
            continue

        history.append(guess)

        # ── 判斷結果 ──────────────────────────────────
        if guess < secret:
            print(f"  {FACES['too_low']}")
        elif guess > secret:
            print(f"  {FACES['too_high']}")
        else:
            slow_print(f"\n  🎉 {FACES['perfect']}")
            slow_print(f"  答案正是 {secret}，你用了 {attempt} 步！")
            _show_history(history, secret)
            return

    # ── 挑戰失敗 ──────────────────────────────────────
    slow_print(f"\n  (╯°□°）╯︵ ┻━┻  用完次數啦！答案是 {secret}。")
    slow_print("  下次一定可以的！再來一局吧～")
    _show_history(history, secret)


def _show_history(history: list[int], secret: int) -> None:
    """顯示猜測歷程折線（純文字版）。"""
    if not history:
        return
    print("\n  ── 你的猜測歷程 ──")
    for i, val in enumerate(history, 1):
        diff = val - secret
        arrow = "↑" if diff < 0 else ("↓" if diff > 0 else "✓")
        bar = "█" * (abs(diff) // 5 + 1)
        print(f"  第{i:2d}次  {val:3d}  {arrow} {bar}")
    print()


if __name__ == "__main__":
    while True:
        play()
        again = input("再玩一局？(y/n)：").strip().lower()
        if again != "y":
            slow_print("\n掰掰！有空再來玩 (´▽`)/~~\n")
            break
