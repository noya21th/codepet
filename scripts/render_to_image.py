#!/usr/bin/env python3
"""将角色渲染为 PNG 图片，供 Claude Code 直接读取显示"""

import os, sys
from PIL import Image

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SPRITE_DIR = os.path.join(SCRIPT_DIR, "..", "sprites")
PET_DIR = os.path.join(os.path.expanduser("~"), ".codepet")

def render_to_png(character, variant='normal', output_path=None):
    """将角色图片缩放到合适大小并保存为 PNG"""
    # 优先用变体图
    src = os.path.join(SPRITE_DIR, character, f"{variant}.png")
    if not os.path.exists(src):
        src = os.path.join(SPRITE_DIR, f"{character}.png")
    if not os.path.exists(src):
        print(f"图片不存在: {src}")
        return None

    img = Image.open(src).convert("RGBA")

    # 缩放到合适展示尺寸（宽度 400px）
    target_w = 400
    ratio = target_w / img.width
    target_h = int(img.height * ratio)
    img = img.resize((target_w, target_h), Image.LANCZOS)

    # 白色背景替换为透明（如果需要）
    # 保持原样即可

    if not output_path:
        os.makedirs(PET_DIR, exist_ok=True)
        output_path = os.path.join(PET_DIR, "display.png")

    img.save(output_path)
    return output_path

if __name__ == '__main__':
    character = sys.argv[1] if len(sys.argv) > 1 else 'gugugaga'
    variant = sys.argv[2] if len(sys.argv) > 2 else 'normal'
    path = render_to_png(character, variant)
    if path:
        print(path)
