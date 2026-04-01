#!/usr/bin/env python3
"""从基础图片自动生成 6 个场景变体"""

import os, sys
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw, ImageFont

SPRITE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sprites")

CHARACTERS = ['bibilabu', 'bagayalu', 'wodedaodun', 'bababoyi', 'waibibabu', 'gugugaga']

# 6 个场景
VARIANTS = {
    'normal':  '普通',
    'happy':   '开心',
    'sleep':   '睡觉',
    'eat':     '吃东西',
    'pet':     '被撸',
    'worry':   '焦虑',
}

def make_happy(img):
    """开心：提亮 + 暖色调"""
    enhancer = ImageEnhance.Brightness(img)
    bright = enhancer.enhance(1.15)
    # 暖色：增加红黄
    r, g, b, a = bright.split()
    r = r.point(lambda x: min(255, int(x * 1.05)))
    g = g.point(lambda x: min(255, int(x * 1.02)))
    return Image.merge('RGBA', (r, g, b, a))

def make_sleep(img):
    """睡觉：变暗 + 轻微模糊"""
    enhancer = ImageEnhance.Brightness(img)
    dark = enhancer.enhance(0.8)
    enhancer2 = ImageEnhance.Color(dark)
    desat = enhancer2.enhance(0.7)
    return desat.filter(ImageFilter.GaussianBlur(radius=0.5))

def make_eat(img):
    """吃东西：微微歪头（旋转 3 度）"""
    rotated = img.rotate(-3, expand=False, fillcolor=(255, 255, 255, 0))
    # 稍微提亮（吃东西开心）
    enhancer = ImageEnhance.Brightness(rotated)
    return enhancer.enhance(1.08)

def make_pet(img):
    """被撸：温暖色调 + 轻微放大"""
    w, h = img.size
    # 轻微放大 5%
    new_w, new_h = int(w * 1.05), int(h * 1.05)
    big = img.resize((new_w, new_h), Image.LANCZOS)
    # 裁回原尺寸（居中）
    left = (new_w - w) // 2
    top = (new_h - h) // 2
    cropped = big.crop((left, top, left + w, top + h))
    # 暖色
    enhancer = ImageEnhance.Color(cropped)
    warm = enhancer.enhance(1.1)
    enhancer2 = ImageEnhance.Brightness(warm)
    return enhancer2.enhance(1.1)

def make_worry(img):
    """焦虑：冷色调 + 轻微缩小"""
    # 冷色：增蓝减红
    r, g, b, a = img.split()
    r = r.point(lambda x: int(x * 0.92))
    b = b.point(lambda x: min(255, int(x * 1.08)))
    cold = Image.merge('RGBA', (r, g, b, a))
    # 轻微降低饱和
    enhancer = ImageEnhance.Color(cold)
    return enhancer.enhance(0.85)

GENERATORS = {
    'normal': lambda img: img.copy(),
    'happy':  make_happy,
    'sleep':  make_sleep,
    'eat':    make_eat,
    'pet':    make_pet,
    'worry':  make_worry,
}

def generate_all():
    total = 0
    for char in CHARACTERS:
        base_path = os.path.join(SPRITE_DIR, f"{char}.png")
        if not os.path.exists(base_path):
            print(f"  [!] 跳过 {char}：基础图片不存在")
            continue

        base = Image.open(base_path).convert("RGBA")
        var_dir = os.path.join(SPRITE_DIR, char)
        os.makedirs(var_dir, exist_ok=True)

        for variant, zh_name in VARIANTS.items():
            gen = GENERATORS[variant]
            result = gen(base)
            out_path = os.path.join(var_dir, f"{variant}.png")
            result.save(out_path)
            total += 1

        print(f"  ✓ {char} — {len(VARIANTS)} 个变体")

    print(f"\n  共生成 {total} 张图片，保存到 {SPRITE_DIR}/[角色名]/")

if __name__ == '__main__':
    print("\n  🎨 生成角色场景变体...\n")
    generate_all()
