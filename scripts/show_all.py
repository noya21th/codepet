#!/usr/bin/env python3
"""一键展示所有 CodePet 角色的终端像素画"""

import os, sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from img2terminal import render_image
from PIL import Image

SPRITE_DIR = os.path.join(SCRIPT_DIR, "..", "sprites")
RESET = "\033[0m"
BOLD = "\033[1m"

chars = [
    ("bibilabu",    "比比拉布", ""),
    ("bagayalu",    "八嘎呀路", ""),
    ("wodedaodun",  "我的刀盾", ""),
    ("bababoyi",    "巴巴博一", ""),
    ("waibibabu",   "歪比巴卜", ""),
    ("gugugaga",    "咕咕嘎嘎", ""),
]

width = int(sys.argv[1]) if len(sys.argv) > 1 else 45

print()
print(f"  ═══════════════════════════════════════")
print(f"    🐾 {BOLD}CodePet 角色画廊{RESET}（终端像素画）")
print(f"  ═══════════════════════════════════════")

for eng, zh, desc in chars:
    img_path = os.path.join(SPRITE_DIR, f"{eng}.png")
    if not os.path.exists(img_path):
        print(f"\n  [!] {zh} 图片不存在: {img_path}")
        continue
    img = Image.open(img_path)
    label = f"\n  {BOLD}{zh}{RESET}" + (f"（{desc}）" if desc else "")
    print(label)
    result = render_image(img, width)
    for line in result.splitlines():
        print(f"    {line}")
    print(f"  {'─' * 40}")

print()
