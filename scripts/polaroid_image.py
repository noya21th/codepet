#!/usr/bin/env python3
"""拍立得相框 — 像素风 PNG 图片版"""

import sys, os, json, platform
from PIL import Image, ImageDraw, ImageFont, ImageFilter

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SPRITE_DIR = os.path.join(SCRIPT_DIR, "..", "sprites")
PET_JSON = os.path.join(os.path.expanduser("~"), ".codepet", "pet.json")
OUTPUT = os.path.join(os.path.expanduser("~"), ".codepet", "photo.png")

SCENE_ZH = {
    'normal': '日常', 'happy': '开心的瞬间', 'sleep': '睡着了',
    'eat': '在吃东西', 'pet': '被摸摸的样子', 'worry': '有点紧张',
}

def load_font(size):
    system = platform.system()
    candidates = []
    if system == "Darwin":
        candidates = ["/System/Library/Fonts/PingFang.ttc", "/System/Library/Fonts/Hiragino Sans GB.ttc"]
    elif system == "Windows":
        windir = os.environ.get("WINDIR", "C:\\Windows")
        candidates = [os.path.join(windir, "Fonts", "msyh.ttc"), os.path.join(windir, "Fonts", "simhei.ttf"), os.path.join(windir, "Fonts", "arial.ttf")]
    else:
        candidates = ["/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]
    for fp in candidates:
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size)
            except:
                continue
    return ImageFont.load_default()

def pixelate(img, pixel_size=8):
    """把图片像素化 — 缩小再放大，产生像素颗粒感"""
    w, h = img.size
    small = img.resize((w // pixel_size, h // pixel_size), Image.NEAREST)
    return small.resize((w, h), Image.NEAREST)

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

    # 加载并像素化角色图片
    sprite = Image.open(img_path).convert("RGBA")

    # 统一缩放到 400px 宽
    target_w = 400
    ratio = target_w / sprite.width
    target_h = int(sprite.height * ratio)
    sprite = sprite.resize((target_w, target_h), Image.LANCZOS)

    # 像素化处理 — 产生复古像素风
    sprite = pixelate(sprite, pixel_size=6)

    # 拍立得尺寸
    padding = 50
    bottom_area = 140
    photo_w = sprite.width + padding * 2
    photo_h = sprite.height + padding + bottom_area

    # 奶白色拍立得底板
    card = Image.new("RGBA", (photo_w, photo_h), (252, 250, 245, 255))

    # 贴像素化的角色图片
    card.paste(sprite, (padding, padding), sprite)

    draw = ImageDraw.Draw(card)

    # 图片区域细边框
    draw.rectangle(
        [padding - 2, padding - 2, padding + sprite.width + 1, padding + sprite.height + 1],
        outline=(220, 218, 210), width=1
    )

    # 外边框阴影
    draw.rectangle([0, 0, photo_w - 1, photo_h - 1], outline=(210, 208, 200), width=2)

    # 底部文字
    font_caption = load_font(20)
    font_studio = load_font(15)

    caption = f"📸 刚才抓拍到了{name}{scene_zh}..."
    studio = "🐋 Ai小蓝鲸照相馆"

    caption_y = sprite.height + padding + 20
    studio_y = caption_y + 45

    draw.text((padding, caption_y), caption, fill=(80, 80, 80), font=font_caption)
    draw.text((padding, studio_y), studio, fill=(160, 158, 150), font=font_studio)

    # 保存
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    card_rgb = Image.new("RGB", card.size, (252, 250, 245))
    card_rgb.paste(card, mask=card.split()[3])
    card_rgb.save(OUTPUT, "PNG", quality=95)

    print(OUTPUT)

if __name__ == '__main__':
    main()
