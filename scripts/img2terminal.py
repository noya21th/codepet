#!/usr/bin/env python3
"""
将图片转为终端像素画（半块字符 ▀▄█ + RGB 真彩色）

Windows ANSI 支持自动开启。
用法:
  python3 img2terminal.py <图片路径> [宽度] [--no-bg]
  python3 img2terminal.py crop <图片路径> <x> <y> <w> <h> [终端宽度]
"""

import sys
from PIL import Image

# Windows: 强制开启 ANSI 彩色支持
if sys.platform == 'win32':
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except:
        pass

UPPER_HALF = "▀"
LOWER_HALF = "▄"
FULL_BLOCK = "█"

def fg(r, g, b):
    return f"\033[38;2;{r};{g};{b}m"

def bg(r, g, b):
    return f"\033[48;2;{r};{g};{b}m"

RESET = "\033[0m"

def is_transparent_or_white(pixel, threshold=245):
    """判断像素是否接近白色/透明（当作背景）"""
    if len(pixel) == 4 and pixel[3] < 128:
        return True
    return pixel[0] > threshold and pixel[1] > threshold and pixel[2] > threshold

def render_image(img, term_width=30, remove_bg=True):
    """将 PIL Image 渲染为终端像素画"""
    # 调整大小：宽度=term_width字符，高度按比例（每字符=2像素高）
    aspect = img.height / img.width
    pixel_w = term_width
    pixel_h = int(term_width * aspect * 1.7)  # 1.7 补偿字符高宽比，比2更胖
    if pixel_h % 2 == 1:
        pixel_h += 1

    img = img.convert("RGBA").resize((pixel_w, pixel_h), Image.LANCZOS)

    lines = []
    for y in range(0, pixel_h, 2):
        line = ""
        for x in range(pixel_w):
            top = img.getpixel((x, y))
            bot = img.getpixel((x, y + 1)) if y + 1 < pixel_h else (255, 255, 255, 0)

            top_bg = remove_bg and is_transparent_or_white(top)
            bot_bg = remove_bg and is_transparent_or_white(bot)

            if top_bg and bot_bg:
                line += " "
            elif top_bg:
                line += f"{fg(bot[0], bot[1], bot[2])}{LOWER_HALF}{RESET}"
            elif bot_bg:
                line += f"{fg(top[0], top[1], top[2])}{UPPER_HALF}{RESET}"
            elif top[:3] == bot[:3]:
                line += f"{fg(top[0], top[1], top[2])}{FULL_BLOCK}{RESET}"
            else:
                line += f"{fg(top[0], top[1], top[2])}{bg(bot[0], bot[1], bot[2])}{UPPER_HALF}{RESET}"
        lines.append(line)

    return "\n".join(lines)

def main():
    if len(sys.argv) < 2:
        print("用法:")
        print("  python3 img2terminal.py <图片> [宽度]")
        print("  python3 img2terminal.py crop <图片> <x> <y> <w> <h> [宽度]")
        sys.exit(1)

    if sys.argv[1] == "crop":
        # 裁切模式
        img_path = sys.argv[2]
        x, y, w, h = int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
        term_width = int(sys.argv[7]) if len(sys.argv) > 7 else 30
        img = Image.open(img_path)
        img = img.crop((x, y, x + w, y + h))
        print(render_image(img, term_width))
    else:
        # 整图模式
        img_path = sys.argv[1]
        term_width = int(sys.argv[2]) if len(sys.argv) > 2 else 40
        img = Image.open(img_path)
        print(render_image(img, term_width))

if __name__ == "__main__":
    main()
