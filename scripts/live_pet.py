#!/usr/bin/env python3
"""CodePet 常驻窗口 — 微动画让宠物看起来像活的"""

import sys, os, json, time, random, copy

# Windows ANSI support
if sys.platform == 'win32':
    try:
        import ctypes
        ctypes.windll.kernel32.SetConsoleMode(ctypes.windll.kernel32.GetStdHandle(-11), 7)
    except: pass

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from img2terminal import render_image
from PIL import Image

SPRITE_DIR = os.path.join(SCRIPT_DIR, "..", "sprites")
PET_JSON = os.path.join(os.path.expanduser("~"), ".codepet", "pet.json")

HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"
CLEAR = "\033[2J\033[H"
RESET = "\033[0m"

# Character-specific idle lines
IDLE_LINES = {
    'bibilabu': ['……', '（调整香蕉皮）', '（发呆中）', '（打了个小哈欠）'],
    'bagayalu': ['……', '（眨了下眼）', '（纹丝不动）', '（鼻子哼了一声）'],
    'wodedaodun': ['zzZ', '（翻了个身）', '（梦中抽了下爪子）', 'zzZ...zzZ...'],
    'bababoyi': ['（盯——）', '（歪头）', '（眨了下大眼睛）', '咕？'],
    'waibibabu': ['（抱胸）', '（推了推墨镜）', '哼。', '（叼起牙签）'],
    'gugugaga': ['（刘海飘了一下）', '嘎。', '（拍了拍翅膀）', '（歪头）'],
}

def load_pet():
    try:
        with open(PET_JSON, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return None

def create_micro_variation(img, num_changes=5):
    """Create a subtle variation of the image by shifting a few pixels"""
    varied = img.copy()
    w, h = varied.size
    for _ in range(num_changes):
        x = random.randint(1, w-2)
        y = random.randint(1, h-2)
        px = varied.getpixel((x, y))
        if px[3] < 128:  # skip transparent
            continue
        # Slightly shift color
        r = max(0, min(255, px[0] + random.randint(-8, 8)))
        g = max(0, min(255, px[1] + random.randint(-8, 8)))
        b = max(0, min(255, px[2] + random.randint(-8, 8)))
        varied.putpixel((x, y), (r, g, b, px[3]))
    return varied

def main():
    pet = load_pet()
    if not pet:
        print("还没有宠物。先运行 codepet hatch")
        return

    character = pet.get('character', 'bagayalu')
    name = pet.get('nickname', pet.get('name', character))
    mood = pet.get('mood', '清醒')

    # Load base image
    scene = 'normal'
    if mood == 'sleep' or mood == '睡觉':
        scene = 'sleep'
    elif mood == 'worry' or mood == '焦虑':
        scene = 'worry'
    elif mood == 'happy' or mood == '开心':
        scene = 'happy'

    img_path = os.path.join(SPRITE_DIR, character, f"{scene}.png")
    if not os.path.exists(img_path):
        img_path = os.path.join(SPRITE_DIR, f"{character}.png")

    base_img = Image.open(img_path).convert("RGBA")

    # Render size
    width = 35

    idle_lines = IDLE_LINES.get(character, ['……'])

    print(HIDE_CURSOR, end="")
    print(CLEAR, end="")

    # Pre-render base frame to count lines
    base_render = render_image(base_img, width)
    base_lines = base_render.splitlines()
    total_display_lines = len(base_lines) + 5  # image + status lines

    last_bubble_time = 0
    bubble_text = ""
    bubble_show_until = 0
    frame = 0

    try:
        while True:
            # Create micro-variation
            varied = create_micro_variation(base_img, num_changes=random.randint(3, 8))
            rendered = render_image(varied, width)
            lines = rendered.splitlines()

            # Move cursor to top
            print("\033[H", end="")

            # Print frame
            print(f"\n  🐾 {name}", end="")
            print(f"{'':>20}", end="")  # clear rest of line
            print()
            print()

            for line in lines:
                print(f"  {line}  ")  # extra spaces to clear artifacts

            print()

            # Status line
            now = time.time()
            hour = time.localtime().tm_hour
            if 0 <= hour < 6:
                time_mood = "🌙 深夜"
            elif 6 <= hour < 9:
                time_mood = "🌅 早晨"
            elif 9 <= hour < 18:
                time_mood = "☀️ 工作中"
            elif 18 <= hour < 22:
                time_mood = "🌆 傍晚"
            else:
                time_mood = "🌙 夜晚"

            print(f"  {time_mood} · Lv.{pet.get('level', 1)} · 经验 {pet.get('exp', 0)}" + "    ")

            # Bubble (occasional dialogue)
            if now > bubble_show_until:
                bubble_text = ""

            if now - last_bubble_time > random.randint(25, 50) and not bubble_text:
                bubble_text = random.choice(idle_lines)
                last_bubble_time = now
                bubble_show_until = now + 5

            if bubble_text:
                print(f"\n  💬 {bubble_text}" + "    ")
            else:
                print(f"\n{'':>30}")  # clear bubble line

            sys.stdout.flush()

            # Wait
            time.sleep(random.uniform(1.2, 2.0))
            frame += 1

            # Reload pet data every 30 frames (~45 seconds)
            if frame % 30 == 0:
                pet = load_pet() or pet

    except KeyboardInterrupt:
        pass
    finally:
        print(SHOW_CURSOR)
        print(CLEAR)
        print(f"  {name} 回窝了。\n")

if __name__ == '__main__':
    main()
