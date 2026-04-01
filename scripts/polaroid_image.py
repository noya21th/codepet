#!/usr/bin/env python3
"""拍立得相框 — 生成 PNG 图片版（Windows 和通用平台）"""

import sys, os, json, platform
from PIL import Image, ImageDraw, ImageFont

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SPRITE_DIR = os.path.join(SCRIPT_DIR, "..", "sprites")
PET_JSON = os.path.join(os.path.expanduser("~"), ".codepet", "pet.json")
OUTPUT = os.path.join(os.path.expanduser("~"), ".codepet", "photo.png")

SCENE_ZH = {
    'normal': '日常', 'happy': '开心的瞬间', 'sleep': '睡着了',
    'eat': '在吃东西', 'pet': '被摸摸的样子', 'worry': '有点紧张',
}

def load_font(size):
    """跨平台加载字体"""
    system = platform.system()
    candidates = []
    if system == "Darwin":
        candidates = [
            "/System/Library/Fonts/PingFang.ttc",
            "/System/Library/Fonts/Hiragino Sans GB.ttc",
        ]
    elif system == "Windows":
        windir = os.environ.get("WINDIR", "C:\\Windows")
        candidates = [
            os.path.join(windir, "Fonts", "msyh.ttc"),
            os.path.join(windir, "Fonts", "simhei.ttf"),
            os.path.join(windir, "Fonts", "arial.ttf"),
        ]
    else:
        candidates = [
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ]
    for fp in candidates:
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size)
            except:
                continue
    return ImageFont.load_default()

def main():
    character = sys.argv[1] if len(sys.argv) > 1 else 'bagayalu'
    scene = sys.argv[2] if len(sys.argv) > 2 else 'normal'

    img_path = os.path.join(SPRITE_DIR, character, f"{scene}.png")
    if not os.path.exists(img_path):
        img_path = os.path.join(SPRITE_DIR, f"{character}.png")

    name = character
    try:
        with open(PET_JSON, 'r', encoding='utf-8') as f:
            pet = json.load(f)
            name = pet.get('nickname', pet.get('name', character))
    except:
        pass

    scene_zh = SCENE_ZH.get(scene, '一个瞬间')

    # 加载角色图片
    sprite = Image.open(img_path).convert("RGBA")

    # 拍立得尺寸
    padding = 40
    bottom_area = 120
    photo_w = sprite.width + padding * 2
    photo_h = sprite.height + padding + bottom_area

    # 白色拍立得底板
    card = Image.new("RGBA", (photo_w, photo_h), (255, 255, 255, 255))

    # 贴角色图片
    card.paste(sprite, (padding, padding), sprite)

    # 画边框阴影
    draw = ImageDraw.Draw(card)
    draw.rectangle([0, 0, photo_w - 1, photo_h - 1], outline=(200, 200, 200), width=2)

    # 底部文字
    font_caption = load_font(18)
    font_studio = load_font(14)

    caption = f"📸 刚才抓拍到了{name}{scene_zh}..."
    studio = "🐋 Ai小蓝鲸照相馆"

    caption_y = sprite.height + padding + 15
    studio_y = caption_y + 35

    draw.text((padding, caption_y), caption, fill=(80, 80, 80), font=font_caption)
    draw.text((padding, studio_y), studio, fill=(140, 140, 140), font=font_studio)

    # 保存
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    card_rgb = Image.new("RGB", card.size, (255, 255, 255))
    card_rgb.paste(card, mask=card.split()[3])
    card_rgb.save(OUTPUT, "PNG", quality=95)

    # 不在这里打开，让 Node.js 调用方负责打开
    print(OUTPUT)

if __name__ == '__main__':
    main()
