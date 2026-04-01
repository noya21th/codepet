#!/usr/bin/env python3
"""将角色图片转为小尺寸 ASCII 字符画 — 保证与角色一致"""

import sys
from PIL import Image

# 亮度到字符映射（从亮到暗）
CHARS = " .:-=+*#%@█"

def render(img_path, width=20):
    img = Image.open(img_path).convert("RGBA")
    aspect = img.height / img.width
    height = int(width * aspect * 0.5)  # 字符高宽比补偿
    img = img.resize((width, height), Image.LANCZOS)

    lines = []
    for y in range(height):
        line = ""
        for x in range(width):
            r, g, b, a = img.getpixel((x, y))
            if a < 128 or (r > 245 and g > 245 and b > 245):
                line += " "
            else:
                brightness = (r * 299 + g * 587 + b * 114) / 1000
                idx = int(brightness / 255 * (len(CHARS) - 1))
                line += CHARS[len(CHARS) - 1 - idx]  # 反转：暗=密字符

        lines.append(line.rstrip())

    # 去首尾空行
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()

    return '\n'.join(lines)

if __name__ == '__main__':
    path = sys.argv[1]
    width = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    print(render(path, width))
