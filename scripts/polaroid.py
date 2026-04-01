#!/usr/bin/env python3
"""拍立得相框效果 — 逐行慢显示，静态，边框对齐"""

import sys, os, json, time, re, wcwidth

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from img2terminal import render_image
from PIL import Image

SPRITE_DIR = os.path.join(SCRIPT_DIR, "..", "sprites")
PET_JSON = os.path.join(os.path.expanduser("~"), ".codepet", "pet.json")

SCENE_ZH = {
    'normal': '日常', 'happy': '开心的瞬间', 'sleep': '睡着了',
    'eat': '在吃东西', 'pet': '被摸摸的样子', 'worry': '有点紧张',
}

_ANSI_RE = re.compile(r'\033\[[0-9;]*m')

def display_width(s):
    """Return the visible column width of *s* after stripping ANSI escapes.

    Uses wcwidth for accurate terminal column widths:
      - half-block chars (▀▄█) and box-drawing (─│┌┐└┘) = 1 column
      - CJK / fullwidth chars = 2 columns
      - emoji (📸🐋 etc.) = 2 columns
      - control / zero-width chars = 0 columns
    """
    clean = _ANSI_RE.sub('', s)
    w = 0
    for ch in clean:
        cw = wcwidth.wcwidth(ch)
        if cw < 0:          # non-printable / control char
            cw = 0
        w += cw
    return w

def pad_to(content, target_width):
    """Pad *content* with trailing spaces so its visible width equals *target_width*."""
    dw = display_width(content)
    diff = target_width - dw
    if diff > 0:
        return content + ' ' * diff
    return content

def main():
    character = sys.argv[1] if len(sys.argv) > 1 else 'bagayalu'
    scene = sys.argv[2] if len(sys.argv) > 2 else 'normal'
    width = int(sys.argv[3]) if len(sys.argv) > 3 else 40

    img_path = os.path.join(SPRITE_DIR, character, f"{scene}.png")
    if not os.path.exists(img_path):
        img_path = os.path.join(SPRITE_DIR, f"{character}.png")

    name = character
    try:
        with open(PET_JSON) as f:
            pet = json.load(f)
            name = pet.get('nickname', pet.get('name', character))
    except:
        pass

    scene_zh = SCENE_ZH.get(scene, '一个瞬间')
    img = Image.open(img_path).convert("RGBA")
    pixel_lines = render_image(img, width).splitlines()

    R = "\033[0m"
    W = "\033[38;2;120;120;120m"

    max_pw = max(display_width(l) for l in pixel_lines) if pixel_lines else width
    caption = f"📸 刚才抓拍到了{name}{scene_zh}..."
    studio = "🐋 Ai小蓝鲸照相馆"
    inner_w = max(max_pw + 6, display_width(caption) + 6, display_width(studio) + 6)
    border = "─" * inner_w

    def fl(content=""):
        return f"  {W}│{R}{pad_to(content, inner_w)}{W}│{R}"

    total = len(pixel_lines) + 10
    delay = 7.0 / max(total, 1)

    # 输出尺寸
    print(f"ROWS:{total + 4} COLS:{inner_w + 8}", file=sys.stderr)

    print()
    print(f"  {W}┌{border}┐{R}"); sys.stdout.flush(); time.sleep(delay)
    print(fl()); sys.stdout.flush(); time.sleep(delay)

    for line in pixel_lines:
        print(fl("   " + line)); sys.stdout.flush(); time.sleep(delay)

    print(fl()); sys.stdout.flush(); time.sleep(delay)
    print(fl()); sys.stdout.flush(); time.sleep(delay)
    print(fl("  " + caption)); sys.stdout.flush(); time.sleep(delay)
    print(fl()); sys.stdout.flush(); time.sleep(delay)
    print(fl("  " + studio)); sys.stdout.flush(); time.sleep(0.3)
    print(fl()); sys.stdout.flush(); time.sleep(0.2)
    print(f"  {W}└{border}┘{R}"); sys.stdout.flush()
    print()

if __name__ == '__main__':
    main()
