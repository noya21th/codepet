#!/usr/bin/env python3
"""一次性展示全部 36 张角色表情的终端像素画"""

import os, sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from img2terminal import render_image
from PIL import Image

SPRITE_DIR = os.path.join(SCRIPT_DIR, "..", "sprites")
RESET = "\033[0m"
BOLD = "\033[1m"

CHARS = ["bibilabu", "bagayalu", "wodedaodun", "bababoyi", "waibibabu", "gugugaga"]
NAMES = {"bibilabu": "比比拉布", "bagayalu": "八嘎呀路", "wodedaodun": "我的刀盾", "bababoyi": "巴巴博一", "waibibabu": "歪比巴卜", "gugugaga": "咕咕嘎嘎"}
EXPRS = ["normal", "happy", "sleep", "eat", "pet", "worry"]
EXPR_ZH = {"normal": "普通", "happy": "开心", "sleep": "睡觉", "eat": "吃东西", "pet": "被撸", "worry": "焦虑"}

width = int(sys.argv[1]) if len(sys.argv) > 1 else 25

print()
print(f"  ═══════════════════════════════════════════")
print(f"    🐾 {BOLD}CodePet 全部 36 张角色表情{RESET}")
print(f"  ═══════════════════════════════════════════")

for char in CHARS:
    print(f"\n  {BOLD}【{NAMES[char]}】{RESET}")
    for expr in EXPRS:
        path = os.path.join(SPRITE_DIR, char, f"{expr}.png")
        if not os.path.exists(path):
            print(f"    {EXPR_ZH[expr]}: 缺失")
            continue
        img = Image.open(path)
        print(f"\n    {EXPR_ZH[expr]}:")
        result = render_image(img, width)
        for line in result.splitlines():
            print(f"      {line}")
    print(f"\n  {'─' * 44}")

print()
