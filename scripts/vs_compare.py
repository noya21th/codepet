#!/usr/bin/env python3
"""
CodePet VS 对比图生成器
两只宠物并排对比，突出属性优劣
用法: python vs_compare.py [other_pet.json]
"""

import os
import sys
import json
import platform
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# ─── Paths ───────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SPRITE_DIR = os.path.join(SCRIPT_DIR, "..", "sprites")
PET_JSON = os.path.join(os.path.expanduser("~"), ".codepet", "pet.json")
OUTPUT_PATH = os.path.join(os.path.expanduser("~"), ".codepet", "vs_compare.png")

# ─── Design tokens ──────────────────────────────────────────────────────────
CARD_W, CARD_H = 900, 500

TEXT_DARK = (40, 40, 45)
TEXT_MED = (120, 118, 115)
TEXT_LIGHT = (170, 168, 165)
GOLD_STAR = (255, 195, 0)
EMPTY_STAR = (210, 208, 204)
BAR_TRACK = (230, 228, 225)
WIN_COLOR = (72, 200, 97)

RARITY_COLORS = {
    "普通": (160, 160, 160),
    "优秀": (72, 180, 97),
    "稀有": (66, 135, 245),
    "史诗": (168, 85, 247),
    "传说": (255, 160, 30),
}

STAT_COLORS = {
    "调试力": (255, 80, 80),
    "耐心值": (66, 135, 245),
    "混沌值": (168, 85, 247),
    "智慧值": (72, 180, 97),
    "毒舌值": (255, 160, 30),
}


# ─── Font loading (same as pet_card.py) ─────────────────────────────────────
def load_font(size, bold=False):
    system = platform.system()
    candidates = []
    if system == "Darwin":
        candidates = [
            "/System/Library/Fonts/PingFang.ttc",
            "/System/Library/Fonts/STHeiti Light.ttc",
            "/System/Library/Fonts/Hiragino Sans GB.ttc",
            "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        ]
    elif system == "Windows":
        winfonts = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts")
        candidates = [
            os.path.join(winfonts, "msyh.ttc"),
            os.path.join(winfonts, "msyhbd.ttc"),
            os.path.join(winfonts, "simhei.ttf"),
            os.path.join(winfonts, "simsun.ttc"),
        ]
    else:
        candidates = [
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/google-noto-cjk/NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/wenquanyi/wqy-microhei/wqy-microhei.ttc",
            "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ]
    font_index = 1 if bold else 0
    for fpath in candidates:
        if os.path.exists(fpath):
            try:
                return ImageFont.truetype(fpath, size, index=font_index)
            except Exception:
                try:
                    return ImageFont.truetype(fpath, size, index=0)
                except Exception:
                    continue
    return ImageFont.load_default()


def draw_rounded_rect(draw, xy, radius, fill=None, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def draw_gradient_bg(img):
    """Light blue-grey gradient."""
    draw = ImageDraw.Draw(img)
    top = (235, 240, 248)
    bottom = (225, 228, 238)
    for y in range(CARD_H):
        ratio = y / CARD_H
        r = int(top[0] + (bottom[0] - top[0]) * ratio)
        g = int(top[1] + (bottom[1] - top[1]) * ratio)
        b = int(top[2] + (bottom[2] - top[2]) * ratio)
        draw.line((0, y, CARD_W, y), fill=(r, g, b))


def load_sprite(character):
    sprite_path = os.path.join(SPRITE_DIR, character, "normal.png")
    if not os.path.exists(sprite_path):
        sprite_path = os.path.join(SPRITE_DIR, f"{character}.png")
    if not os.path.exists(sprite_path):
        return None
    return Image.open(sprite_path).convert("RGBA")


def draw_pet_side(card, draw, pet_data, x_start, w, fonts, is_placeholder=False):
    """Draw one pet's info on a side of the card."""
    font_name, font_sm, font_xs, font_star, font_rarity, font_level = fonts

    cx = x_start + w // 2  # center x
    y = 20

    if is_placeholder:
        # Draw "???" placeholder
        q_text = "???"
        q_bbox = font_name.getbbox(q_text)
        q_w = q_bbox[2] - q_bbox[0]
        draw.text((cx - q_w // 2, 120), q_text, fill=TEXT_LIGHT, font=font_name)

        hint = "等你来挑战"
        hint_bbox = font_sm.getbbox(hint)
        hint_w = hint_bbox[2] - hint_bbox[0]
        draw.text((cx - hint_w // 2, 200), hint, fill=TEXT_LIGHT, font=font_sm)
        return {}

    name = pet_data.get("nickname") or pet_data.get("name", "???")
    character = pet_data.get("character", "bagayalu")
    rarity = pet_data.get("rarity", "普通")
    stars = pet_data.get("stars", 1)
    level = pet_data.get("level", 1)
    stats = pet_data.get("stats", {})

    # Sprite
    sprite = load_sprite(character)
    if sprite:
        sprite_h = 110
        scale = sprite_h / sprite.height
        sprite_w = int(sprite.width * scale)
        sprite_resized = sprite.resize((sprite_w, sprite_h), Image.Resampling.NEAREST)
        sprite_x = cx - sprite_w // 2
        card.paste(sprite_resized, (sprite_x, y), sprite_resized)
    y += 118

    # Name
    name_bbox = font_name.getbbox(name)
    name_w = name_bbox[2] - name_bbox[0]
    draw = ImageDraw.Draw(card)
    draw.text((cx - name_w // 2, y), name, fill=TEXT_DARK, font=font_name)
    y += 30

    # Stars
    max_stars = 5
    star_str = "★" * stars + "☆" * (max_stars - stars)
    star_bbox = font_star.getbbox(star_str)
    star_w = star_bbox[2] - star_bbox[0]
    sx = cx - star_w // 2
    for i in range(max_stars):
        ch = "★" if i < stars else "☆"
        color = GOLD_STAR if i < stars else EMPTY_STAR
        draw.text((sx, y), ch, fill=color, font=font_star)
        ch_bbox = font_star.getbbox(ch)
        sx += ch_bbox[2] - ch_bbox[0] + 1
    y += 22

    # Rarity + Level
    rarity_color = RARITY_COLORS.get(rarity, TEXT_MED)
    info_text = f"{rarity} · Lv.{level}"
    info_bbox = font_rarity.getbbox(info_text)
    info_w = info_bbox[2] - info_bbox[0]
    draw.text((cx - info_w // 2, y), info_text, fill=rarity_color, font=font_rarity)
    y += 28

    # Stat bars
    stat_order = ["调试力", "耐心值", "混沌值", "智慧值", "毒舌值"]
    bar_margin = x_start + 20
    bar_w = w - 40
    bar_h = 7

    for stat_name in stat_order:
        val = stats.get(stat_name, 0)
        color = STAT_COLORS.get(stat_name, (88, 86, 214))

        # Label + value
        draw.text((bar_margin, y), stat_name, fill=TEXT_DARK, font=font_xs)
        val_text = str(val)
        val_bbox = font_xs.getbbox(val_text)
        val_w_px = val_bbox[2] - val_bbox[0]
        draw.text((bar_margin + bar_w - val_w_px, y), val_text, fill=TEXT_MED, font=font_xs)
        y += 18

        # Bar
        draw_rounded_rect(draw, (bar_margin, y, bar_margin + bar_w, y + bar_h),
                         radius=bar_h // 2, fill=BAR_TRACK)
        fill_w = max(bar_h, int(bar_w * val / 100))
        draw_rounded_rect(draw, (bar_margin, y, bar_margin + fill_w, y + bar_h),
                         radius=bar_h // 2, fill=color)
        y += 16

    return stats


def generate():
    # Load my pet
    if not os.path.exists(PET_JSON):
        print(f"Error: {PET_JSON} not found. Hatch a pet first!")
        sys.exit(1)

    with open(PET_JSON, "r", encoding="utf-8") as f:
        my_pet = json.load(f)

    # Load other pet (if provided)
    other_pet = None
    other_path = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1].strip() else None
    if other_path and os.path.exists(other_path):
        with open(other_path, "r", encoding="utf-8") as f:
            other_pet = json.load(f)

    # Fonts
    font_name = load_font(22, bold=True)
    font_sm = load_font(14)
    font_xs = load_font(12)
    font_star = load_font(14)
    font_rarity = load_font(13)
    font_level = load_font(13, bold=True)
    font_vs = load_font(48, bold=True)
    font_footer = load_font(13)

    fonts = (font_name, font_sm, font_xs, font_star, font_rarity, font_level)

    # ─── Create canvas ───────────────────────────────────────────────────
    card = Image.new("RGBA", (CARD_W, CARD_H), (235, 240, 248, 255))
    draw_gradient_bg(card)
    draw = ImageDraw.Draw(card)

    # Layout: left 45%, center 10%, right 45%
    side_w = int(CARD_W * 0.45)  # 405
    center_x = side_w
    center_w = CARD_W - side_w * 2  # 90

    # Left card background
    draw_rounded_rect(
        draw,
        (10, 10, side_w - 5, CARD_H - 50),
        radius=16, fill=(255, 255, 255, 200), outline=(220, 218, 215), width=1,
    )

    # Right card background
    draw_rounded_rect(
        draw,
        (CARD_W - side_w + 5, 10, CARD_W - 10, CARD_H - 50),
        radius=16, fill=(255, 255, 255, 200), outline=(220, 218, 215), width=1,
    )

    # Draw left pet (my pet)
    my_stats = draw_pet_side(card, ImageDraw.Draw(card), my_pet, 10, side_w - 15, fonts)

    # Draw right pet
    if other_pet:
        other_stats = draw_pet_side(card, ImageDraw.Draw(card), other_pet, CARD_W - side_w + 5, side_w - 15, fonts)
    else:
        other_stats = draw_pet_side(card, ImageDraw.Draw(card), {}, CARD_W - side_w + 5, side_w - 15, fonts, is_placeholder=True)

    draw = ImageDraw.Draw(card)

    # ─── Center VS ───────────────────────────────────────────────────────
    vs_text = "VS"
    vs_bbox = font_vs.getbbox(vs_text)
    vs_w = vs_bbox[2] - vs_bbox[0]
    vs_h = vs_bbox[3] - vs_bbox[1]
    vs_x = center_x + (center_w - vs_w) // 2
    vs_y = 80

    # VS glow circle
    glow_r = 40
    glow = Image.new("RGBA", (glow_r * 2, glow_r * 2), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    glow_draw.ellipse((0, 0, glow_r * 2 - 1, glow_r * 2 - 1), fill=(255, 60, 60, 40))
    glow = glow.filter(ImageFilter.GaussianBlur(radius=12))
    card.paste(glow, (vs_x + vs_w // 2 - glow_r, vs_y + vs_h // 2 - glow_r), glow)
    draw = ImageDraw.Draw(card)

    # VS text with gradient-like red
    draw.text((vs_x + 2, vs_y + 2), vs_text, fill=(180, 30, 30, 80), font=font_vs)  # shadow
    draw.text((vs_x, vs_y), vs_text, fill=(230, 50, 50), font=font_vs)

    # ─── Winner indicators (green dots) ──────────────────────────────────
    if other_pet and other_stats:
        stat_order = ["调试力", "耐心值", "混沌值", "智慧值", "毒舌值"]
        # Position winner dots in center column aligned with stat bars
        dot_start_y = 228  # approximate alignment with stat bars
        dot_spacing = 34

        for i, stat_name in enumerate(stat_order):
            my_val = my_stats.get(stat_name, 0)
            other_val = other_stats.get(stat_name, 0)
            dot_y = dot_start_y + i * dot_spacing

            if my_val > other_val:
                # Green dot on left side
                draw.ellipse((center_x + 10, dot_y, center_x + 22, dot_y + 12), fill=WIN_COLOR)
            elif other_val > my_val:
                # Green dot on right side
                draw.ellipse((center_x + center_w - 22, dot_y, center_x + center_w - 10, dot_y + 12), fill=WIN_COLOR)
            else:
                # Tie - yellow dots on both
                draw.ellipse((center_x + 10, dot_y, center_x + 22, dot_y + 12), fill=(255, 195, 0))
                draw.ellipse((center_x + center_w - 22, dot_y, center_x + center_w - 10, dot_y + 12), fill=(255, 195, 0))

    # ─── Footer ──────────────────────────────────────────────────────────
    footer = "谁的宠物更强？ · Ai小蓝鲸"
    footer_bbox = font_footer.getbbox(footer)
    footer_w = footer_bbox[2] - footer_bbox[0]
    draw.text(((CARD_W - footer_w) // 2, CARD_H - 35), footer, fill=TEXT_LIGHT, font=font_footer)

    # ─── Accent lines ────────────────────────────────────────────────────
    for i in range(3):
        alpha = int(120 - i * 35)
        draw.rectangle((0, i, CARD_W, i + 1), fill=(88, 86, 214, alpha))
        draw.rectangle((0, CARD_H - 1 - i, CARD_W, CARD_H - i), fill=(88, 86, 214, alpha))

    # ─── Save ────────────────────────────────────────────────────────────
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    card_rgb = Image.new("RGB", card.size, (235, 240, 248))
    card_rgb.paste(card, mask=card.split()[3])
    card_rgb.save(OUTPUT_PATH, "PNG", quality=95)
    print(f"VS comparison saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    generate()
