#!/usr/bin/env python3
"""
CodePet QR Code 分享卡片生成器
生成 800x450 分享卡片，左侧宠物信息 + 右侧 QR 码
"""

import os
import sys
import json
import platform
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# ─── Auto-install qrcode ────────────────────────────────────────────────────
try:
    import qrcode
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'qrcode[pil]', '--quiet'])
    import qrcode

# ─── Paths ───────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SPRITE_DIR = os.path.join(SCRIPT_DIR, "..", "sprites")
PET_JSON = os.path.join(os.path.expanduser("~"), ".codepet", "pet.json")
OUTPUT_PATH = os.path.join(os.path.expanduser("~"), ".codepet", "share_card.png")

# ─── Design tokens ──────────────────────────────────────────────────────────
CARD_W, CARD_H = 800, 450
BG_COLOR = (252, 250, 245)
ACCENT = (88, 86, 214)
TEXT_PRIMARY = (40, 40, 45)
TEXT_SECONDARY = (120, 118, 115)
TEXT_MUTED = (170, 168, 165)
GOLD_STAR = (255, 195, 0)
EMPTY_STAR = (210, 208, 204)
BAR_TRACK = (240, 238, 232)

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


def pixelate_sprite(sprite, pixel_size=8):
    """Resize down then back up for pixel art effect."""
    small_w = max(1, sprite.width // pixel_size)
    small_h = max(1, sprite.height // pixel_size)
    small = sprite.resize((small_w, small_h), Image.Resampling.NEAREST)
    return small.resize((sprite.width, sprite.height), Image.Resampling.NEAREST)


def draw_rounded_rect(draw, xy, radius, fill=None, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def draw_stat_bar(draw, x, y, w, h, value, max_val, color, label, font_sm, font_xs):
    draw.text((x, y), label, fill=TEXT_PRIMARY, font=font_sm)
    val_text = str(value)
    val_bbox = font_xs.getbbox(val_text)
    val_w = val_bbox[2] - val_bbox[0]
    draw.text((x + w - val_w, y), val_text, fill=TEXT_SECONDARY, font=font_xs)
    bar_y = y + 22
    draw_rounded_rect(draw, (x, bar_y, x + w, bar_y + h), radius=h // 2, fill=BAR_TRACK)
    fill_w = max(h, int(w * value / max_val))
    draw_rounded_rect(draw, (x, bar_y, x + fill_w, bar_y + h), radius=h // 2, fill=color)


def generate():
    # Load pet data
    if not os.path.exists(PET_JSON):
        print(f"Error: {PET_JSON} not found. Hatch a pet first!")
        sys.exit(1)

    with open(PET_JSON, "r", encoding="utf-8") as f:
        pet = json.load(f)

    name = pet.get("nickname") or pet.get("name", "???")
    character = pet.get("character", "bagayalu")
    rarity = pet.get("rarity", "普通")
    stars = pet.get("stars", 1)
    level = pet.get("level", 1)
    stats = pet.get("stats", {})

    # Load sprite
    sprite_path = os.path.join(SPRITE_DIR, character, "normal.png")
    if not os.path.exists(sprite_path):
        sprite_path = os.path.join(SPRITE_DIR, f"{character}.png")
    if not os.path.exists(sprite_path):
        print(f"Error: Sprite not found for '{character}'")
        sys.exit(1)

    sprite = Image.open(sprite_path).convert("RGBA")

    # Load fonts
    font_name = load_font(32, bold=True)
    font_sm = load_font(15)
    font_xs = load_font(12)
    font_star = load_font(20)
    font_rarity = load_font(16)
    font_footer = load_font(13)
    font_qr_label = load_font(16, bold=True)

    # ─── Create canvas ───────────────────────────────────────────────────
    card = Image.new("RGBA", (CARD_W, CARD_H), BG_COLOR + (255,))
    draw = ImageDraw.Draw(card)

    # Subtle shadow border (draw on slightly larger canvas, crop later)
    # Instead, add a subtle inner shadow effect
    for i in range(3):
        alpha = int(40 - i * 12)
        draw.rectangle((i, i, CARD_W - 1 - i, CARD_H - 1 - i), outline=(180, 178, 170, alpha))

    # ─── Left side (60% = 480px) ─────────────────────────────────────────
    left_w = 480
    left_pad = 30

    # Sprite area
    sprite_target_h = 180
    scale = sprite_target_h / sprite.height
    sprite_target_w = int(sprite.width * scale)
    sprite_resized = sprite.resize((sprite_target_w, sprite_target_h), Image.Resampling.NEAREST)
    sprite_pixelated = pixelate_sprite(sprite_resized, pixel_size=8)

    sprite_x = left_pad + 20
    sprite_y = 30

    # Sprite background
    sp_bg_pad = 12
    draw_rounded_rect(
        draw,
        (sprite_x - sp_bg_pad, sprite_y - sp_bg_pad,
         sprite_x + sprite_target_w + sp_bg_pad, sprite_y + sprite_target_h + sp_bg_pad),
        radius=14, fill=(255, 255, 255, 255), outline=(235, 233, 228), width=1,
    )
    card.paste(sprite_pixelated, (sprite_x, sprite_y), sprite_pixelated)

    # Name + info to the right of sprite
    info_x = sprite_x + sprite_target_w + sp_bg_pad + 20
    info_y = sprite_y + 10

    draw.text((info_x, info_y), name, fill=TEXT_PRIMARY, font=font_name)
    info_y += 40

    # Stars
    max_stars = 5
    sx = info_x
    for i in range(max_stars):
        ch = "★" if i < stars else "☆"
        color = GOLD_STAR if i < stars else EMPTY_STAR
        draw.text((sx, info_y), ch, fill=color, font=font_star)
        ch_bbox = font_star.getbbox(ch)
        sx += ch_bbox[2] - ch_bbox[0] + 1
    info_y += 28

    # Rarity badge
    rarity_color = RARITY_COLORS.get(rarity, TEXT_SECONDARY)
    rarity_bbox = font_rarity.getbbox(rarity)
    rarity_w = rarity_bbox[2] - rarity_bbox[0]
    rarity_h = rarity_bbox[3] - rarity_bbox[1]
    draw_rounded_rect(
        draw,
        (info_x - 6, info_y - 2, info_x + rarity_w + 6, info_y + rarity_h + 4),
        radius=8, fill=rarity_color + (30,), outline=rarity_color + (80,), width=1,
    )
    draw.text((info_x, info_y), rarity, fill=rarity_color, font=font_rarity)
    info_y += 28

    # Level
    draw.text((info_x, info_y), f"Lv.{level}", fill=ACCENT, font=font_sm)

    # ─── Top 2 stats as bars ────────────────────────────────────────────
    stat_order = ["调试力", "耐心值", "混沌值", "智慧值", "毒舌值"]
    # Pick top 2 by value
    sorted_stats = sorted(stat_order, key=lambda s: stats.get(s, 0), reverse=True)
    top2 = sorted_stats[:2]

    bar_x = left_pad + 10
    bar_y = sprite_y + sprite_target_h + sp_bg_pad + 24
    bar_w = left_w - left_pad * 2

    for stat_name in top2:
        val = stats.get(stat_name, 0)
        color = STAT_COLORS.get(stat_name, ACCENT)
        draw_stat_bar(draw, bar_x, bar_y, bar_w, 8, val, 100, color, stat_name, font_sm, font_xs)
        bar_y += 40

    # ─── Right side (40% = 320px): QR code ──────────────────────────────
    right_x = left_w
    right_w = CARD_W - left_w

    # Divider line
    draw.line((right_x, 20, right_x, CARD_H - 20), fill=(235, 233, 228), width=1)

    # Generate QR code
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=6, border=2)
    qr.add_data("https://www.npmjs.com/package/codepet")
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color=(40, 40, 45), back_color=BG_COLOR).convert("RGBA")

    # Resize QR to fit
    qr_size = min(220, right_w - 40)
    qr_img = qr_img.resize((qr_size, qr_size), Image.Resampling.NEAREST)

    qr_x = right_x + (right_w - qr_size) // 2
    qr_y = (CARD_H - qr_size) // 2 - 30
    card.paste(qr_img, (qr_x, qr_y), qr_img)

    # "扫码安装" label
    label = "扫码安装"
    label_bbox = font_qr_label.getbbox(label)
    label_w = label_bbox[2] - label_bbox[0]
    draw.text((right_x + (right_w - label_w) // 2, qr_y + qr_size + 12), label, fill=TEXT_PRIMARY, font=font_qr_label)

    # npm command
    npm_text = "npm i -g codepet"
    npm_bbox = font_xs.getbbox(npm_text)
    npm_w = npm_bbox[2] - npm_bbox[0]
    draw.text((right_x + (right_w - npm_w) // 2, qr_y + qr_size + 36), npm_text, fill=TEXT_MUTED, font=font_xs)

    # ─── Footer ──────────────────────────────────────────────────────────
    footer = "CodePet · Ai小蓝鲸"
    footer_bbox = font_footer.getbbox(footer)
    footer_w = footer_bbox[2] - footer_bbox[0]
    draw.text(((CARD_W - footer_w) // 2, CARD_H - 32), footer, fill=TEXT_MUTED, font=font_footer)

    # ─── Accent lines ────────────────────────────────────────────────────
    for i in range(4):
        alpha = int(150 - i * 35)
        r, g, b = ACCENT
        draw.rectangle((0, i, CARD_W, i + 1), fill=(r, g, b, alpha))
        draw.rectangle((0, CARD_H - 1 - i, CARD_W, CARD_H - i), fill=(r, g, b, alpha))

    # ─── Save ────────────────────────────────────────────────────────────
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    card_rgb = Image.new("RGB", card.size, BG_COLOR)
    card_rgb.paste(card, mask=card.split()[3])
    card_rgb.save(OUTPUT_PATH, "PNG", quality=95)
    print(f"Share card saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    generate()
