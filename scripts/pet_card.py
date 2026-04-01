#!/usr/bin/env python3
"""
CodePet 宠物卡片生成器
生成一张精美的宠物分享卡片 (PNG 600x800)
"""

import os
import sys
import json
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# ─── Paths ───────────────────────────────────────────────────────────────────

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SPRITE_DIR = os.path.join(SCRIPT_DIR, "..", "sprites")
PET_JSON = os.path.join(os.path.expanduser("~"), ".codepet", "pet.json")
OUTPUT_PATH = os.path.join(os.path.expanduser("~"), ".codepet", "card.png")

# ─── Design tokens ───────────────────────────────────────────────────────────

CARD_W, CARD_H = 600, 800

# ─── Theme system ────────────────────────────────────────────────────────────

THEMES = {
    "default": {
        "BG_COLOR": (252, 250, 245),
        "ACCENT": (88, 86, 214),
        "ACCENT_LIGHT": (118, 116, 234),
        "BAR_TRACK": (240, 238, 232),
        "TEXT_PRIMARY": (40, 40, 45),
        "TEXT_SECONDARY": (120, 118, 115),
        "TEXT_MUTED": (170, 168, 165),
        "GOLD_STAR": (255, 195, 0),
        "EMPTY_STAR": (210, 208, 204),
        "WATERMARK_COLOR": (200, 198, 194),
        "SPRITE_BG": (255, 255, 255, 255),
        "SPRITE_OUTLINE": (235, 233, 228),
        "DIVIDER": (235, 233, 228),
        "EQUIP_BG": (245, 243, 238),
        "EQUIP_OUTLINE": (230, 228, 222),
        "RARITY_COLORS": {
            "普通": (160, 160, 160),
            "优秀": (72, 180, 97),
            "稀有": (66, 135, 245),
            "史诗": (168, 85, 247),
            "传说": (255, 160, 30),
        },
        "STAT_COLORS": {
            "调试力": (66, 135, 245),
            "耐心值": (72, 180, 97),
            "混沌值": (247, 85, 85),
            "智慧值": (168, 85, 247),
            "毒舌值": (255, 160, 30),
        },
    },
    "dark": {
        "BG_COLOR": (18, 18, 24),
        "ACCENT": (160, 90, 255),
        "ACCENT_LIGHT": (190, 130, 255),
        "BAR_TRACK": (40, 40, 52),
        "TEXT_PRIMARY": (230, 228, 235),
        "TEXT_SECONDARY": (150, 148, 160),
        "TEXT_MUTED": (90, 88, 100),
        "GOLD_STAR": (255, 210, 50),
        "EMPTY_STAR": (55, 55, 65),
        "WATERMARK_COLOR": (65, 63, 75),
        "SPRITE_BG": (28, 28, 38, 255),
        "SPRITE_OUTLINE": (50, 48, 62),
        "DIVIDER": (50, 48, 62),
        "EQUIP_BG": (30, 30, 42),
        "EQUIP_OUTLINE": (55, 53, 68),
        "RARITY_COLORS": {
            "普通": (120, 120, 130),
            "优秀": (60, 210, 100),
            "稀有": (80, 160, 255),
            "史诗": (190, 100, 255),
            "传说": (255, 180, 40),
        },
        "STAT_COLORS": {
            "调试力": (80, 160, 255),
            "耐心值": (60, 210, 100),
            "混沌值": (255, 70, 90),
            "智慧值": (190, 100, 255),
            "毒舌值": (255, 180, 40),
        },
    },
}

def get_theme(style_name):
    return THEMES.get(style_name, THEMES["default"])

# Default values (overridden per-call in generate_card)
BG_COLOR = (252, 250, 245)
ACCENT = (88, 86, 214)
ACCENT_LIGHT = (118, 116, 234)
BAR_TRACK = (240, 238, 232)
TEXT_PRIMARY = (40, 40, 45)
TEXT_SECONDARY = (120, 118, 115)
TEXT_MUTED = (170, 168, 165)
GOLD_STAR = (255, 195, 0)
EMPTY_STAR = (210, 208, 204)
WATERMARK_COLOR = (200, 198, 194)

RARITY_COLORS = {
    "普通": (160, 160, 160),
    "优秀": (72, 180, 97),
    "稀有": (66, 135, 245),
    "史诗": (168, 85, 247),
    "传说": (255, 160, 30),
}

STAT_COLORS = {
    "调试力": (66, 135, 245),
    "耐心值": (72, 180, 97),
    "混沌值": (247, 85, 85),
    "智慧值": (168, 85, 247),
    "毒舌值": (255, 160, 30),
}

# ─── Font loading ────────────────────────────────────────────────────────────

def load_font(size, bold=False):
    """Try macOS system fonts with CJK support, fallback gracefully."""
    candidates = [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    # For bold, try index 1 in TTC (usually medium/bold weight)
    font_index = 1 if bold else 0
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size, index=font_index)
            except Exception:
                try:
                    return ImageFont.truetype(path, size, index=0)
                except Exception:
                    continue
    return ImageFont.load_default()


# ─── Drawing helpers ─────────────────────────────────────────────────────────

def draw_rounded_rect(draw, xy, radius, fill=None, outline=None, width=1):
    """Draw a rounded rectangle."""
    x0, y0, x1, y1 = xy
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def draw_stat_bar(draw, x, y, w, h, value, max_val, color, label, font_sm, font_xs,
                  text_primary=None, text_secondary=None, bar_track=None):
    """Draw a single stat bar with label and value."""
    _tp = text_primary or TEXT_PRIMARY
    _ts = text_secondary or TEXT_SECONDARY
    _bt = bar_track or BAR_TRACK
    draw.text((x, y), label, fill=_tp, font=font_sm)
    val_text = str(value)
    val_bbox = font_xs.getbbox(val_text)
    val_w = val_bbox[2] - val_bbox[0]
    draw.text((x + w - val_w, y), val_text, fill=_ts, font=font_xs)
    bar_y = y + 26
    draw_rounded_rect(draw, (x, bar_y, x + w, bar_y + h), radius=h // 2, fill=_bt)
    fill_w = max(h, int(w * value / max_val))
    draw_rounded_rect(draw, (x, bar_y, x + fill_w, bar_y + h), radius=h // 2, fill=color)


def draw_exp_bar(draw, x, y, w, h, exp, level, font_xs,
                 accent=None, bar_track=None, text_muted=None):
    """Draw the experience bar."""
    _ac = accent or ACCENT
    _bt = bar_track or BAR_TRACK
    _tm = text_muted or TEXT_MUTED
    exp_needed = 100 * level
    ratio = min(exp / max(exp_needed, 1), 1.0)
    draw_rounded_rect(draw, (x, y, x + w, y + h), radius=h // 2, fill=_bt)
    fill_w = max(h, int(w * ratio))
    draw_rounded_rect(draw, (x, y, x + fill_w, y + h), radius=h // 2, fill=_ac)
    exp_text = f"EXP {exp}/{exp_needed}"
    exp_bbox = font_xs.getbbox(exp_text)
    exp_w = exp_bbox[2] - exp_bbox[0]
    draw.text((x + (w - exp_w) // 2, y + h + 4), exp_text, fill=_tm, font=font_xs)


# ─── Main card generation ────────────────────────────────────────────────────

def generate_card(style="default"):
    # Load theme
    T = get_theme(style)
    _BG = T["BG_COLOR"]
    _ACCENT = T["ACCENT"]
    _BAR_TRACK = T["BAR_TRACK"]
    _TEXT_PRIMARY = T["TEXT_PRIMARY"]
    _TEXT_SECONDARY = T["TEXT_SECONDARY"]
    _TEXT_MUTED = T["TEXT_MUTED"]
    _GOLD_STAR = T["GOLD_STAR"]
    _EMPTY_STAR = T["EMPTY_STAR"]
    _WATERMARK = T["WATERMARK_COLOR"]
    _SPRITE_BG = T["SPRITE_BG"]
    _SPRITE_OUTLINE = T["SPRITE_OUTLINE"]
    _DIVIDER = T["DIVIDER"]
    _EQUIP_BG = T["EQUIP_BG"]
    _EQUIP_OUTLINE = T["EQUIP_OUTLINE"]
    _RARITY_COLORS = T["RARITY_COLORS"]
    _STAT_COLORS = T["STAT_COLORS"]

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
    exp = pet.get("exp", 0)
    stats = pet.get("stats", {})
    hat = pet.get("hat")
    accessory = pet.get("accessory")

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
    font_rarity = load_font(18)
    font_sm = load_font(16)
    font_xs = load_font(13)
    font_level = load_font(14, bold=True)
    font_watermark = load_font(13)
    font_star = load_font(22)
    font_equip = load_font(14)

    # ─── Create canvas ───────────────────────────────────────────────────

    card = Image.new("RGBA", (CARD_W, CARD_H), _BG + (255,))
    draw = ImageDraw.Draw(card)

    # ─── Dark theme: subtle vignette overlay ─────────────────────────────

    if style == "dark":
        vignette = Image.new("RGBA", (CARD_W, CARD_H), (0, 0, 0, 0))
        vig_draw = ImageDraw.Draw(vignette)
        # Corner darkening
        for i in range(80):
            alpha = int(30 * (1 - i / 80))
            vig_draw.rectangle((0, i, CARD_W, i + 1), fill=(0, 0, 0, alpha))
            vig_draw.rectangle((0, CARD_H - 1 - i, CARD_W, CARD_H - i), fill=(0, 0, 0, alpha))
        card = Image.alpha_composite(card, vignette)
        draw = ImageDraw.Draw(card)

    # ─── Decorative top band ─────────────────────────────────────────────

    for i in range(6):
        alpha = int(180 - i * 30)
        r, g, b = _ACCENT
        draw.rectangle((0, i, CARD_W, i + 1), fill=(r, g, b, alpha))

    # ─── Dark theme: glow effect behind sprite ───────────────────────────

    sprite_target_w = 280
    scale = sprite_target_w / sprite.width
    sprite_target_h = int(sprite.height * scale)
    sprite_resized = sprite.resize(
        (sprite_target_w, sprite_target_h), Image.Resampling.NEAREST
    )

    sprite_x = (CARD_W - sprite_target_w) // 2
    sprite_y = 40

    if style == "dark":
        # Purple glow behind sprite
        glow = Image.new("RGBA", (sprite_target_w + 80, sprite_target_h + 80), (0, 0, 0, 0))
        glow_draw = ImageDraw.Draw(glow)
        glow_draw.rounded_rectangle(
            (0, 0, sprite_target_w + 79, sprite_target_h + 79),
            radius=30, fill=_ACCENT + (35,)
        )
        glow = glow.filter(ImageFilter.GaussianBlur(radius=20))
        card.paste(glow, (sprite_x - 40, sprite_y - 30), glow)
        draw = ImageDraw.Draw(card)
    else:
        # Light theme shadow
        shadow = Image.new("RGBA", (sprite_target_w + 20, sprite_target_h + 20), (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow)
        shadow_draw.rounded_rectangle(
            (0, 0, sprite_target_w + 19, sprite_target_h + 19),
            radius=20, fill=(0, 0, 0, 40)
        )
        shadow = shadow.filter(ImageFilter.GaussianBlur(radius=10))
        card.paste(shadow, (sprite_x - 10, sprite_y + 5), shadow)

    # Sprite background card
    sprite_bg_pad = 24
    draw_rounded_rect(
        draw,
        (
            sprite_x - sprite_bg_pad,
            sprite_y - sprite_bg_pad + 10,
            sprite_x + sprite_target_w + sprite_bg_pad,
            sprite_y + sprite_target_h + sprite_bg_pad - 5,
        ),
        radius=20,
        fill=_SPRITE_BG,
        outline=_SPRITE_OUTLINE,
        width=1,
    )
    card.paste(sprite_resized, (sprite_x, sprite_y), sprite_resized)

    # ─── Name ────────────────────────────────────────────────────────────

    y_cursor = sprite_y + sprite_target_h + sprite_bg_pad + 12

    name_bbox = font_name.getbbox(name)
    name_w = name_bbox[2] - name_bbox[0]
    draw.text(((CARD_W - name_w) // 2, y_cursor), name, fill=_TEXT_PRIMARY, font=font_name)
    y_cursor += 46

    # ─── Stars & Rarity ──────────────────────────────────────────────────

    max_stars = 5
    star_str = "★" * stars + "☆" * (max_stars - stars)
    star_bbox = font_star.getbbox(star_str)
    star_w = star_bbox[2] - star_bbox[0]

    rarity_color = _RARITY_COLORS.get(rarity, _TEXT_SECONDARY)
    rarity_bbox = font_rarity.getbbox(rarity)
    rarity_w = rarity_bbox[2] - rarity_bbox[0]

    total_w = star_w + 12 + rarity_w
    start_x = (CARD_W - total_w) // 2

    sx = start_x
    for i, ch in enumerate(star_str):
        color = _GOLD_STAR if i < stars else _EMPTY_STAR
        draw.text((sx, y_cursor), ch, fill=color, font=font_star)
        ch_bbox = font_star.getbbox(ch)
        sx += ch_bbox[2] - ch_bbox[0] + 1

    # Rarity badge
    badge_x = sx + 12
    badge_y = y_cursor + 2
    badge_pad_x, badge_pad_y = 10, 3
    draw_rounded_rect(
        draw,
        (
            badge_x - badge_pad_x,
            badge_y - badge_pad_y,
            badge_x + rarity_w + badge_pad_x,
            badge_y + (rarity_bbox[3] - rarity_bbox[1]) + badge_pad_y + 2,
        ),
        radius=10,
        fill=rarity_color + (30,),
        outline=rarity_color + (80,),
        width=1,
    )
    draw.text((badge_x, badge_y), rarity, fill=rarity_color, font=font_rarity)
    y_cursor += 36

    # ─── Level & EXP ─────────────────────────────────────────────────────

    level_text = f"Lv.{level}"
    level_bbox = font_level.getbbox(level_text)
    level_w = level_bbox[2] - level_bbox[0]

    bar_margin = 60
    bar_w = CARD_W - bar_margin * 2 - level_w - 16

    draw.text((bar_margin, y_cursor), level_text, fill=_ACCENT, font=font_level)
    draw_exp_bar(draw, bar_margin + level_w + 16, y_cursor + 2, bar_w, 12, exp, level, font_xs,
                 accent=_ACCENT, bar_track=_BAR_TRACK, text_muted=_TEXT_MUTED)
    y_cursor += 42

    # ─── Divider ─────────────────────────────────────────────────────────

    div_margin = 50
    draw.line(
        (div_margin, y_cursor, CARD_W - div_margin, y_cursor),
        fill=_DIVIDER, width=1,
    )
    y_cursor += 16

    # ─── Stats ───────────────────────────────────────────────────────────

    stat_margin = 50
    stat_w = CARD_W - stat_margin * 2
    stat_order = ["调试力", "耐心值", "混沌值", "智慧值", "毒舌值"]

    for stat_name in stat_order:
        val = stats.get(stat_name, 0)
        color = _STAT_COLORS.get(stat_name, _ACCENT)
        draw_stat_bar(draw, stat_margin, y_cursor, stat_w, 10, val, 100, color, stat_name, font_sm, font_xs,
                      text_primary=_TEXT_PRIMARY, text_secondary=_TEXT_SECONDARY, bar_track=_BAR_TRACK)
        y_cursor += 46

    # ─── Equipment info ──────────────────────────────────────────────────

    equip_parts = []
    if hat:
        equip_parts.append(f"🎩 {hat}")
    if accessory:
        equip_parts.append(f"✨ {accessory}")

    if equip_parts:
        y_cursor += 4
        equip_text = "   ".join(equip_parts)
        equip_bbox = font_equip.getbbox(equip_text)
        equip_w = equip_bbox[2] - equip_bbox[0]
        eq_x = (CARD_W - equip_w) // 2
        eq_y = y_cursor

        draw_rounded_rect(
            draw,
            (eq_x - 16, eq_y - 6, eq_x + equip_w + 16, eq_y + 22),
            radius=12,
            fill=_EQUIP_BG,
            outline=_EQUIP_OUTLINE,
            width=1,
        )
        draw.text((eq_x, eq_y), equip_text, fill=_TEXT_SECONDARY, font=font_equip)
        y_cursor += 36

    # ─── Watermark ───────────────────────────────────────────────────────

    watermark = "Ai小蓝鲸"
    wm_bbox = font_watermark.getbbox(watermark)
    wm_w = wm_bbox[2] - wm_bbox[0]
    draw.text(
        ((CARD_W - wm_w) // 2, CARD_H - 36),
        watermark,
        fill=_WATERMARK,
        font=font_watermark,
    )

    # ─── Bottom accent line ──────────────────────────────────────────────

    for i in range(4):
        alpha = int(120 - i * 30)
        r, g, b = _ACCENT
        draw.rectangle((0, CARD_H - 1 - i, CARD_W, CARD_H - i), fill=(r, g, b, alpha))

    # ─── Save & open ─────────────────────────────────────────────────────

    suffix = f"-{style}" if style != "default" else ""
    out_path = os.path.join(os.path.expanduser("~"), ".codepet", f"card{suffix}.png")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    card_rgb = Image.new("RGB", card.size, _BG)
    card_rgb.paste(card, mask=card.split()[3])
    card_rgb.save(out_path, "PNG", quality=95)
    print(f"Card saved to {out_path}")

    if sys.platform == "darwin":
        os.system(f'open "{out_path}"')


if __name__ == "__main__":
    style = sys.argv[1] if len(sys.argv) > 1 else "default"
    generate_card(style)
