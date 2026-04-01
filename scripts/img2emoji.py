#!/usr/bin/env python3
"""将图片转为 emoji 色块画 — 体积极小，CC 不会折叠"""

import sys
from PIL import Image

# 用 Unicode 全角方块，不用 ANSI 颜色码
# 将颜色量化到有限调色板，用对应的 emoji/unicode 字符表示
PALETTE = [
    ((255,255,255), ' '),  # 白/透明
    ((240,230,210), '🟨'),  # 浅黄/米色 → 黄方块
    ((210,180,120), '🟧'),  # 棕黄 → 橙方块
    ((180,130,70),  '🟫'),  # 棕色
    ((140,100,50),  '🟫'),  # 深棕
    ((100,70,35),   '⬛'),  # 很深棕 → 黑
    ((50,50,50),    '⬛'),  # 黑
    ((200,200,200), '⬜'),  # 灰白
    ((160,160,160), '🔲'),  # 灰
    ((120,120,120), '🔳'),  # 深灰
    ((220,150,150), '🟥'),  # 粉红
    ((200,60,60),   '🟥'),  # 红
]

def closest_char(r, g, b, a):
    if a < 128 or (r > 245 and g > 245 and b > 245):
        return ' '
    best = ' '
    best_dist = float('inf')
    for (pr, pg, pb), ch in PALETTE:
        d = (r-pr)**2 + (g-pg)**2 + (b-pb)**2
        if d < best_dist:
            best_dist = d
            best = ch
    return best

def render(img_path, width=15):
    img = Image.open(img_path).convert("RGBA")
    aspect = img.height / img.width
    height = int(width * aspect * 0.55)  # emoji 是正方形，补偿比例
    img = img.resize((width, height), Image.LANCZOS)

    lines = []
    for y in range(height):
        line = ""
        for x in range(width):
            r, g, b, a = img.getpixel((x, y))
            line += closest_char(r, g, b, a)
        lines.append(line.rstrip())

    # 去掉首尾空行
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()

    return '\n'.join(lines)

if __name__ == '__main__':
    path = sys.argv[1]
    width = int(sys.argv[2]) if len(sys.argv) > 2 else 15
    print(render(path, width))
