#!/usr/bin/env python3
"""
CodePet 小红书/朋友圈分享图生成器
生成 1080x1440 (3:4) 分享图，适配小红书和微信朋友圈
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
OUTPUT_PATH = os.path.join(os.path.expanduser("~"), ".codepet", "xhs_share.png")

# ─── Design tokens ──────────────────────────────────────────────────────────
CARD_W, CARD_H = 1080, 1440

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

ACHIEVEMENT_ICONS = {
    "first_pat": "🤚",
    "first_feed": "🍕",
    "lv2": "2️⃣",
    "lv3": "3️⃣",
    "lv5": "5️⃣",
    "lv6": "6️⃣",
    "lv10": "🔟",
    "lv15": "🏅",
    "lv20": "🏆",
    "exp100": "💯",
    "exp500": "🌟",
    "exp1000": "✨",
    "exp5000": "💎",
    "rare": "💙",
    "epic": "💜",
    "legendary": "🧡",
    "shiny": "🌈",
    "pat10": "💕",
    "pat50": "💖",
    "feed10": "🍰",
    "feed50": "🎂",
    "hat": "🎩",
    "accessory": "💍",
}

TEXT_DARK = (50, 40, 45)
TEXT_MED = (100, 90, 95)
TEXT_LIGHT = (160, 150, 155)


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


def pixelate_sprite(sprite, pixel_size=6):
    small_w = max(1, sprite.width // pixel_size)
    small_h = max(1, sprite.height // pixel_size)
    small = sprite.resize((small_w, small_h), Image.Resampling.NEAREST)
    return small.resize((sprite.width, sprite.height), Image.Resampling.NEAREST)


def draw_rounded_rect(draw, xy, radius, fill=None, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def draw_gradient_bg(img):
    """Draw warm pink gradient background."""
    draw = ImageDraw.Draw(img)
    top = (255, 240, 235)     # #FFF0EB
    bottom = (255, 232, 224)  # #FFE8E0
    for y in range(CARD_H):
        ratio = y / CARD_H
        r = int(top[0] + (bottom[0] - top[0]) * ratio)
        g = int(top[1] + (bottom[1] - top[1]) * ratio)
        b = int(top[2] + (bottom[2] - top[2]) * ratio)
        draw.line((0, y, CARD_W, y), fill=(r, g, b))


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
    achievements = pet.get("achievements", [])
    catchphrase = pet.get("catchphrase", "")

    # Load sprite
    sprite_path = os.path.join(SPRITE_DIR, character, "normal.png")
    if not os.path.exists(sprite_path):
        sprite_path = os.path.join(SPRITE_DIR, f"{character}.png")
    if not os.path.exists(sprite_path):
        print(f"Error: Sprite not found for '{character}'")
        sys.exit(1)

    sprite = Image.open(sprite_path).convert("RGBA")

    # Load fonts
    font_name = load_font(36, bold=True)
    font_rarity = load_font(20)
    font_star = load_font(26)
    font_stat_label = load_font(20)
    font_stat_val = load_font(16)
    font_quote = load_font(22)
    font_share = load_font(24, bold=True)
    font_footer = load_font(16)
    font_badge = load_font(28)
    font_level = load_font(18, bold=True)

    # ─── Create canvas with gradient ─────────────────────────────────────
    card = Image.new("RGBA", (CARD_W, CARD_H), (255, 240, 235, 255))
    draw_gradient_bg(card)
    draw = ImageDraw.Draw(card)

    y_cursor = 60

    # ─── Sprite with white card behind ───────────────────────────────────
    sprite_target_h = 360
    scale = sprite_target_h / sprite.height
    sprite_target_w = int(sprite.width * scale)
    sprite_resized = sprite.resize((sprite_target_w, sprite_target_h), Image.Resampling.NEAREST)
    sprite_pixelated = pixelate_sprite(sprite_resized, pixel_size=6)

    sprite_x = (CARD_W - sprite_target_w) // 2
    sprite_y = y_cursor

    # White card background with shadow
    card_pad = 24
    shadow = Image.new("RGBA", (sprite_target_w + card_pad * 2 + 20, sprite_target_h + card_pad * 2 + 20), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rounded_rectangle(
        (0, 0, shadow.width - 1, shadow.height - 1),
        radius=24, fill=(0, 0, 0, 25)
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=10))
    card.paste(shadow, (sprite_x - card_pad - 5, sprite_y - card_pad + 5), shadow)
    draw = ImageDraw.Draw(card)

    draw_rounded_rect(
        draw,
        (sprite_x - card_pad, sprite_y - card_pad,
         sprite_x + sprite_target_w + card_pad, sprite_y + sprite_target_h + card_pad),
        radius=20, fill=(255, 255, 255, 240), outline=(240, 230, 225), width=1,
    )
    card.paste(sprite_pixelated, (sprite_x, sprite_y), sprite_pixelated)

    y_cursor = sprite_y + sprite_target_h + card_pad + 30

    # ─── Name + Stars + Rarity badge ─────────────────────────────────────
    name_bbox = font_name.getbbox(name)
    name_w = name_bbox[2] - name_bbox[0]
    draw.text(((CARD_W - name_w) // 2, y_cursor), name, fill=TEXT_DARK, font=font_name)
    y_cursor += 50

    # Stars centered
    max_stars = 5
    star_str = "★" * stars + "☆" * (max_stars - stars)
    star_bbox = font_star.getbbox(star_str)
    star_w = star_bbox[2] - star_bbox[0]

    rarity_color = RARITY_COLORS.get(rarity, TEXT_MED)
    rarity_bbox = font_rarity.getbbox(rarity)
    rarity_w = rarity_bbox[2] - rarity_bbox[0]
    rarity_h = rarity_bbox[3] - rarity_bbox[1]

    total_w = star_w + 16 + rarity_w + 20
    start_x = (CARD_W - total_w) // 2

    sx = start_x
    for i in range(max_stars):
        ch = "★" if i < stars else "☆"
        color = (255, 195, 0) if i < stars else (220, 215, 210)
        draw.text((sx, y_cursor), ch, fill=color, font=font_star)
        ch_bbox = font_star.getbbox(ch)
        sx += ch_bbox[2] - ch_bbox[0] + 1

    # Rarity badge
    badge_x = sx + 16
    badge_y = y_cursor + 3
    draw_rounded_rect(
        draw,
        (badge_x - 10, badge_y - 3, badge_x + rarity_w + 10, badge_y + rarity_h + 5),
        radius=10, fill=rarity_color + (35,), outline=rarity_color + (90,), width=1,
    )
    draw.text((badge_x, badge_y), rarity, fill=rarity_color, font=font_rarity)
    y_cursor += 40

    # Level
    level_text = f"Lv.{level}"
    level_bbox = font_level.getbbox(level_text)
    level_w = level_bbox[2] - level_bbox[0]
    draw.text(((CARD_W - level_w) // 2, y_cursor), level_text, fill=(88, 86, 214), font=font_level)
    y_cursor += 35

    # ─── Catchphrase / quote ─────────────────────────────────────────────
    if catchphrase:
        quote = f'"{catchphrase}"'
        quote_bbox = font_quote.getbbox(quote)
        quote_w = quote_bbox[2] - quote_bbox[0]
        draw.text(((CARD_W - quote_w) // 2, y_cursor), quote, fill=TEXT_MED, font=font_quote)
        y_cursor += 40

    y_cursor += 10

    # ─── Stats panel ─────────────────────────────────────────────────────
    stat_order = ["调试力", "耐心值", "混沌值", "智慧值", "毒舌值"]
    stat_margin = 100
    stat_w = CARD_W - stat_margin * 2
    bar_h = 10

    # Panel background
    panel_h = len(stat_order) * 50 + 20
    draw_rounded_rect(
        draw,
        (stat_margin - 20, y_cursor - 10, CARD_W - stat_margin + 20, y_cursor + panel_h),
        radius=16, fill=(255, 255, 255, 180), outline=(240, 230, 225), width=1,
    )

    panel_y = y_cursor + 10
    for stat_name in stat_order:
        val = stats.get(stat_name, 0)
        color = STAT_COLORS.get(stat_name, (88, 86, 214))

        # Label
        draw.text((stat_margin, panel_y), stat_name, fill=TEXT_DARK, font=font_stat_label)
        val_text = str(val)
        val_bbox = font_stat_val.getbbox(val_text)
        val_w = val_bbox[2] - val_bbox[0]
        draw.text((stat_margin + stat_w - val_w, panel_y + 2), val_text, fill=TEXT_MED, font=font_stat_val)

        # Bar
        bar_y = panel_y + 28
        draw_rounded_rect(draw, (stat_margin, bar_y, stat_margin + stat_w, bar_y + bar_h),
                         radius=bar_h // 2, fill=(240, 235, 230))
        fill_w = max(bar_h, int(stat_w * val / 100))
        draw_rounded_rect(draw, (stat_margin, bar_y, stat_margin + fill_w, bar_y + bar_h),
                         radius=bar_h // 2, fill=color)
        panel_y += 50

    y_cursor += panel_h + 20

    # ─── Achievement badges ──────────────────────────────────────────────
    if achievements:
        shown = achievements[:6]
        badge_str = " ".join(ACHIEVEMENT_ICONS.get(a, "🏅") for a in shown)
        badge_bbox = font_badge.getbbox(badge_str)
        badge_w = badge_bbox[2] - badge_bbox[0]
        draw.text(((CARD_W - badge_w) // 2, y_cursor), badge_str, fill=TEXT_DARK, font=font_badge)
        if len(achievements) > 6:
            extra = f"+{len(achievements) - 6}"
            extra_bbox = font_stat_val.getbbox(extra)
            draw.text(((CARD_W + badge_w) // 2 + 8, y_cursor + 6), extra, fill=TEXT_LIGHT, font=font_stat_val)
        y_cursor += 50

    # ─── Share text ──────────────────────────────────────────────────────
    share_text = "我的编程搭子，你也来养一只？"
    share_bbox = font_share.getbbox(share_text)
    share_w = share_bbox[2] - share_bbox[0]
    draw.text(((CARD_W - share_w) // 2, y_cursor), share_text, fill=TEXT_DARK, font=font_share)
    y_cursor += 50

    # ─── Decorative divider ─────────────────────────────────────────────
    y_cursor += 20
    div_w = 200
    div_x = (CARD_W - div_w) // 2
    draw.line((div_x, y_cursor, div_x + div_w, y_cursor), fill=(220, 210, 205), width=1)
    y_cursor += 20

    # ─── Footer ──────────────────────────────────────────────────────────
    footer = "CodePet · Ai小蓝鲸 · npm i -g codepet"
    footer_bbox = font_footer.getbbox(footer)
    footer_w = footer_bbox[2] - footer_bbox[0]
    draw.text(((CARD_W - footer_w) // 2, y_cursor), footer, fill=TEXT_LIGHT, font=font_footer)
    y_cursor += 50

    # ─── Crop to actual content height (maintain 3:4 ratio) ────────────
    # Ensure minimum height respects 3:4 ratio, but don't leave huge blank areas
    content_h = y_cursor
    # Snap to 3:4 ratio: width=1080, ideal height=1440
    # If content is shorter, use the smaller of 1440 or content + padding
    final_h = min(CARD_H, max(content_h, int(CARD_W * 4 / 3 * 0.7)))
    # Keep 3:4 friendly: round to nearest multiple that looks good
    final_h = max(final_h, content_h)
    if final_h < CARD_H:
        card = card.crop((0, 0, CARD_W, final_h))

    # ─── Save ────────────────────────────────────────────────────────────
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    bg_color = (255, 240, 235)
    card_rgb = Image.new("RGB", card.size, bg_color)
    card_rgb.paste(card, mask=card.split()[3])
    card_rgb.save(OUTPUT_PATH, "PNG", quality=95)
    print(f"XHS share image saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    generate()
