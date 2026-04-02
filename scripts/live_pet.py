#!/usr/bin/env python3
"""CodePet 常驻窗口 — 微动画让宠物看起来像活的"""

import sys, os, json, time, random, re

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

IDLE_LINES = {
    'bibilabu': ['……', '（调整香蕉皮）', '（发呆中）', '（打了个小哈欠）', '（尾巴动了一下）'],
    'bagayalu': ['……', '（眨了下眼）', '（纹丝不动）', '（鼻子哼了一声）', '（换了只脚重心）'],
    'wodedaodun': ['zzZ', '（翻了个身）', '（梦中抽了下爪子）', 'zzZ...zzZ...', '（打了个巨大的哈欠）'],
    'bababoyi': ['（盯——）', '（歪头）', '（眨了下大眼睛）', '咕？', '（羽毛蓬了一下）'],
    'waibibabu': ['（抱胸）', '（推了推墨镜）', '哼。', '（叼起牙签）', '（换了个站姿）'],
    'gugugaga': ['（刘海飘了一下）', '嘎。', '（拍了拍翅膀）', '（歪头）', '（小脚踩了踩地面）'],
}

def load_pet():
    try:
        with open(PET_JSON, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return None

ANSI_RE = re.compile(r'\033\[[0-9;]*m')

def tweak_rendered_lines(lines):
    """在终端渲染后的行层面做微动画——随机偏移、闪烁"""
    result = list(lines)
    if len(result) < 4:
        return result

    # 随机选 2-4 行做微调
    for _ in range(random.randint(2, 4)):
        idx = random.randint(1, len(result) - 2)
        action = random.random()

        if action < 0.25:
            # 整行右移 1 格
            result[idx] = ' ' + result[idx]
        elif action < 0.5:
            # 整行左移 1 格
            if result[idx].startswith('  '):
                result[idx] = result[idx][1:]
        elif action < 0.75:
            # 整体上移效果：跟上一行交换
            if idx > 1:
                result[idx], result[idx-1] = result[idx-1], result[idx]
        # 其余什么都不做（保持静止）

    return result

def main():
    pet = load_pet()
    if not pet:
        print("还没有宠物。先运行 codepet hatch")
        return

    character = pet.get('character', 'bagayalu')
    name = pet.get('nickname', pet.get('name', character))
    mood = pet.get('mood', '清醒')

    scene = 'normal'
    if mood in ('sleep', '睡觉'):
        scene = 'sleep'
    elif mood in ('worry', '焦虑'):
        scene = 'worry'
    elif mood in ('happy', '开心'):
        scene = 'happy'

    img_path = os.path.join(SPRITE_DIR, character, f"{scene}.png")
    if not os.path.exists(img_path):
        img_path = os.path.join(SPRITE_DIR, f"{character}.png")

    base_img = Image.open(img_path).convert("RGBA")
    width = 35

    idle_lines = IDLE_LINES.get(character, ['……'])

    # 预渲染基础帧
    base_render = render_image(base_img, width)
    base_lines = base_render.splitlines()

    print(HIDE_CURSOR, end="")
    print(CLEAR, end="")

    last_bubble_time = 0
    bubble_text = ""
    bubble_show_until = 0
    frame = 0
    # 记录输出总行数用于光标回退
    output_lines = len(base_lines) + 8

    try:
        while True:
            # 每 5 帧做一次微调，其余帧显示原图（呼吸节奏感）
            if frame % 5 in (2, 3):
                display_lines = tweak_rendered_lines(base_lines)
            else:
                display_lines = base_lines

            # 光标回到顶部
            print("\033[H", end="")

            # 名字
            print(f"\n  🐾 {name}{'':>30}")
            print()

            # 像素画
            for line in display_lines:
                print(f"  {line}  ")

            print()

            # 时段
            hour = time.localtime().tm_hour
            if 0 <= hour < 6:
                tm = "🌙 深夜"
            elif 6 <= hour < 9:
                tm = "🌅 早晨"
            elif 9 <= hour < 18:
                tm = "☀️ 工作中"
            elif 18 <= hour < 22:
                tm = "🌆 傍晚"
            else:
                tm = "🌙 夜晚"

            print(f"  {tm} · Lv.{pet.get('level', 1)} · 经验 {pet.get('exp', 0)}{'':>10}")

            # 气泡
            now = time.time()
            if now > bubble_show_until:
                bubble_text = ""
            if now - last_bubble_time > random.randint(20, 40) and not bubble_text:
                bubble_text = random.choice(idle_lines)
                last_bubble_time = now
                bubble_show_until = now + 5

            if bubble_text:
                print(f"\n  💬 {bubble_text}{'':>20}")
            else:
                print(f"\n{'':>40}")

            sys.stdout.flush()
            time.sleep(random.uniform(0.8, 1.5))
            frame += 1

            # 每 60 帧重新读宠物数据
            if frame % 60 == 0:
                pet = load_pet() or pet

    except KeyboardInterrupt:
        pass
    finally:
        print(SHOW_CURSOR)
        print(CLEAR)
        print(f"  {name} 回窝了。\n")

if __name__ == '__main__':
    main()
